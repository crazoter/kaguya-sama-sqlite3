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

# Constants
# Get absolute path to kaguya_data.db
KAGUYA_DATA_DIR = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 
        "../data/"))
KAGUYA_DATA_DB_PATH = os.path.join(KAGUYA_DATA_DIR, "kaguya_data.db")

dbconn = None
dbcur = None

# Helper functions
def ensure_tablename(tablename):
    """Throw error if param is not a tablename"""
    if tablename not in SCHEMA:
        raise ValueError("tablename must be in SCHEMA")

def ensure_is_column(tablename, column):
    """
    Throw error if param is not a tablename or column
    It's not that efficient though O(n) to traverse array
    """
    if tablename not in SCHEMA or column not in SCHEMA[tablename]:
        raise ValueError("column must be in tablename")

# SQLite3 database
def connect(backup=True):
    """connect to the kaguya_data.db database

    @param backup: perform a backup to 'backup{timestamp}.db. Done by default
    """
    global dbconn, dbcur
    assert os.path.exists(KAGUYA_DATA_DB_PATH)
    dbconn = sqlite3.connect(KAGUYA_DATA_DB_PATH)
    if backup:
        # Perform a backup in case something happens
        backup_path = os.path.join(KAGUYA_DATA_DIR, 'backup')
        backup_path = os.path.join(backup_path, 'backup' + str(calendar.timegm(time.gmtime())) + '.db')
        bck = sqlite3.connect(backup_path)
        dbconn.backup(bck)
        bck.close()
    # Make sure we get results in a nice format
    # See https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
    dbconn.row_factory = sqlite3.Row
    dbcur = dbconn.cursor()

def close():
    """close the connection to the kaguya_data.db database"""
    global dbconn, dbcur
    dbcur = None
    dbconn.close()

# Tables
def insert_one(tablename, obj_schema, obj):
    """Insert an object into the database.
    Note that the ordering of data in the object is expecteed to be the  same as the ordering of data
    in the obj_schema, and of equal length
    
    @param tablename: table name in string format
    @param obj_schema: Columns for the object (from SCHEMA) in array format
    @param obj: array or tuple to be inserted
    """
    global dbconn, dbcur
    # Sanity checks
    assert len(obj) == len(obj_schema)
    ensure_tablename(tablename)

    query = "insert into " + tablename + " ("
    for key in obj_schema:
        ensure_is_column(tablename, key)
        query += key + ","
    query = query[:-1] + ") values (?"
    query += ",?" * (len(obj)  - 1)
    query += ")"
    dbcur.execute(query, tuple(obj))
    dbconn.commit()

def get_all(tablename):
    """Get all data from a table
    
    @param tablename: table name in string format
    @return array of sqlite3.Rows. See https://docs.python.org/3/library/sqlite3.html#row-objects
    """
    global dbconn, dbcur
    ensure_tablename(tablename)
    dbcur.execute('SELECT * FROM ' + tablename)
    return dbcur.fetchall()

def get_with_cond_equal(tablename, var_val_map={}):
    """Get all data from a table with condition equal
    
    @param tablename: table name in string format
    @param var_val_map: dictionary of variables to be equal to values. This should not be empty.
    @return array of sqlite3.Rows. See https://docs.python.org/3/library/sqlite3.html#row-objects
    """
    global dbconn, dbcur
    # Sanity- Sanitization checks
    ensure_tablename(tablename)
    query = 'SELECT * FROM ' + tablename + ' WHERE '
    for var in var_val_map:
        ensure_is_column(tablename, var)
        query += var + '=? AND '
    query = query[:-4]
    dbcur.execute(query, tuple(var_val_map.values()))
    return dbcur.fetchall()

def delete(tablename, obj_schema, obj):
    """Delete object(s) from the database.
    Note that the ordering of data in the object is expecteed to be the same as the ordering of data
    in the obj_schema, and of equal length
    
    @param tablename: table name in string format
    @param obj_schema: Columns for the object (from SCHEMA) in array format
    @param obj: array or tuple to be deleted
    """
    global dbconn, dbcur
    # Sanity- Sanitization checks
    assert len(obj) == len(obj_schema)
    ensure_tablename(tablename)

    query = "DELETE FROM " + tablename + " WHERE "
    for key in obj_schema:
        ensure_is_column(tablename, key)
        query += key + "=? AND "
    query = query[:-4]
    dbcur.execute(query, tuple(obj))
    dbconn.commit()


# Rudimentary Tests
if __name__ == '__main__':
    connect()
    insert_one(TABLENAME_SERIES, SCHEMA[TABLENAME_SERIES], ["test"])
    print(tuple(get_all(TABLENAME_SERIES)[0]))
    delete(TABLENAME_SERIES, SCHEMA[TABLENAME_SERIES], tuple(get_all(TABLENAME_SERIES)[0]))
    print(get_all(TABLENAME_SERIES))