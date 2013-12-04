#!/usr/bin/env python3.3

import bcrypt
import cgi
import configparser
import http.cookies
import os
import pymysql # https://github.com/PyMySQL/PyMySQL/
import random
import string
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

def check_browser_cookie(require_login=True):
    cookie = []
    if "HTTP_COOKIE" in os.environ:
        cookie = http.cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    if "session" in cookie:
        user = check_cookie(cookie["session"].value)
        if user:
            return user
    if not require_login:
        return False
    redirect("index.py?error=nologin")
    sys.exit(0)

def printHeader():
    print("""Content-Type: text/html

<!doctype html>
<html>
<head>
<title>Markov Chains</title>
<link rel="stylesheet" type="text/css" href="cssreset.css" />
<link rel="stylesheet" type="text/css" href="stylesheet.css" />
</head>
<body>
<div id="main">
<center><h1>Markov Chains</h1><a href="user.py">User page</a></center>
<hr>
<br />
""")

def printFooter():
    print("""</div>
</body>""", end="")

def redirect(loc, headers=""):
    print("""Content-Type: text/html""")
    print(headers)
    print("""

<!doctype html>
<html>
<head>
<meta http-equiv="refresh" content="0; url=""" + loc + """">
</head>
<body>
<a href='""" + loc + """'> Please click here if you are not redirected.<a/>
</body>
</html>""")


# -----------------------------------------------------------------------------
# End HTML functions
# -----------------------------------------------------------------------------
# Begin database functions
# -----------------------------------------------------------------------------

# Increment this number whenever the schema is changed, and databases will
# automatically remake themselves. (Warning: existing data will be deleted.)
db_version = 19

def initdb():
    global conn
    config = configparser.ConfigParser()
    # Storing the cfg file in the web folder is not secure,
    # don't do this on a real install.
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
        c.execute("SELECT value FROM info WHERE `key` = 'db_version'")
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
    c.execute("""CREATE TABLE users
        (username VARCHAR(255) PRIMARY KEY,
        password TEXT,
        cookie TEXT,
        cookie_expire DATETIME)""")
    # blank password
    c.execute("INSERT INTO users VALUES ('test', '$2a$12$6J4OyHUwI4Z8xAqslIpxLeFnQmuGkf700V7Rm9kMGpmMeW2VXHJkK', '', NOW() + INTERVAL 1 DAY)")
    c.execute("DROP TABLE IF EXISTS blocks")
    c.execute("""CREATE TABLE blocks
        (id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        user VARCHAR(255),
        original_text LONGTEXT,
        source_url TEXT,
        FOREIGN KEY (user) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE)""")
    c.execute("DROP TABLE IF EXISTS chunks")
    c.execute("""CREATE TABLE chunks
        (block_id INT,
        context_length INT,
        context VARCHAR(25),
        next VARCHAR(25),
        INDEX (context),
        FOREIGN KEY (block_id) REFERENCES block(id) ON DELETE CASCADE ON UPDATE CASCADE)""")
    c.execute("DROP TABLE IF EXISTS generated_text")
    c.execute("""CREATE TABLE generated_text
        (block_id INT,
        date DATETIME,
        text LONGTEXT,
        FOREIGN KEY (block_id) REFERENCES block(id) ON DELETE CASCADE ON UPDATE CASCADE)""")
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
        session_id = randomCookie()
        cookie = http.cookies.SimpleCookie()
        cookie['session'] = session_id
        c = conn.cursor()
        c.execute("UPDATE users SET cookie = %s, cookie_expire = NOW() + INTERVAL 1 WEEK WHERE username = %s", (session_id, user))
        return cookie.output()
    else:
        # user exists, password is bad
        return False

def check_cookie(cookie):
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE cookie = %s AND cookie_expire > NOW()", (cookie, ))
    r = c.fetchone()
    c.close()
    if r == None:
        return False
    else:
        return r[0]

def create_user(user, password):
    c = conn.cursor()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(12))
    # c.execute("DELETE FROM users WHERE username = %s", (user, ))
    try:
        c.execute("INSERT INTO users VALUES (%s, %s, '', NOW())", (user, hashed))
    except pymysql.err.IntegrityError:
        # It's likely the user already exists
        return False
    finally:
        conn.commit()
        c.close()
    return True

def create_block(name, user, text, url=None):
    c = conn.cursor()
    c.execute("INSERT INTO blocks VALUES (null, %s, %s, %s, %s)", (name, user, text, url))
    c.execute("SELECT max(id) FROM blocks")
    id = c.fetchone()[0]
    if False:
        # This doesn't work for some reason :(
        for context_length in range(1, 11):
            for i in range(context_length, len(text)):
                try:
                    context = text[i-context_length:i]
                    string = str(text[i])
                    c.execute("INSERT INTO chunks VALUES (%s, %s, %s, %s)", (id, context_length, context, string))
                except:
                    pass
    words = text.split()
    for i in range(1, len(words)):
        try:
            context = words[i-1]
            string = words[i]
            c.execute("INSERT INTO chunks VALUES (%s, %s, %s, %s)", (id, 0, context, string))
        except:
            pass
    conn.commit()
    c.close()

def get_blocks(user, id=None):
    c = conn.cursor(pymysql.cursors.DictCursor)
    if id:
        c.execute("SELECT * FROM blocks WHERE user = %s AND id = %s", (user, id))
    else:
        c.execute("SELECT * FROM blocks WHERE user = %s", (user, ))
    blocks = c.fetchall()
    conn.commit()
    c.close()
    return blocks

def create_chain(id, context_length, length):
    context_length = int(context_length)
    c = conn.cursor(pymysql.cursors.DictCursor)
    text = ""
    if context_length == 0:
        text = "test"
        c.execute("SELECT * FROM chunks WHERE block_id = %s ORDER BY RAND() LIMIT 1", (id, ))
        context = c.fetchone()['next']
        text = context
        for i in range(length):
            c.execute("SELECT * FROM chunks WHERE block_id = %s AND context = %s", (id, context))
            words = c.fetchall()
            if len(words) < 1:
                c.execute("SELECT * FROM chunks WHERE block_id = %s ORDER BY RAND() LIMIT 1", (id, ))
                context = c.fetchone()['next']
            else:
                context = random.choice(words)['next']
            text += context + " "
    else:
        # TODO: implement
        for i in range(length):
            pass
    # TODO: add text to generated_text table
    conn.commit()
    c.close()
    return text.encode('ascii', 'ignore')[2:-1]

# -----------------------------------------------------------------------------
# End database functions
# -----------------------------------------------------------------------------

def randomCookie(length=40):
    return "".join(random.choice(string.ascii_uppercase +\
        string.ascii_lowercase + string.digits) for x in range(length))

def init():
    initdb()

if __name__ == "__main__":
    print("Error: This file should not be run on its own, only included")
    sys.exit(1)
else:
    init()
