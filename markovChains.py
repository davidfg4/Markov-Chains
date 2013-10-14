#!/usr/bin/env python3.3

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
    conn.close()

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
