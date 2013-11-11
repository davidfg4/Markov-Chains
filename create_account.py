#!/usr/bin/env python3.3

import cgi
import markovChains

def main():
    form = cgi.FieldStorage()
    created = False
    logged_in = False
    username = ""
    if "name" in form:
        username = form["name"].value
        if "password" in form:
            password = form["password"].value
        else:
            password = ""
        created = markovChains.create_user(username, password)
        cookie = markovChains.check_credentials(username, password)
        if cookie:
            logged_in = True
    # Build the page
    if logged_in:
        markovChains.redirect("user.py", cookie)
    else:
        markovChains.printHeader()
        if username != "" and not created:
            print("Error creating account, try a different username.<br>")
        print("""<form method="get" action="create_account.py">
Name: <input type="text" size="20" maxlength="40" name="name"> <br />
Password: <input type="password" size="20" maxlength="40" name="password"> <br />
<input type="submit" value="Create account">
</form>
""")
        markovChains.printFooter()


if __name__ == "__main__":
    main()
