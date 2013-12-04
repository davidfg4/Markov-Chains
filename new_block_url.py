#!/usr/bin/env python3.3

import cgi
import markovChains
import urllib.request


def main():
    form = cgi.FieldStorage()
    user = markovChains.check_browser_cookie()
    if "name" in form and "url" in form:
        name = form["name"].value
        url = form["url"].value
        f = urllib.request.urlopen(url)
        text = f.read()
        markovChains.create_block(name, user, text, url)
        markovChains.redirect("user.py")
    else:
        markovChains.printHeader()
        print("""<form method="post" action="new_block_url.py">
Block name:<br />
<input type="text" size="20" maxlength="40" name="name"> <br />
URL:<br />
<input type="text" size="60" maxlength="500" name="url"> <br />
<br />
<input type="submit" value="Submit">
</form>
<br />
<a href="http://www.gutenberg.org/ebooks/search/?sort_order=downloads">Popular Gutenberg ebooks</a>
""")
        markovChains.printFooter()


if __name__ == "__main__":
    main()
