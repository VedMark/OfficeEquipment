#!/usr/bin/python2.7
import sys
import re
import MySQLdb as mysql
from PyQt5.QtCore import QDate

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, \
    QPushButton, QMessageBox, QVBoxLayout, QDateEdit
from DBConnection import Connection


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self._initUI()
        self.controller = _Controller(self)

    def _initUI(self):
        self.__idLabel = QLabel('Id')
        self.__nameLabel = QLabel('Name')
        self.__modelLabel = QLabel('Model')
        self.__costLabel = QLabel('Cost')
        self.__purchaseDateLabel = QLabel('Purchase date')
        self.__departmentLabel = QLabel('Department')
        self.__roomLabel = QLabel('Room')
        self.__receiveDateLabel = QLabel('Receive date')

        self.__idEdit = QLineEdit()
        self.__idEdit.setPlaceholderText('Use for editing/removing operations')
        self.__nameEdit = QLineEdit()
        self.__modelEdit = QLineEdit()
        self.__costEdit = QLineEdit()
        self.__purchaseDate = QDateEdit()
        self.__purchaseDate.setDisplayFormat('dd.MM.yyyy')
        self.__purchaseDate.setCalendarPopup(True)
        self.__purchaseDate.setDate(QDate.currentDate())
        self.__purchaseDate.setMinimumDate(QDate(1900, 1, 1))
        self.__purchaseDate.setMaximumDate(QDate(2099, 31, 12))
        self.__departmentEdit = QLineEdit()
        self.__roomEdit = QLineEdit()
        self.__receiveDate = QDateEdit()
        self.__receiveDate.setDisplayFormat('dd.MM.yyyy')
        self.__receiveDate.setCalendarPopup(True)
        self.__receiveDate.setDate(QDate.currentDate())
        self.__receiveDate.setMinimumDate(QDate(1900, 1, 1))
        self.__receiveDate.setMaximumDate(QDate(2099, 31, 12))

        self.submitButton = QPushButton('Submit')
        self.editButton = QPushButton('Edit')
        self.removeButton = QPushButton('Remove')

        layout = QVBoxLayout()
        layout.addWidget(self.__idLabel)
        layout.addWidget(self.__idEdit)
        layout.addSpacing(20)
        layout.addWidget(self.__nameLabel)
        layout.addWidget(self.__nameEdit)
        layout.addSpacing(10)
        layout.addWidget(self.__modelLabel)
        layout.addWidget(self.__modelEdit)
        layout.addSpacing(10)
        layout.addWidget(self.__costLabel)
        layout.addWidget(self.__costEdit)
        layout.addSpacing(10)
        layout.addWidget(self.__purchaseDateLabel)
        layout.addWidget(self.__purchaseDate)
        layout.addSpacing(10)
        layout.addWidget(self.__departmentLabel)
        layout.addWidget(self.__departmentEdit)
        layout.addSpacing(10)
        layout.addWidget(self.__roomLabel)
        layout.addWidget(self.__roomEdit)
        layout.addSpacing(10)
        layout.addWidget(self.__receiveDateLabel)
        layout.addWidget(self.__receiveDate)
        layout.addStretch(2)
        layout.addWidget(self.submitButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.removeButton)

        self.setLayout(layout)
        self.__nameEdit.setFocus()

    @property
    def id(self):
        return self.__idEdit.text()

    @id.setter
    def id(self, value):
        self.__idEdit.setText(value)

    @property
    def name(self):
        return self.__nameEdit.text()

    @name.setter
    def name(self, value):
        self.__nameEdit.setText(value)

    @property
    def model(self):
        return self.__modelEdit.text()

    @model.setter
    def model(self, value):
        self.__modelEdit.setText(value)

    @property
    def cost(self):
        return self.__costEdit.text()

    @cost.setter
    def cost(self, value):
        self.__costEdit.setText(value)

    @property
    def purchaseDate(self):
        return self.__purchaseDate.date().toPyDate()

    @property
    def department(self):
        return self.__departmentEdit.text()

    @department.setter
    def department(self, value):
        self.__departmentEdit.setText(value)

    @property
    def room(self):
        return self.__roomEdit.text()

    @room.setter
    def room(self, value):
        self.__roomEdit.setText(value)

    @property
    def receiveDate(self):
        return self.__receiveDate.date().toPyDate()


