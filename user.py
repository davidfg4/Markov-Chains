#!/usr/bin/env python3.3

import cgi
import markovChains


def main():
    user = markovChains.check_browser_cookie()
    markovChains.printHeader()
    print("You are logged in as " + user)
    markovChains.printFooter()


if __name__ == "__main__":
    main()
