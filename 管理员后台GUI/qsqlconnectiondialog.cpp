#include "qsqlconnectiondialog.h"
#include "ui_qsqlconnectiondialog.h"

#include <QSqlDatabase>

QSqlConnectionDialog::QSqlConnectionDialog(QWidget *parent)
    : QDialog(parent)
{
    ui.setupUi(this);

    QStringList drivers = QSqlDatabase::drivers();

    // remove compat names
    drivers.removeAll("QMYSQL3");
    drivers.removeAll("QOCI8");
    drivers.removeAll("QODBC3");
    drivers.removeAll("QPSQL7");
    drivers.removeAll("QTDS7");

//    if (!drivers.contains("QSQLITE"))
//        ui.dbCheckBox->setEnabled(false);

//    ui.comboDriver->addItems(drivers);

}

QSqlConnectionDialog::~QSqlConnectionDialog()
{
}

QString QSqlConnectionDialog::driverName() const
{
    return "QMYSQL3";
}

QString QSqlConnectionDialog::databaseName() const
{
    return "music";
}

QString QSqlConnectionDialog::userName() const
{
    return ui.editUsername->text();
}

QString QSqlConnectionDialog::password() const
{
    return ui.editPassword->text();
}

QString QSqlConnectionDialog::hostName() const
{
    return ui.editHostname->text();
}

int QSqlConnectionDialog::port() const
{
    return ui.portSpinBox->value();
}

bool QSqlConnectionDialog::useInMemoryDatabase() const
{
    return false;
//    return ui.dbCheckBox->isChecked();
}

void QSqlConnectionDialog::on_okButton_clicked()
{

    accept();

}
