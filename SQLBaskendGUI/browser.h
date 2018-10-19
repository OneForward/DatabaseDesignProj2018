
#ifndef BROWSER_H
#define BROWSER_H

#include <QWidget>
#include <QSqlTableModel>
#include <QMessageBox>
#include "ui_browserwidget.h"

class ConnectionWidget;
QT_FORWARD_DECLARE_CLASS(QTableView)
QT_FORWARD_DECLARE_CLASS(QPushButton)
QT_FORWARD_DECLARE_CLASS(QTextEdit)
QT_FORWARD_DECLARE_CLASS(QSqlError)

class Browser: public QWidget, private Ui::Browser
{
    Q_OBJECT
public:
    Browser(QWidget *parent = nullptr);
    virtual ~Browser();

    QSqlError addConnection(const QString &driver, const QString &dbName, const QString &host,
                  const QString &user, const QString &passwd, int port = -1);

    void insertRow();
    void deleteRow();
    void updateActions();

    QString currentTableName;
    QSqlTableModel* sqltbmodel;
    QSqlTableModel* alSongsModel;
    QImage* imageAlbum;
    QImage* imageArtist;
    QSqlDatabase db;

public slots:
    void exec();
    void showTable(const QString &table);
    void showMetaData(const QString &table);
    void addConnection();
    void currentChanged() { updateActions(); }
    void about();

    void on_insertRowAction_triggered()
    { insertRow(); }
    void on_deleteRowAction_triggered()
    { deleteRow(); }
    void on_fieldStrategyAction_triggered();
    void on_rowStrategyAction_triggered();
    void on_manualStrategyAction_triggered();
    void on_submitAction_triggered();
    void on_revertAction_triggered();
    void on_selectAction_triggered();
    void on_connectionWidget_tableActivated(const QString &table)
    { showTable(table); }
    void on_connectionWidget_metaDataRequested(const QString &table)
    { showMetaData(table); }
    void on_submitButton_clicked()
    {
        exec();
        lineEditSearch->setFocus();
    }
    void on_clearButton_clicked()
    {
        sqltbmodel->select();
        updateActions();
        lineEditSearch->clear();
        lineEditSearch->setFocus();
//        sqlEdit->clear();
//        sqlEdit->setFocus();
    }

signals:
    void statusMessage(const QString &message);
private slots:
    void on_search_clicked();
    void on_lineEditSearch_returnPressed();

    void on_arUpload_clicked();
    void on_alUpload_clicked();
    void on_arCommitButton_clicked();
    void on_alCommitButton_clicked();

    void on_addSong_clicked();
    void on_removeSong_clicked();
};

class CustomModel: public QSqlTableModel
{
    Q_OBJECT
public:
    explicit CustomModel(QObject *parent = nullptr, QSqlDatabase db = QSqlDatabase())
        : QSqlTableModel(parent, db) {}

    QVariant data(const QModelIndex &idx, int role) const override
    {
        if (role == Qt::BackgroundRole && isDirty(idx))
            return QBrush(QColor(Qt::yellow));
        return QSqlTableModel::data(idx, role);
    }
};

#endif
