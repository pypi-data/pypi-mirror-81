# Copyright (c) 2020 Dimitrios-Georgios Akestoridis
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Python implementation of Multiple-Criteria Decision-Making algorithms
"""

import os

from .__about__ import __author__            # noqa: F401
from .__about__ import __author_email__      # noqa: F401
from .__about__ import __classifiers__       # noqa: F401
from .__about__ import __copyright__         # noqa: F401
from .__about__ import __description__       # noqa: F401
from .__about__ import __install_requires__  # noqa: F401
from .__about__ import __keywords__          # noqa: F401
from .__about__ import __license__           # noqa: F401
from .__about__ import __python_requires__   # noqa: F401
from .__about__ import __title__             # noqa: F401
from .__about__ import __url__               # noqa: F401

from .__getversion__ import getversion

from .correlate import correlate
from .load import load
from .normalize import normalize
from .rank import rank
from .score import score
from .weigh import weigh


__version__ = getversion(os.path.dirname(os.path.abspath(__file__)))
__all__ = ["load", "normalize", "correlate", "weigh", "score", "rank"]
