Markov-Chains
=============

Requirements
------------
A webserver that can execute python as a cgi script.
In apache this probably involves using "Options +ExecCGI" in either a .htaccess
file, or the main site config file in a <Directory> section.

Python 3.3

PyMYSQL - https://github.com/PyMySQL/PyMySQL/

py-bcrypt 0.4 - http://www.mindrot.org/projects/py-bcrypt/
This might exist in you package manager as python3-bcrypt.
If installing from source, might need this version instead: https://github.com/wcdolphin/python-bcrypt

A MySQL database is required, here are the basics of setting up a user and database:
```
mysql> CREATE DATABASE markov;
mysql> CREATE USER 'markov'@'localhost' IDENTIFIED BY '';
mysql> grant all privileges on markov.* to markov@localhost ;
```

Put the host, database, username, and password for mysql in markovChains.cfg.

Architecture
------------
markovChains.py contains all the common functions shared between the pages.
Other python files are specific pages, and primarily contain display code, not
data manipulation code.
