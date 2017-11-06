#!/usr/bin/python2.7
import MySQLdb as mysql
from settings import connection


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Connection:
    __metaclass__ = Singleton

    def __init__(self):
        try:
            self._connection = mysql.connect(host=connection['host'],
                                             user=connection['user'],
                                             passwd=connection['password'],
                                             db=connection['database'])
        except mysql.Error, error:
            print "Error %d: %s" % (error.args[0], error.args[1])

    def __del__(self):
        self._connection.close()

    @property
    def cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()

    def rollback(self):
        self._connection.rollback()
