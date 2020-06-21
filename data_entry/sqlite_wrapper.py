#!/usr/bin/env python3

"""
sqlite_wrapper.py: Component to wrap SQLite3 commands for the data entry tool.
"""

__author__      = "crazoter"
__copyright__   = "Copyright 2020"
__license__     = "GPL"
__version__     = "1.0.0"
__status__      = "Development"

import os
import sqlite3
import calendar
import time

from schema import *

class SqliteWrapper:
    def __init__(self, schema, database_path, backup_path=None):
        self.database_path = database_path
        self.backup_path = backup_path
        self.dbconn = None
        self.dbcur = None
        self.schema = schema

    # Helper functions
    def ensure_tablename(self, tablename):
        """Throw error if param is not a tablename"""
        if tablename not in self.schema:
            raise ValueError("tablename must be in self.schema")

    def ensure_is_column(self, tablename, column):
        """
        Throw error if param is not a tablename or column
        It's not that efficient though O(n) to traverse array
        """
        if tablename not in self.schema or column not in self.schema[tablename]:
            raise ValueError("column must be in tablename")

    # SQLite3 database
    def connect(self):
        """connect to the kaguya_data.db database

        @param database_path: path to database to manipulate
        @param backup_path: If set, writes a backup to the path in the name 'backup{timestamp}.db.
        """
        assert os.path.exists(self.database_path)
        self.dbconn = sqlite3.connect(self.database_path)
        if self.backup_path:
            # Perform a backup in case something happens
            self.backup_path = os.path.join(self.backup_path, 'backup' + str(calendar.timegm(time.gmtime())) + '.db')
            bck = sqlite3.connect(self.backup_path)
            self.dbconn.backup(bck)
            bck.close()
        # Make sure we get results in a nice format
        # See https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
        self.dbconn.row_factory = sqlite3.Row
        self.dbcur = self.dbconn.cursor()

    def close(self):
        """close the connection to the kaguya_data.db database"""
        self.dbcur = None
        self.dbconn.close()

    # Tables
    def insert_one(self, tablename, obj_schema, obj):
        """Insert an object into the database.
        Note that the ordering of data in the object is expecteed to be the  same as the ordering of data
        in the obj_schema, and of equal length
        
        @param tablename: table name in string format
        @param obj_schema: Columns for the object (from self.schema) in array format
        @param obj: array or tuple to be inserted
        """
        # Sanity checks
        assert len(obj) == len(obj_schema)
        self.ensure_tablename(tablename)

        query = "insert into " + tablename + " ("
        for key in obj_schema:
            self.ensure_is_column(tablename, key)
            query += key[0] + ","
        query = query[:-1] + ") values (?"
        query += ",?" * (len(obj)  - 1)
        query += ")"
        self.dbcur.execute(query, tuple(obj))
        self.dbconn.commit()

    def get_all(self, tablename):
        """Get all data from a table
        
        @param tablename: table name in string format
        @return array of sqlite3.Rows. See https://docs.python.org/3/library/sqlite3.html#row-objects
        """
        self.ensure_tablename(tablename)
        self.dbcur.execute('SELECT * FROM ' + tablename)
        return self.dbcur.fetchall()

    def get_with_cond_equal(self, tablename, var_val_map={}):
        """Get all data from a table with condition equal
        UNTESTED
        @param tablename: table name in string format
        @param var_val_map: dictionary of variables to be equal to values. This should not be empty.
        @return array of sqlite3.Rows. See https://docs.python.org/3/library/sqlite3.html#row-objects
        """
        # Sanity- Sanitization checks
        self.ensure_tablename(tablename)
        query = 'SELECT * FROM ' + tablename + ' WHERE '
        for var in var_val_map:
            self.ensure_is_column(tablename, var)
            query += var + '=? AND '
        query = query[:-4]
        self.dbcur.execute(query, tuple(var_val_map.values()))
        return self.dbcur.fetchall()

    def delete(self, tablename, obj_schema, obj):
        """Delete object(s) from the database.
        Note that the ordering of data in the object is expecteed to be the same as the ordering of data
        in the obj_schema, and of equal length
        
        @param tablename: table name in string format
        @param obj_schema: Columns for the object (from self.schema) in array format
        @param obj: array or tuple to be deleted
        """
        # Sanity- Sanitization checks
        assert len(obj) == len(obj_schema)
        self.ensure_tablename(tablename)

        query = "DELETE FROM " + tablename + " WHERE "
        for key in obj_schema:
            self.ensure_is_column(tablename, key)
            query += key[0] + "=? AND "
        query = query[:-4]
        self.dbcur.execute(query, tuple(obj))
        self.dbconn.commit()


# This serves as a rudimentary testcase
if __name__ == '__main__':
    # Constants
    # Get absolute path to data directory
    data_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/"))
    # Get path to kaguya_data.db
    db_path = os.path.join(data_dir, "kaguya_data.db")
    # Get path to backup directory
    backup_path = os.path.join(data_dir, 'backup')

    sqlite_wrapper = SqliteWrapper(SCHEMA, db_path, backup_path)
    sqlite_wrapper.connect()
    sqlite_wrapper.insert_one(TBL_SERIES, SCHEMA[TBL_SERIES], ["test"])
    print(tuple(sqlite_wrapper.get_all(TBL_SERIES)[0]))
    sqlite_wrapper.delete(TBL_SERIES, SCHEMA[TBL_SERIES], tuple(sqlite_wrapper.get_all(TBL_SERIES)[0]))
    print(sqlite_wrapper.get_all(TBL_SERIES))
