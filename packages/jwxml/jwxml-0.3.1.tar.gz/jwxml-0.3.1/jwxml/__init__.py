"""
jwxml: Various Python classes for parsing JWST-related information in XML files

* `SUR`: a segment update request file
  (mirror move command from the WAS to the MCS)
* `Segment_Update`: a single mirror update inside of a SUR
* `SIAF`: a SIAF file (Science Instrument Aperture File,
  listing the defined apertures for a given instrument)
* `Aperture`: a single aperture inside a SIAF
"""

from .mirrors import Segment_Update, SUR
from .siaf import Aperture, SIAF
from .constants import PRD_VERSION, PRD_DATA_ROOT
import warnings

__all__ = ['Segment_Update', 'SUR', 'Aperture', 'SIAF', 'PRD_DATA_ROOT', 'PRD_VERSION']

import os.path

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    __version__ = f.read().strip()

warnings.warning("jwxml is deprecated and its use should be phased out. See pysiaf and/or webbpsf instead.", DeprecationWarning)
