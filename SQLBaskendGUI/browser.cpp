#include "browser.h"
#include "qsqlconnectiondialog.h"

#include <QtWidgets>
#include <QtSql>

Browser::Browser(QWidget *parent)
    : QWidget(parent)
{
    setupUi(this);

    table->addAction(insertRowAction);
    table->addAction(deleteRowAction);
    table->addAction(fieldStrategyAction);
    table->addAction(rowStrategyAction);
    table->addAction(manualStrategyAction);
    table->addAction(submitAction);
    table->addAction(revertAction);
    table->addAction(selectAction);

    textBrowser->setText(connectionWidget->getInfo());
    dateEdit->setCalendarPopup(true);
    dateEdit->setDate(QDate::currentDate());
    currentTableName = "";

    imageAlbum = new QImage();
    imageArtist = new QImage();
    if (QSqlDatabase::drivers().isEmpty())
        QMessageBox::information(this, tr("No database drivers found"),
                                 tr("No database drivers found"));

    emit statusMessage(tr("Ready."));


}

Browser::~Browser()
{
}

void Browser::exec()
{
    QMessageBox msgBox(QMessageBox::Warning, tr("警告!"), "警告!<br>是否确认提交修改!", 0, this);
    msgBox.addButton(tr("确认提交"), QMessageBox::AcceptRole);
    QPushButton *cancel = msgBox.addButton(tr("取消"), QMessageBox::RejectRole);
    msgBox.setDefaultButton(cancel);
    if (msgBox.exec() == QMessageBox::AcceptRole)
    {
        sqltbmodel->submitAll();
    }

    updateActions();
}

QSqlError Browser::addConnection(const QString &driver, const QString &dbName, const QString &host,
                            const QString &user, const QString &passwd, int port)
{
    static int cCount = 0;

    QSqlError err;
    db = QSqlDatabase::addDatabase(driver, QString("Browser%1").arg(++cCount));
    db.setDatabaseName(dbName);
    db.setHostName(host);
    db.setPort(port);
    if (!db.open(user, passwd)) {
        err = db.lastError();
        db = QSqlDatabase();
        QSqlDatabase::removeDatabase(QString("Browser%1").arg(cCount));
    }
    connectionWidget->refresh();


    QSqlQueryModel *model = new QSqlQueryModel(alSongsTable);
    QSqlQuery query(db);
    query.exec("DELETE FROM cache_songs");
    model->setQuery(query);
    alSongsModel = new QSqlTableModel(alSongsTable, db);
    alSongsModel->setTable("cache_songs");
    alSongsModel->setEditStrategy(QSqlTableModel::OnManualSubmit);
    alSongsTable->setModel(alSongsModel);

    return err;
}

void Browser::addConnection()
{
    QSqlConnectionDialog dialog(this);
    if (dialog.exec() != QDialog::Accepted)
        return;

    QSqlError err = addConnection(dialog.driverName(), dialog.databaseName(), dialog.hostName(),
                       dialog.userName(), dialog.password(), dialog.port());
    if (err.type() != QSqlError::NoError)
        QMessageBox::warning(this, tr("Unable to open database"), tr("An error occurred while "
                                "opening the connection: ") + err.text());

}

void Browser::showTable(const QString &t)
{
    sqltbmodel = new CustomModel(table, connectionWidget->currentDatabase());
    sqltbmodel->setEditStrategy(QSqlTableModel::OnManualSubmit);
    sqltbmodel->setTable(connectionWidget->currentDatabase().driver()->escapeIdentifier(t, QSqlDriver::TableName));
    currentTableName = connectionWidget->currentDatabase().driver()->escapeIdentifier(t, QSqlDriver::TableName);
    currentTableName = currentTableName.mid(1, currentTableName.length()-3);
    qDebug() << "currentTableName = " << currentTableName << "\n";

    sqltbmodel->select();
    if (sqltbmodel->lastError().type() != QSqlError::NoError)
        emit statusMessage(sqltbmodel->lastError().text());

    table->setModel(sqltbmodel);
//    table->setEditTriggers(QAbstractItemView::DoubleClicked|QAbstractItemView::EditKeyPressed);
//    connect(table->selectionModel(), &QItemSelectionModel::currentRowChanged,
//            this, &Browser::currentChanged);

    updateActions();
}

