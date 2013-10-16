#!/usr/bin/env python3.3

import cgi
import markovChains


def main():
    # Check if they logged in
    form = cgi.FieldStorage()
    logged_in = False
    log_in_failure = False
    if "name" in form:
        username = form["name"].value
        if "password" in form:
            password = form["password"].value
        else:
            password = ""
        cookie = markovChains.check_credentials(username, password)
        if cookie:
            logged_in = True
        if not logged_in:
            log_in_failure = True
    # Build the page
    if logged_in:
        # TODO: set cookie or something
        markovChains.redirect("user.py", cookie)
    else:
        markovChains.printHeader()
        if log_in_failure:
            print("Invliad username or password, please try again.")
        print("""<form method="post" action="index.py">
Name: <input type="text" size="20" maxlength="40" name="name"> <br />
Password: <input type="password" size="20" maxlength="40" name="password"> <br />
<input type="submit" value="Log in">
</form>
<br />
<a href="create_account.py">Create account</a>
""")
        markovChains.printFooter()


if __name__ == "__main__":
    main()
