#!/usr/bin/env python3.3

import cgi
import markovChains


def main():
    markovChains.printHeader()
    print("""You are logged in!""")
    markovChains.printFooter()


if __name__ == "__main__":
    main()
