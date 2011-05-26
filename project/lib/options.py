from optparse import OptionParser

class Options:

  def __init__(self):
    self._init_parser()
    
  def _init_parser(self):
    usage = 'Usage %prog'
    self.parser = OptionParser(usage=usage)
    self.parser.add_option('-x', '--example', default='example-value', dest='example', help='An example option')
  
  def parse(self, args = None):
    return self.parser.parse_args(args)