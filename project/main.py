import sys
import urwid
from lib import EditDisplay
from lib import GraphController


def edit(name):
    try:
        assert open(name, "a")
    except:
        sys.stderr.write(__doc__)
        return
    EditDisplay(name).main()


def graph():
    GraphController().main()


def main():

    arg = sys.argv[1]
    print(sys.argv)

    if arg == '-e':
      name = sys.argv[2]

      if name:
        print("edit")
        edit(name)

    elif arg == '-d':
      print("display")
      graph()

    else:
      print("there was a problem")


if __name__ == '__main__':
  main()
