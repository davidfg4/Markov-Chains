import cgi
import sys

"""
markovChains.py
This file contains helper functions that are common to all pages of the webapp.
It should contain functions to do all database calls, and return only valid
python objects and data structures.
"""

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
    # connect to the database
    pass

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
