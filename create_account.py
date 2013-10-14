#!/usr/bin/env python3.3

import markovChains

def main():
    markovChains.printHeader()
    print("""<form method="get" action="user.py">
Name: <input type="text" size="20" maxlength="40" name="name"> <br />
Password: <input type="password" size="20" maxlength="40" name="name"> <br />
<input type="submit" value="Create account">
</form>
""")
    markovChains.printFooter()


if __name__ == "__main__":
    main()
