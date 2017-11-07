#!/usr/bin/python2.7

import re
import MySQLdb as mysql

from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, \
    QPushButton, QMessageBox, QVBoxLayout, QDateEdit, QComboBox, QHBoxLayout

from DBConnection import Connection


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self._initUI()
        self.controller = _Controller(self)
        self.requireDepartments.emit()

    _requireDepartments = pyqtSignal(name='requireDepartments')
    _requireRooms = pyqtSignal(str, name='requireRooms')

    def refresh(self):
        self.requireDepartments.emit()
        self.idEdit.setFocus()

    def setDepartments(self, array):
        self.departmentCmb.clear()
        self.departmentCmb.addItems(array)
        self.requireRooms.emit(self.department)

    def setRooms(self, array):
        self.roomsCmb.clear()
        self.roomsCmb.addItems(array)

    def _initUI(self):
        self.idLabel = QLabel('Id')
        self.nameLabel = QLabel('Name')
        self.modelLabel = QLabel('Model')
        self.costLabel = QLabel('Cost')
        self.purchaseDateLabel = QLabel('Purchase date')
        self.departmentLabel = QLabel('Department')
        self.roomLabel = QLabel('Room')


        self.idEdit = QLineEdit()
        self.idEdit.setPlaceholderText('Use for editing/removing operations')
        self.nameEdit = QLineEdit()
        self.modelEdit = QLineEdit()
        self.costEdit = QLineEdit()
        self.purchaseDateEdit = QDateEdit()
        self.purchaseDateEdit.setDisplayFormat('dd.MM.yyyy')
        self.purchaseDateEdit.setCalendarPopup(True)
        self.purchaseDateEdit.setDate(QDate.currentDate())
        self.purchaseDateEdit.setMinimumDate(QDate(1900, 1, 1))
        self.purchaseDateEdit.setMaximumDate(QDate(2099, 31, 12))
        self.departmentCmb = QComboBox()
        self.roomsCmb = QComboBox()

        self.submitButton = QPushButton('Submit')
        self.editButton = QPushButton('Edit')
        self.removeButton = QPushButton('Remove')

        layout = QVBoxLayout()
        layout.addWidget(self.idLabel)
        layout.addWidget(self.idEdit)
        layout.addSpacing(20)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameEdit)
        layout.addSpacing(10)
        layout.addWidget(self.modelLabel)
        layout.addWidget(self.modelEdit)
        layout.addSpacing(10)
        layout.addWidget(self.costLabel)
        layout.addWidget(self.costEdit)
        layout.addSpacing(10)
        layout.addWidget(self.purchaseDateLabel)
        layout.addWidget(self.purchaseDateEdit)
        layout.addSpacing(10)
        layout.addWidget(self.departmentLabel)
        layout.addWidget(self.departmentCmb)
        layout.addSpacing(10)
        layout.addWidget(self.roomLabel)
        layout.addWidget(self.roomsCmb)
        layout.addStretch(2)
        layout.addWidget(self.submitButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.removeButton)

        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addLayout(layout)
        hlayout.addStretch()

        self.setLayout(hlayout)

    @property
    def id(self):
        return self.idEdit.text()

    @id.setter
    def id(self, value):
        self.idEdit.setText(value)

    @property
    def name(self):
        return self.nameEdit.text()

    @name.setter
    def name(self, value):
        self.nameEdit.setText(value)

    @property
    def model(self):
        return self.modelEdit.text()

    @model.setter
    def model(self, value):
        self.modelEdit.setText(value)

    @property
    def cost(self):
        return self.costEdit.text()

    @cost.setter
    def cost(self, value):
        self.costEdit.setText(value)

    @property
    def purchaseDate(self):
        return self.purchaseDateEdit.date().toPyDate()

    @property
    def department(self):
        return self.departmentCmb.currentText()

    @property
    def room(self):
        return self.roomsCmb.currentText()


