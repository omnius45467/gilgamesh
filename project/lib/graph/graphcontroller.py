import urwid
from graphmodel import GraphModel
from graphview import GraphView

class GraphController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """
    def __init__(self):
        self.animate_alarm = None
        self.model = GraphModel()
        self.view = GraphView( self )
        # use the first mode as the default
        mode = self.get_modes()[0]
        self.model.set_mode( mode )
        # update the view
        self.view.on_mode_change( mode )
        self.view.update_graph(True)

    def get_modes(self):
        """Allow our view access to the list of modes."""
        return self.model.get_modes()

    def set_mode(self, m):
        """Allow our view to set the mode."""
        rval = self.model.set_mode( m )
        self.view.update_graph(True)
        return rval

    def get_data(self, offset, range):
        """Provide data to our view for the graph."""
        return self.model.get_data( offset, range )


    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()

    def animate_graph(self, loop=None, user_data=None):
        """update the graph and schedule the next update"""
        self.view.update_graph()
        self.animate_alarm = self.loop.set_alarm_in(
            UPDATE_INTERVAL, self.animate_graph)

    def stop_animation(self):
        """stop animating the graph"""
        if self.animate_alarm:
            self.loop.remove_alarm(self.animate_alarm)
        self.animate_alarm = None

