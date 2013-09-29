Markov-Chains
=============

Requirements
------------
A webserver that can execute python as a cgi script.
In apache this probably involves using "Options +ExecCGI" in either a .htaccess
file, or the main site config file in a <Directory> section.

A sql server will be required at some point, but not yet.

Architecture
------------
markovChains.py contains all the common functions shared between the pages.
Other python files are specific pages, and primarily contain display code, not
data manipulation code.
