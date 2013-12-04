#!/usr/bin/env python3.3

import cgi
import markovChains


def main():
    user = markovChains.check_browser_cookie()
    markovChains.printHeader()
    print("You are logged in as " + user)
    print("<br />")
    print("<br />")
    print("<h2>Blocks</h2>")
    blocks = markovChains.get_blocks(user)
    print("<table>")
    print("<tr><th>Name</th><th>Actions</th></tr>")
    for block in blocks:
        print("<tr><td>" + block['name'] + '</td><td><a href="create_chain.py?id=' + str(block['id']) + '">Create chain</a></td></tr>')
    print("</table>")
    print("<br />")
    print('<a href="new_block.py">Create a new block from text</a>')
    print("<br />")
    print('<a href="new_block_url.py">Create a new block from a webpage</a>')
    markovChains.printFooter()


if __name__ == "__main__":
    main()
