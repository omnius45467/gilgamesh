import urwid
import time

class GraphView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    graph display.
    """
    palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('line',         'black',      'light gray', 'standout'),
        ('bg background','light gray', 'black'),
        ('bg 1',         'black',      'dark blue', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 2 smooth',  'dark cyan',  'black'),
        ('button normal','light gray', 'dark blue', 'standout'),
        ('button select','white',      'dark green'),
        ('line',         'black',      'light gray', 'standout'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
        ('pg smooth',     'dark magenta','black')
        ]

    graph_samples_per_bar = 10
    graph_num_bars = 5
    graph_offset_per_second = 5

    def __init__(self, controller):
        self.controller = controller
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None
        urwid.WidgetWrap.__init__(self, self.main_window())

    def get_offset_now(self):
        if self.start_time is None:
            return 0
        if not self.started:
            return self.offset
        tdelta = time.time() - self.start_time
        return int(self.offset + (tdelta*self.graph_offset_per_second))

    def update_graph(self, force_update=False):
        o = self.get_offset_now()
        if o == self.last_offset and not force_update:
            return False
        self.last_offset = o
        gspb = self.graph_samples_per_bar
        r = gspb * self.graph_num_bars
        d, max_value, repeat = self.controller.get_data( o, r )
        l = []
        for n in range(self.graph_num_bars):
            value = sum(d[n*gspb:(n+1)*gspb])/gspb
            # toggle between two bar types
            if n & 1:
                l.append([0,value])
            else:
                l.append([value,0])
        self.graph.set_data(l,max_value)

        # also update progress
        if (o//repeat)&1:
            # show 100% for first half, 0 for second half
            if o%repeat > repeat//2:
                prog = 0
            else:
                prog = 1
        else:
            prog = float(o%repeat) / repeat
        self.animate_progress.set_completion( prog )
        return True

    def on_animate_button(self, button):
        """Toggle started state and button text."""
        if self.started: # stop animation
            button.set_label("Start")
            self.offset = self.get_offset_now()
            self.started = False
            self.controller.stop_animation()
        else:
            button.set_label("Stop")
            self.started = True
            self.start_time = time.time()
            self.controller.animate_graph()


    def on_reset_button(self, w):
        self.offset = 0
        self.start_time = time.time()
        self.update_graph(True)

    def on_mode_button(self, button, state):
        """Notify the controller of a new mode setting."""
        if state:
            # The new mode is the label of the button
            self.controller.set_mode( button.get_label() )
        self.last_offset = None

    def on_mode_change(self, m):
        """Handle external mode change by updating radio buttons."""
        for rb in self.mode_buttons:
            if rb.get_label() == m:
                rb.set_state(True, do_callback=False)
                break
        self.last_offset = None

    def on_unicode_checkbox(self, w, state):
        self.graph = self.bar_graph( state )
        self.graph_wrap._w = self.graph
        self.animate_progress = self.progress_bar( state )
        self.animate_progress_wrap._w = self.animate_progress
        self.update_graph( True )


    def main_shadow(self, w):
        """Wrap a shadow and background around widget w."""
        bg = urwid.AttrWrap(urwid.SolidFill(u"\u2592"), 'screen edge')
        shadow = urwid.AttrWrap(urwid.SolidFill(u" "), 'main shadow')

        bg = urwid.Overlay( shadow, bg,
            ('fixed left', 3), ('fixed right', 1),
            ('fixed top', 2), ('fixed bottom', 1))
        w = urwid.Overlay( w, bg,
            ('fixed left', 2), ('fixed right', 3),
            ('fixed top', 1), ('fixed bottom', 2))
        return w

    def bar_graph(self, smooth=False):
        satt = None
        if smooth:
            satt = {(1,0): 'bg 1 smooth', (2,0): 'bg 2 smooth'}
        w = urwid.BarGraph(['bg background','bg 1','bg 2'], satt=satt)
        return w

    def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

    def radio_button(self, g, l, fn):
        w = urwid.RadioButton(g, l, False, on_state_change=fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

    def progress_bar(self, smooth=False):
        if smooth:
            return urwid.ProgressBar('pg normal', 'pg complete',
                0, 1, 'pg smooth')
        else:
            return urwid.ProgressBar('pg normal', 'pg complete',
                0, 1)

    def exit_program(self, w):
        raise urwid.ExitMainLoop()

    def graph_controls(self):
        modes = self.controller.get_modes()
        # setup mode radio buttons
        self.mode_buttons = []
        group = []
        for m in modes:
            rb = self.radio_button( group, m, self.on_mode_button )
            self.mode_buttons.append( rb )
        # setup animate button
        self.animate_button = self.button( "", self.on_animate_button)
        self.on_animate_button( self.animate_button )
        self.offset = 0
        self.animate_progress = self.progress_bar()
        animate_controls = urwid.GridFlow( [
            self.animate_button,
            self.button("Reset", self.on_reset_button),
            ], 9, 2, 0, 'center')

        if urwid.get_encoding_mode() == "utf8":
            unicode_checkbox = urwid.CheckBox(
                "Enable Unicode Graphics",
                on_state_change=self.on_unicode_checkbox)
        else:
            unicode_checkbox = urwid.Text(
                "UTF-8 encoding not detected")

        self.animate_progress_wrap = urwid.WidgetWrap(
            self.animate_progress)

        l = [    urwid.Text("Mode",align="center"),
            ] + self.mode_buttons + [
            urwid.Divider(),
            urwid.Text("Animation",align="center"),
            animate_controls,
            self.animate_progress_wrap,
            urwid.Divider(),
            urwid.LineBox( unicode_checkbox ),
            urwid.Divider(),
            self.button("Quit", self.exit_program ),
            ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w

    def main_window(self):
        self.graph = self.bar_graph()
        self.graph_wrap = urwid.WidgetWrap( self.graph )
        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        c = self.graph_controls()
        w = urwid.Columns([('weight',2,self.graph_wrap),
            ('fixed',1,vline), c],
            dividechars=1, focus_column=2)
        w = urwid.Padding(w,('fixed left',1),('fixed right',0))
        w = urwid.AttrWrap(w,'body')
        w = urwid.LineBox(w)
        w = urwid.AttrWrap(w,'line')
        w = self.main_shadow(w)
        return w