void Browser::showMetaData(const QString &t)
{
    QSqlRecord rec = connectionWidget->currentDatabase().record(t);
    QStandardItemModel *model = new QStandardItemModel(table);

    model->insertRows(0, rec.count());
    model->insertColumns(0, 7);

    model->setHeaderData(0, Qt::Horizontal, "Fieldname");
    model->setHeaderData(1, Qt::Horizontal, "Type");
    model->setHeaderData(2, Qt::Horizontal, "Length");
    model->setHeaderData(3, Qt::Horizontal, "Precision");
    model->setHeaderData(4, Qt::Horizontal, "Required");
    model->setHeaderData(5, Qt::Horizontal, "AutoValue");
    model->setHeaderData(6, Qt::Horizontal, "DefaultValue");

    for (int i = 0; i < rec.count(); ++i) {
        QSqlField fld = rec.field(i);
        model->setData(model->index(i, 0), fld.name());
        model->setData(model->index(i, 1), fld.typeID() == -1
                ? QString(QMetaType::typeName(fld.type()))
                : QString("%1 (%2)").arg(QMetaType::typeName(fld.type())).arg(fld.typeID()));
        model->setData(model->index(i, 2), fld.length());
        model->setData(model->index(i, 3), fld.precision());
        model->setData(model->index(i, 4), fld.requiredStatus() == -1 ? QVariant("?")
                : QVariant(bool(fld.requiredStatus())));
        model->setData(model->index(i, 5), fld.isAutoValue());
        model->setData(model->index(i, 6), fld.defaultValue());
    }

    table->setModel(model);
    table->setEditTriggers(QAbstractItemView::NoEditTriggers);
    updateActions();

    delete model;

    rec = connectionWidget->currentDatabase().record("cache_songs");
    model = new QStandardItemModel(alSongsTable);

    model->insertRows(0, rec.count());
    model->insertColumns(0, 7);

    model->setHeaderData(0, Qt::Horizontal, "Fieldname");
    model->setHeaderData(1, Qt::Horizontal, "Type");
    model->setHeaderData(2, Qt::Horizontal, "Length");
    model->setHeaderData(3, Qt::Horizontal, "Precision");
    model->setHeaderData(4, Qt::Horizontal, "Required");
    model->setHeaderData(5, Qt::Horizontal, "AutoValue");
    model->setHeaderData(6, Qt::Horizontal, "DefaultValue");

    for (int i = 0; i < rec.count(); ++i) {
        QSqlField fld = rec.field(i);
        model->setData(model->index(i, 0), fld.name());
        model->setData(model->index(i, 1), fld.typeID() == -1
                ? QString(QMetaType::typeName(fld.type()))
                : QString("%1 (%2)").arg(QMetaType::typeName(fld.type())).arg(fld.typeID()));
        model->setData(model->index(i, 2), fld.length());
        model->setData(model->index(i, 3), fld.precision());
        model->setData(model->index(i, 4), fld.requiredStatus() == -1 ? QVariant("?")
                : QVariant(bool(fld.requiredStatus())));
        model->setData(model->index(i, 5), fld.isAutoValue());
        model->setData(model->index(i, 6), fld.defaultValue());
    }

    alSongsTable->setModel(model);
    alSongsTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
}

void Browser::insertRow()
{
    QSqlTableModel *model = qobject_cast<QSqlTableModel *>(table->model());
    if (!model)
        return;

    QModelIndex insertIndex = table->currentIndex();
    int row = insertIndex.row() == -1 ? 0 : insertIndex.row();
    model->insertRow(row);
    insertIndex = model->index(row, 0);
    table->setCurrentIndex(insertIndex);
    table->edit(insertIndex);
}

void Browser::deleteRow()
{
    QSqlTableModel *model = qobject_cast<QSqlTableModel *>(table->model());
    if (!model)
        return;

    QModelIndexList currentSelection = table->selectionModel()->selectedIndexes();
    for (int i = 0; i < currentSelection.count(); ++i) {
        if (currentSelection.at(i).column() != 0)
            continue;
        model->removeRow(currentSelection.at(i).row());
    }

    updateActions();
}

void Browser::updateActions()
{
    QSqlTableModel * tm = qobject_cast<QSqlTableModel *>(table->model());
    bool enableIns = tm;
    bool enableDel = enableIns && table->currentIndex().isValid();

    insertRowAction->setEnabled(enableIns);
    deleteRowAction->setEnabled(enableDel);

    fieldStrategyAction->setEnabled(tm);
    rowStrategyAction->setEnabled(tm);
    manualStrategyAction->setEnabled(tm);
    submitAction->setEnabled(tm);
    revertAction->setEnabled(tm);
    selectAction->setEnabled(tm);

    if (tm) {
        QSqlTableModel::EditStrategy es = tm->editStrategy();
        fieldStrategyAction->setChecked(es == QSqlTableModel::OnFieldChange);
        rowStrategyAction->setChecked(es == QSqlTableModel::OnRowChange);
        manualStrategyAction->setChecked(es == QSqlTableModel::OnManualSubmit);
    }

    textBrowser->setText(connectionWidget->getInfo());
}

