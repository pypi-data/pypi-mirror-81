from ._library import *
from . import version
from .version import module as __version__

def get_config():
  """Returns a string containing the configuration information.
  """
  import bob.extension
  return bob.extension.get_config(__name__, version.externals)

# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]


import warnings
warnings.simplefilter('default')
warnings.warn("bob.ip.draw will be deprecated in 01/04/2020. Please use matplotlib for plotting.", DeprecationWarning)
