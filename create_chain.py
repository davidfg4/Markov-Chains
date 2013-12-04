#!/usr/bin/env python3.3

import cgi
import markovChains


def main():
    form = cgi.FieldStorage()
    user = markovChains.check_browser_cookie()
    if "id" not in form:
        markovChains.printHeader()
        print("Error: block id is required, go back to the user page and try again.")
        markovChains.printFooter()
        return
    id = form['id'].value
    if "context" in form and "length" in form:
        context = form["context"].value
        length = int(form["length"].value)
        markovChains.printHeader()
        print(markovChains.create_chain(id, context, length))
        markovChains.printFooter()
    else:
        markovChains.printHeader()
        block = markovChains.get_blocks(user, id=id)
        print("""<form method="post" action="create_chain.py">
<input type="hidden" name="id" value='""" + id + """'>
Block name: """ + block[0]['name'] + """
<br />
Context to use:
<select name="context">
<option value="0">1 word</option>
<option value="1">1 letter</option>""")
        for i in range(2, 11):
            print('<option value="' + str(i) + '">' + str(i) + ' letters</option>')
        print("""</select>
<br />
Length: <input type="text" size="10" maxlength="5" name="length" value="500"><br />
<br />
<br />
<input type="submit" value="Create">
</form>
""")
        markovChains.printFooter()


if __name__ == "__main__":
    main()
