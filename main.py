#!/usr/bin/python2.7
import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory, QTabWidget

from widget import technics


def main():
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))

    technics_tab = technics.Widget()
    
    tabs = QTabWidget()
    tabs.addTab(technics_tab, "Technics")

    tabs.setGeometry(450, 100, 400, 650)
    tabs.setWindowTitle('Office Equipment')
    tabs.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