class _Controller:
    def __init__(self, view):
        self._model = _Model()
        self._view = view
        self._setConnections()

    def _setConnections(self):
        self._view.submitButton.clicked.connect(self._processSubmission)
        self._view.editButton.clicked.connect(self._processEditing)
        self._view.removeButton.clicked.connect(self._processErasing)

    def _validate_id(self, id):
        if re.match('^[\d]{1,11}$', id):
            return True
        return False

    def _validate_name(self, name):
        if re.match('^[\w]{1,19}$', name):
            return True
        return False

    def _validate_model(self, model):
        if re.match('^[\w\-.]{1,20}$', model):
            return True
        return False

    def _validate_cost(self, cost):
        if re.match('^[\d]{0,11}$', cost):
            return True
        return False

    def _validate_department(self, department):
        if re.match('^[\w\-.]{0,5}$', department):
            return True
        return False

    def _validate_room(self, room):
        if re.match('^[\w]{0,5}$', room):
            return True
        return False

    def _processSubmission(self):
        if self._validate_name(self._view.name) and self._validate_model(self._view.model) and \
           self._validate_cost(self._view.cost) and self._validate_department(self._view.department) and \
           self._validate_room(self._view.room):
            try:
                self._model.insertTechnicsItem(name=self._view.name,
                                               model=self._view.model,
                                               cost=self._view.cost,
                                               purcase_date=self._view.purchaseDate,
                                               department=self._view.department,
                                               room=self._view.room,
                                               receive_date=self._view.receiveDate)
                QMessageBox.information(None,
                                        'Information',
                                        'Successfully inserted')
                self._view.name = ''
                self._view.model = ''
                self._view.cost = ''
                self._view.department = ''
                self._view.room = ''
            except mysql.Error:
                QMessageBox.information(None,
                                        'Information',
                                        'Could not save successfully')
            except ComputerLocationError as error:
                QMessageBox.information(None,
                                        'Information',
                                        error.message)
            except Exception: pass
        else:
            QMessageBox.information(None,
                                    'Information',
                                    'Something wrong with parameters')

    def _processEditing(self):
        if self._validate_id(self._view.id) and self._validate_name(self._view.name) and \
           self._validate_model(self._view.model) and self._validate_cost(self._view.cost) and \
           self._validate_department(self._view.department) and self._validate_room(self._view.room):
            try:
                self._model.editTechnicsItem(id=self._view.id,
                                             name=self._view.name,
                                             model=self._view.model,
                                             cost=self._view.cost,
                                             purcase_date=self._view.purchaseDate,
                                             department=self._view.department,
                                             room=self._view.room,
                                             receive_date=self._view.receiveDate)
                QMessageBox.information(None,
                                        'Information',
                                        'Successfully edited')
                self._view.id = ''
            except mysql.Error:
                QMessageBox.information(None,
                                        'Information',
                                        'Could not edit successfully')
            except ComputerLocationError as error:
                QMessageBox.information(None,
                                        'Information',
                                        error.message)
            except Exception: pass

        else:
            QMessageBox.information(None,
                                    'Information',
                                    'Something wrong with parameters')

    def _processErasing(self):
        if self._validate_id(self._view.id):
            try:
                self._model.deleteTechnicsItem(id=self._view.id)
                QMessageBox.information(None,
                                        'Information',
                                        'Successfully removed')
                self._view.id = ''
            except mysql.Error:
                QMessageBox.information(None,
                                        'Information',
                                        'Could not remove successfully')
            except Exception: pass
        else:
            QMessageBox.information(None,
                                    'Information',
                                    'Something wrong with parameters')

    def quitApp(self):
        sys.exit(1)


class _Model:
    def __init__(self):
        self.db = Connection()
        self.cursor = self.db.cursor

    def insertTechnicsItem(self, name, model, cost, purcase_date, department, room, receive_date):
        try:
            self.cursor.execute(
                """
                SELECT room_id
                  FROM company_orgtechnics.Rooms r 
                  INNER JOIN company_orgtechnics.Departments d
                    ON r.department_id = d.department_id
                  WHERE d.short_name = '{0}' AND r.name = '{1}'
                """.format(department, room))
            room_id = self.cursor.fetchall()

            if len(room_id) == 0:
                raise ComputerLocationError('Room ' + department + '-' + str(room) + ' does not exists')
            else:
                room_id = room_id[0][0]

            self.cursor.execute(
                """
                INSERT INTO company_orgtechnics.Computers 
                  (comp_name,model,cost,purchase_date,room_id,receive_date) 
                  VALUES('{0}','{1}',{2},'{3}',{4},'{5}')
                """.format(name, model, cost, purcase_date, room_id, receive_date))
            self.db.commit()
        except mysql.Error as error:
            print "Error %d: %s" % (error.args[0], error.args[1])
            self.db.rollback()
            raise mysql.Error(error.args)

    def editTechnicsItem(self, id, name, model, cost, purcase_date, department, room, receive_date):
        try:
            self.cursor.execute(
                """
                SELECT room_id
                  FROM company_orgtechnics.Rooms r 
                  INNER JOIN company_orgtechnics.Departments d
                    ON r.department_id = d.department_id
                  WHERE d.short_name = '{0}' AND r.name = '{1}'
                """.format(department, room))
            room_id = self.cursor.fetchall()

            if len(room_id) == 0:
                raise ComputerLocationError('Room ' + department + '-' + str(room) + ' does not exists')
            else:
                room_id = room_id[0][0]

            self.cursor.execute(
                """
                UPDATE company_orgtechnics.Computers 
                SET comp_name='{1}',model='{2}',cost='{3}',purchase_date='{4}',room_id='{5}',receive_date='{6}' 
                WHERE comp_id = '{0}'
                """.format(id, name, model, cost, purcase_date, room_id, receive_date))
            self.db.commit()
        except mysql.Error as error:
            print "Error %d: %s" % (error.args[0], error.args[1])
            self.db.rollback()
            raise mysql.Error(error.args)


    def deleteTechnicsItem(self, id):
        try:
            self.cursor.execute(
                """
                DELETE FROM company_orgtechnics.Computers
                WHERE comp_id = '{0}'
                """.format(id)
            )
            self.db.commit()
        except mysql.Error as error:
            print "Error %d: %s" % (error.args[0], error.args[1])
            self.db.rollback()
            raise mysql.Error(error.args)


class ComputerLocationError(Exception):
    def __init__(self, message):
        self.message = message
