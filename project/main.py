import sys
import urwid
from lib import EditDisplay

def main():
    try:
        name = sys.argv[1]
        assert open(name, "a")
    except:
        sys.stderr.write(__doc__)
        return
    EditDisplay(name).main()

if __name__ == '__main__':
  main()