void Browser::about()
{
    QMessageBox::about(this, tr("About"), tr("模拟网易云数据库后台管理系统"));
}

void Browser::on_fieldStrategyAction_triggered()
{
    QSqlTableModel * tm = qobject_cast<QSqlTableModel *>(table->model());
    if (tm)
        tm->setEditStrategy(QSqlTableModel::OnFieldChange);
}

void Browser::on_rowStrategyAction_triggered()
{
    QSqlTableModel * tm = qobject_cast<QSqlTableModel *>(table->model());
    if (tm)
        tm->setEditStrategy(QSqlTableModel::OnRowChange);
}

void Browser::on_manualStrategyAction_triggered()
{
    QSqlTableModel * tm = qobject_cast<QSqlTableModel *>(table->model());
    if (tm)
        tm->setEditStrategy(QSqlTableModel::OnManualSubmit);
}

void Browser::on_submitAction_triggered()
{
    QSqlTableModel * tm = qobject_cast<QSqlTableModel *>(table->model());
    if (tm)
        tm->submitAll();
}

void Browser::on_revertAction_triggered()
{
    QSqlTableModel * tm = qobject_cast<QSqlTableModel *>(table->model());
    if (tm)
        tm->revertAll();
}

void Browser::on_selectAction_triggered()
{
    QSqlTableModel * tm = qobject_cast<QSqlTableModel *>(table->model());
    if (tm)
        tm->select();
}

void Browser::on_search_clicked()
{
//    QSqlTableModel *model = new CustomModel(table);
    QString keyword = lineEditSearch->text();
    QString str;
    if (keyword.isEmpty() or keyword.trimmed().isEmpty())
    {
        sqltbmodel->select();
        return;
    }

//        str = QString("SELECT * FROM %1s WHERE %1_id = %2 or %1_name = %2").arg(currentTableName).arg(keyword);
    str = QString("%1_id = %2 or %1_name = %2").arg(currentTableName).arg(keyword);
//    qDebug() << "kw = " << keyword << "\n";
//    qDebug() << str << "\n";
    sqltbmodel->setFilter(str);
//    model->setQuery(QSqlQuery(str, connectionWidget->currentDatabase()));
    table->setModel(sqltbmodel);

    if (sqltbmodel->lastError().type() != QSqlError::NoError)
        emit statusMessage(sqltbmodel->lastError().text());
    else if (sqltbmodel->query().isSelect())
        emit statusMessage(tr("Query OK."));
    else
        emit statusMessage(tr("Query OK, number of affected rows: %1").arg(
                           sqltbmodel->query().numRowsAffected()));

    updateActions();

}

void Browser::on_lineEditSearch_returnPressed()
{
    on_search_clicked();
}



void Browser::on_arUpload_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(
                    this, "open image file",
                    ".",
                    "Image files (*.bmp *.jpg *.pbm *.pgm *.png *.ppm *.xbm *.xpm);;All files (*.*)");
    if(fileName != "")
    {
        if(imageArtist->load(fileName))
        {
            QGraphicsScene *scene = new QGraphicsScene;
            scene->addPixmap(QPixmap::fromImage(*imageArtist));
            arGraphicsView->setScene(scene);
            arGraphicsView->resize(imageArtist->width() + 10, imageArtist->height() + 10);
            arGraphicsView->show();
        }
        else {
            QMessageBox::information(this,
                                     tr("打开图像失败"),
                                     tr("打开图像失败!"));
        }
    }

}

void Browser::on_alUpload_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(
                    this, "open image file",
                    ".",
                    "Image files (*.bmp *.jpg *.pbm *.pgm *.png *.ppm *.xbm *.xpm);;All files (*.*)");
    if(fileName != "")
    {
        if(imageAlbum->load(fileName))
        {
            QGraphicsScene *scene = new QGraphicsScene;
            scene->addPixmap(QPixmap::fromImage(*imageAlbum));
            alGraphicsView->setScene(scene);
            alGraphicsView->resize(imageAlbum->width() + 10, imageAlbum->height() + 10);
            alGraphicsView->show();
        }
        else {
            QMessageBox::information(this,
                                     tr("打开图像失败"),
                                     tr("打开图像失败!"));
        }
    }
}

