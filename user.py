#!/usr/bin/env python3.3

import cgi
import markovChains


def main():
    user = markovChains.check_browser_cookie()
    markovChains.printHeader()
    print("You are logged in as " + user)
    print("<br>")
    print("<h2>Blocks</h2>")
    print("<table>")
    print("<tr><th>Name</th><th>New text</th></tr>")
    print("<tr><td>example block</td><td>new text</td></tr>")
    print("</table>")
    markovChains.printFooter()


if __name__ == "__main__":
    main()
