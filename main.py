#!/usr/bin/python2.7

import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory, QTabWidget

from widget import technics, departments, rooms, employees, \
    transfers, technicsView, roomsView, responsibleView


def main():
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    technics_tab = technics.Widget()
    departments_tab = departments.Widget()
    rooms_tab = rooms.Widget()
    employees_tab = employees.Widget()
    transfers_tab = transfers.Widget()
    technicsView_tab = technicsView.Widget()
    roomsView_tab = roomsView.Widget()
    responsibleView_tab = responsibleView.Widget()
    
    tabs = QTabWidget()
    tabs.addTab(technics_tab, 'Technics')
    tabs.addTab(departments_tab, 'Departments')
    tabs.addTab(rooms_tab, 'Rooms')
    tabs.addTab(employees_tab, 'Employees')
    tabs.addTab(transfers_tab, 'Transers')
    tabs.addTab(technicsView_tab, 'Technics View')
    tabs.addTab(roomsView_tab, 'Rooms View')
    tabs.addTab(responsibleView_tab, 'Responsible View')

    tabs.setFixedWidth(750)
    tabs.setFixedHeight(600)
    tabs.setWindowTitle('Office Equipment')
    tabs.show()
    tabs.currentChanged.connect(lambda x: tabs.currentWidget().refresh())

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