class _Controller:
    def __init__(self, view):
        self._model = _Model()
        self._view = view
        self._setConnections()

    def _setConnections(self):
        self._view.submitButton.clicked.connect(self._processSubmission)
        self._view.editButton.clicked.connect(self._processEditing)
        self._view.removeButton.clicked.connect(self._processErasing)
        self._view.requireDepartments.connect(self._getDepartments)
        self._view.requireRooms.connect(self._getRooms)
        self._view.departmentCmb.activated.connect(self._getRooms)

    def _getDepartments(self):
        departments = sorted([x[0] for x in self._model.getDepartmentsShortNames()])
        self._view.setDepartments(departments)

    def _getRooms(self):
        rooms = sorted([x[0] for x in self._model.getRoomsNames(self._view.department)])
        self._view.setRooms(rooms)

    def _validate_id(self, id):
        if re.match('^[\d]{1,11}$', id):
            return True
        return False

    def _validate_name(self, name):
        if re.match('^[\w]{1,20}$', name):
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
        if re.match('^[\w\-.]{1,5}$', department):
            return True
        return False

    def _validate_room(self, room):
        if re.match('^[\w]{1,5}$', room):
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
                                               room=self._view.room)
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
                                             room=self._view.room)
                QMessageBox.information(None,
                                        'Information',
                                        'Successfully edited')
                self._view.id = ''
                self._view.name = ''
                self._view.model = ''
                self._view.cost = ''
                self._view.department = ''
                self._view.room = ''
            except mysql.Error:
                QMessageBox.information(None,
                                        'Information',
                                        'Could not edit successfully')
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


class _Model:
    def __init__(self):
        self.db = Connection()
        self.cursor = self.db.cursor

    def insertTechnicsItem(self, name, model, cost, purcase_date, department, room):
        try:
            self.cursor.execute(
                """
                SELECT room_id
                  FROM company_orgtechnics.Rooms r 
                  INNER JOIN company_orgtechnics.Departments d
                    ON r.department_id = d.department_id
                  WHERE d.short_name='{0}' AND r.name='{1}'
                """.format(department, room))
            room_id = self.cursor.fetchall()

            if len(room_id) == 0:
                raise mysql.Error()
            else:
                room_id = room_id[0][0]

            self.cursor.execute(
                """
                INSERT INTO company_orgtechnics.Computers 
                  (comp_name,model,cost,purchase_date,room_id) 
                  VALUES('{0}','{1}',{2},'{3}',{4})
                """.format(name, model, cost, purcase_date, room_id))
            self.db.commit()
        except mysql.Error as error:
            print "Error %d: %s" % (error.args[0], error.args[1])
            self.db.rollback()
            raise mysql.Error(error.args)

    def editTechnicsItem(self, id, name, model, cost, purcase_date, department, room):
        try:
            self.cursor.execute(
                """
                SELECT room_id
                  FROM company_orgtechnics.Rooms r 
                  INNER JOIN company_orgtechnics.Departments d
                    ON r.department_id = d.department_id
                  WHERE d.short_name='{0}' AND r.name='{1}'
                """.format(department, room))
            room_id = self.cursor.fetchall()

            if len(room_id) == 0:
                raise mysql.Error()
            else:
                room_id = room_id[0][0]

            self.cursor.execute(
                """
                UPDATE company_orgtechnics.Computers 
                SET comp_name='{1}',model='{2}',cost='{3}',purchase_date='{4}',room_id='{5}' 
                WHERE comp_id='{0}'
                """.format(id, name, model, cost, purcase_date, room_id))
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
                WHERE comp_id='{0}'
                """.format(id)
            )
            self.db.commit()
        except mysql.Error as error:
            print "Error %d: %s" % (error.args[0], error.args[1])
            self.db.rollback()
            raise mysql.Error(error.args)

    def getDepartmentsShortNames(self):
        try:
            self.cursor.execute(
                """
                SELECT DISTINCT short_name
                FROM company_orgtechnics.Departments
                """
            )
            return self.cursor.fetchall()
        except mysql.Error as error:
            print "Error %d: %s" % (error.args[0], error.args[1])
            self.db.rollback()
            return list()

    def getRoomsNames(self, department):
        try:
            self.cursor.execute(
                """
                SELECT DISTINCT name
                FROM company_orgtechnics.Rooms INNER JOIN company_orgtechnics.Departments
                  ON Rooms.department_id = Departments.department_id
                WHERE short_name='{0}'
                """.format(department)
            )
            return self.cursor.fetchall()
        except mysql.Error as error:
            print "Error %d: %s" % (error.args[0], error.args[1])
            self.db.rollback()
            raise mysql.Error(error.args)
