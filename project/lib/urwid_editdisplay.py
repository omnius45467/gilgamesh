import sys
import urwid
from urwid_linewalker import LineWalker

class EditDisplay:
    palette = [
        ('body','default', 'default'),
        ('foot','dark cyan', 'dark blue', 'bold'),
        ('key','light cyan', 'dark blue', 'underline'),
        ]

    footer_text = ('foot', [
        "Text Editor    ",
        ('key', "F5"), " save  ",
        ('key', "F8"), " quit",
        ])

    def __init__(self, name):
        self.save_name = name
        self.walker = LineWalker(name)
        self.listbox = urwid.ListBox(self.walker)
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text),
            "foot")
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'),
            footer=self.footer)

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.unhandled_keypress)
        self.loop.run()

    def unhandled_keypress(self, k):
        """Last resort for keypresses."""

        if k == "f5":
            self.save_file()
        elif k == "f8":
            raise urwid.ExitMainLoop()
        elif k == "delete":
            # delete at end of line
            self.walker.combine_focus_with_next()
        elif k == "backspace":
            # backspace at beginning of line
            self.walker.combine_focus_with_prev()
        elif k == "enter":
            # start new line
            self.walker.split_focus()
            # move the cursor to the new line and reset pref_col
            self.loop.process_input(["down", "home"])
        elif k == "right":
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_next(pos)
            if w:
                self.listbox.set_focus(pos, 'above')
                self.loop.process_input(["home"])
        elif k == "left":
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_prev(pos)
            if w:
                self.listbox.set_focus(pos, 'below')
                self.loop.process_input(["end"])
        else:
            return
        return True


    def save_file(self):
        """Write the file out to disk."""

        l = []
        walk = self.walker
        for edit in walk.lines:
            # collect the text already stored in edit widgets
            if edit.original_text.expandtabs() == edit.edit_text:
                l.append(edit.original_text)
            else:
                l.append(re_tab(edit.edit_text))

        # then the rest
        while walk.file is not None:
            l.append(walk.read_next_line())

        # write back to disk
        outfile = open(self.save_name, "w")

        prefix = ""
        for line in l:
            outfile.write(prefix + line)
            prefix = "\n"

def re_tab(s):
    """Return a tabbed string from an expanded one."""
    l = []
    p = 0
    for i in range(8, len(s), 8):
        if s[i-2:i] == "  ":
            # collapse two or more spaces into a tab
            l.append(s[p:i].rstrip() + "\t")
            p = i

    if p == 0:
        return s
    else:
        l.append(s[p:])
        return "".join(l)

