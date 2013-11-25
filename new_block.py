#!/usr/bin/env python3.3

import cgi
import markovChains


def main():
    form = cgi.FieldStorage()
    user = markovChains.check_browser_cookie()
    if "name" in form and "text" in form:
        name = form["name"].value
        text = form["text"].value
        markovChains.create_block(name, user, text)
        markovChains.redirect("user.py")
    else:
        markovChains.printHeader()
        print("""<form method="post" action="new_block.py">
Block name:<br />
<input type="text" size="20" maxlength="40" name="name"> <br />
Text:<br />
<textarea name="text" cols="50" rows="20"></textarea>
<br />
<input type="submit" value="Submit">
</form>
""")
        markovChains.printFooter()


if __name__ == "__main__":
    main()