void Browser::on_arCommitButton_clicked()
{
    QString artistName = arArtistName->text();
    if (artistName.isEmpty()) {
        QMessageBox::information(this,
                                 tr("警告"),
                                 tr("请输入艺人名字!"));
        return;
    }
    QString artistDesc = arDesc->toPlainText();
    QByteArray arr;
    QBuffer buffer(&arr);
    buffer.open(QIODevice::WriteOnly);
    imageArtist->save(&buffer, "PNG");

    QString str = QString("INSERT INTO recent_artists(artist_id, artist_name, artist_pic, briedDesc)"
                " VALUES(%1, %2, %3)").arg(0).arg(artistName).arg(artistDesc);
    qDebug() << str << "\n";

    QSqlQueryModel *model = new QSqlQueryModel(table);
    QSqlQuery query(db);
    query.prepare("INSERT INTO recent_artists(artist_id, artist_name, artist_pic, briefDesc)"
                  " VALUES(:id, :name, :pic, :desc)");
    query.bindValue(":id", 0);
    query.bindValue(":name", artistName);
    query.bindValue(":pic", arr);
    query.bindValue(":desc", artistDesc);
    query.exec();
    model->setQuery(query);

    table->setModel(model);

    if (model->lastError().type() != QSqlError::NoError)
        emit statusMessage(model->lastError().text());
    else if (model->query().isSelect())
        emit statusMessage(tr("Query OK."));
    else
        emit statusMessage(tr("Query OK, number of affected rows: %1").arg(
                           model->query().numRowsAffected()));

    updateActions();

}

void Browser::on_alCommitButton_clicked()
{
    QString albumName = albumNameEdit->text();
    if (albumName.isEmpty()) {
        QMessageBox::information(this,
                                 tr("警告"),
                                 tr("请输入专辑名字!"));
        return;
    }

    QString albumDesc = alDesc->toPlainText();
    QDate qdate = dateEdit->date();
    QString date = qdate.toString();
    QByteArray arr;
    QBuffer buffer(&arr);
    buffer.open(QIODevice::WriteOnly);
    imageAlbum->save(&buffer, "PNG");

    QString str = QString("INSERT INTO recent_albums(album_id, album_name, album_pic,"
                          "publish_time, description, company, type, sub_type, artist_name, songs_count)"
                " VALUES(%1, %2, %3, %4)").arg(0).arg(albumName).arg(albumDesc).arg(date);
    qDebug() << str << "\n";

    QSqlQueryModel *model = new QSqlQueryModel(table);
    QSqlQuery query(db);
    query.prepare("INSERT INTO recent_albums(album_id, album_name, album_pic,"
                  "publish_time, description, company, type, sub_type, artist_name, songs_count)"
                  " VALUES(:id, :name, :pic, :date, :desc, :company, :type, :subType, :arName, :cnt)");
    query.bindValue(":id", 0);
    query.bindValue(":name", albumName);
    query.bindValue(":pic", arr);
    query.bindValue(":date", date);
    query.bindValue(":desc", albumDesc);
    query.bindValue(":company", alCompany->text());
    query.bindValue(":type", alType->currentText());
    query.bindValue(":subType", alSubtype->currentText());
    query.bindValue(":arName", alArtistName->text());
    query.bindValue(":cnt", 0);
    query.exec();
    model->setQuery(query);

    table->setModel(model);

    if (model->lastError().type() != QSqlError::NoError)
        emit statusMessage(model->lastError().text());
    else if (model->query().isSelect())
        emit statusMessage(tr("Query OK."));
    else
    {

        emit statusMessage(tr("Query OK, number of affected rows: %1").arg(
                           model->query().numRowsAffected()));
        QMessageBox::information(this,
                                 tr("成功"),
                                 tr("已成功添加专辑:%1!").arg(albumName));
    }
    updateActions();

    delete model;
    model = new QSqlQueryModel(alSongsTable);
    query.exec("DELETE FROM cache_songs");
    model->setQuery(query);
    alSongsTable->setModel(model);
}


void Browser::on_addSong_clicked()
{
    alSongsModel->insertRecord(alSongsModel->rowCount(), alSongsModel->record());
    alSongsModel->submitAll();
    alSongsTable->setModel(alSongsModel);
    updateActions();
}

void Browser::on_removeSong_clicked()
{
    QItemSelectionModel* sModel = alSongsTable->selectionModel();
    QModelIndexList idxList = sModel->selectedRows();
    for (int i=0; i<idxList.size(); ++i) {
        alSongsModel->removeRow(idxList.at(i).row());
    }
    alSongsModel->submitAll();
    alSongsModel->select();
    alSongsTable->setModel(alSongsModel);
    updateActions();
}
