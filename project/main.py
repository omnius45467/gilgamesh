import os
import sys
import urwid
from lib import EditDisplay
from lib import GraphController
from lib import HelpMenu
from lib import DatabaseConnection

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def edit(name):
    try:
        assert open(name, "a")
    except:
        sys.stderr.write(__doc__)
        return
    EditDisplay(name).main()


def graph():
    GraphController().main()


def trends():
    print("twitter trends")


def help():
    HelpMenu().main()


def diagnostic():
    print("diagnostic")


def main():
    arg = sys.argv[1]

    if arg == '-e':
        name = sys.argv[2]
        if name:
            edit(name)
        else:
            print("Sorry I can't make a connection")

    elif arg == '-a':
        print("starting db connection")
        DatabaseConnection().RawModel()

    elif arg == '-i':
        graph()

    elif arg == '-t':
        trends()

    elif arg == '-h':
        help()

    elif arg == '-d':
        diagnostic()

    else:
        print("there was a problem")


if __name__ == '__main__':
    main()
