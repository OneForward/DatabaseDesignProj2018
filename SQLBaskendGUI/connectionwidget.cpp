#include "connectionwidget.h"

#include <QtWidgets>
#include <QtSql>


ConnectionWidget::ConnectionWidget(QWidget *parent)
    : QWidget(parent), info("")
{
    QVBoxLayout *layout = new QVBoxLayout(this);
    tree = new QTreeWidget(this);
    tree->setObjectName(QLatin1String("tree"));
    tree->setHeaderLabels(QStringList(tr("服务器数据库")));
    tree->header()->setSectionResizeMode(QHeaderView::Stretch);
    QAction *refreshAction = new QAction(tr("Refresh"), tree);
    metaDataAction = new QAction(tr("Show Schema"), tree);
    connect(refreshAction, &QAction::triggered, this, &ConnectionWidget::refresh);
    connect(metaDataAction, &QAction::triggered, this, &ConnectionWidget::showMetaData);
    tree->addAction(refreshAction);
    tree->addAction(metaDataAction);
    tree->setContextMenuPolicy(Qt::ActionsContextMenu);

    layout->addWidget(tree);

    QMetaObject::connectSlotsByName(this);
}

ConnectionWidget::~ConnectionWidget()
{
}

static QString qDBCaption(const QSqlDatabase &db)
{
//    QString nm = db.driverName();
    QString nm = "";
//    nm.append(QLatin1Char(':'));
    if (!db.userName().isEmpty())
        nm.append(db.userName()).append(QLatin1Char('@'));
    nm.append(db.databaseName());
    return nm;
}

void ConnectionWidget::refresh()
{
    int songsCnt(0), albumsCnt(0), artistsCnt(0), playlistsCnt(0), usrsCnt(0);
    tree->clear();
    QStringList connectionNames = QSqlDatabase::connectionNames();

    bool gotActiveDb = false;
    for (int i = 0; i < connectionNames.count(); ++i) {
        QTreeWidgetItem *root = new QTreeWidgetItem(tree);
        QSqlDatabase db = QSqlDatabase::database(connectionNames.at(i), false);
        QSqlQuery query(db);
        root->setText(0, qDBCaption(db));
        if (connectionNames.at(i) == activeDb) {
            gotActiveDb = true;
            setActive(root);
        }
        if (db.isOpen()) {
            QStringList tables = db.tables();


            for (int t = 0; t < tables.count(); ++t) {
                QTreeWidgetItem *table = new QTreeWidgetItem(root);
                table->setText(0, tables.at(t));          


                if (tables.at(t) == "songs") {
                    query.exec("SELECT * FROM SONGS");
                    while (query.next()) songsCnt++;
                    qDebug() << "songsCnt = " << songsCnt << "\n";
                }
                if (tables.at(t) == "albums") {
                    query.exec("SELECT * FROM ALBUMS");
                    while (query.next()) albumsCnt++;
                    qDebug() << "albumsCnt = " << albumsCnt << "\n";
                }
                if (tables.at(t) == "artists") {
                    query.exec("SELECT * FROM ARTISTS");
                    while (query.next())artistsCnt++;
                    qDebug() << "artistsCnt = " << artistsCnt << "\n";
                }
                if (tables.at(t) == "playlists") {
                    query.exec("SELECT * FROM PLAYLISTS");
                    while (query.next())playlistsCnt++;
                    qDebug() << "playlistsCnt = " << playlistsCnt << "\n";
                }
                if (tables.at(t) == "usrs") {
                    query.exec("SELECT * FROM USRS");
                    while (query.next())usrsCnt++;
                    qDebug() << "usrsCnt = " << usrsCnt << "\n";
                }

            }
        }
    }


    info.sprintf("当前服务器拥有\n歌曲数目：%d\n专辑数目：%d\n艺人数目：%d\n歌单数目：%d\n用户数目：%d\n",
                 songsCnt, albumsCnt, artistsCnt, playlistsCnt, usrsCnt);

    if (!gotActiveDb) {
        activeDb = connectionNames.value(0);
        setActive(tree->topLevelItem(0));
    }

    tree->doItemsLayout(); // HACK
}
QString ConnectionWidget::getInfo() const
{
    return info;
}

QSqlDatabase ConnectionWidget::currentDatabase() const
{
    return QSqlDatabase::database(activeDb);
}

static void qSetBold(QTreeWidgetItem *item, bool bold)
{
    QFont font = item->font(0);
    font.setBold(bold);
    item->setFont(0, font);
}

void ConnectionWidget::setActive(QTreeWidgetItem *item)
{
    for (int i = 0; i < tree->topLevelItemCount(); ++i) {
        if (tree->topLevelItem(i)->font(0).bold())
            qSetBold(tree->topLevelItem(i), false);
    }

    if (!item)
        return;

    qSetBold(item, true);
    activeDb = QSqlDatabase::connectionNames().value(tree->indexOfTopLevelItem(item));
}

void ConnectionWidget::on_tree_itemActivated(QTreeWidgetItem *item, int /* column */)
{
    if (!item)
        return;

    if (!item->parent()) {
        setActive(item);
    } else {
        setActive(item->parent());
        emit tableActivated(item->text(0));
    }
}

void ConnectionWidget::showMetaData()
{
    QTreeWidgetItem *cItem = tree->currentItem();
    if (!cItem || !cItem->parent())
        return;
    setActive(cItem->parent());
    emit metaDataRequested(cItem->text(0));
}

void ConnectionWidget::on_tree_currentItemChanged(QTreeWidgetItem *current, QTreeWidgetItem *)
{
    metaDataAction->setEnabled(current && current->parent());
}
