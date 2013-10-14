#!/usr/bin/env python3.3

import bcrypt
import cgi
import configparser
import pymysql # https://github.com/PyMySQL/PyMySQL/
import sys

"""
markovChains.py
This file contains helper functions that are common to all pages of the webapp.
It should contain functions to do all database calls, and return only valid
python objects and data structures.
"""

# Global variables:
conn = None

# -----------------------------------------------------------------------------
# Begin HTML functions
# -----------------------------------------------------------------------------

def printHeader():
    print("""Content-Type: text/html

<!doctype html>
<html>
<head>
<title></title>
</head>
<body>
<div id="main">""")

def printFooter():
    print("""</div>
</body>""", end="")


# -----------------------------------------------------------------------------
# End HTML functions
# -----------------------------------------------------------------------------
# Begin database functions
# -----------------------------------------------------------------------------

# Increment this number whenever the schema is changed, and databases will
# automatically remake themselves. (Warning: existing data will be deleted.)
db_version = 5

def initdb():
    global conn
    config = configparser.ConfigParser()
    config.read("markovChains.cfg")
    host = config['db']['host']
    database = config['db']['database']
    username = config['db']['username']
    password = config['db']['password']
    conn = pymysql.connect(host=host,
        user=username,
        passwd=password,
        db=database)
    c = conn.cursor()
    try:
        c.execute ("SELECT value FROM info WHERE `key` = 'db_version'")
        r = int(c.fetchall()[0][0])
        if r < db_version:
            #print("DB is old, remaking")
            create_db()
        elif r > db_version:
            #print("DB is newer than code, aborting")
            sys.exit(1)
    except pymysql.err.ProgrammingError:
        create_db()

def create_db():
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS info")
    c.execute("CREATE TABLE info (`key` VARCHAR(255) PRIMARY KEY, value TEXT)")
    c.execute("INSERT INTO info VALUES ('db_version', %s)", (db_version, ))
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (username VARCHAR(255) PRIMARY KEY, password TEXT)")
    # blank password
    c.execute("INSERT INTO users VALUES ('test', '$2a$12$6J4OyHUwI4Z8xAqslIpxLeFnQmuGkf700V7Rm9kMGpmMeW2VXHJkK')")
    conn.commit()
    c.close()
    
def check_credentials(user, password):
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = %s", (user, ))
    r = c.fetchone()
    c.close()
    if r == None:
        # user does not exist
        return False
    hashed = r[0]
    if bcrypt.hashpw(password, hashed) == hashed:
        # user exists, password is good
        return True
    else:
        # user exists, password is bad
        return False

def create_user(user, password):
    c = conn.cursor()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(12))
    c.execute("DELETE FROM users WHERE username = %s", (user, ))
    c.execute("INSERT INTO users VALUES (%s, %s)", (user, hashed))
    conn.commit()
    c.close()

# -----------------------------------------------------------------------------
# End database functions
# -----------------------------------------------------------------------------

def init():
    initdb()

if __name__ == "__main__":
    print("Error: This file should not be run on its own, only included")
    sys.exit(1)
else:
    init()
