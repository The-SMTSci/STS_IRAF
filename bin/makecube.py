#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

import optparse
import numpy as np
from astropy.io import fits

#############################################################################
# makecube.py
#############################################################################
__doc__ = """

makecube -- given an ordered command line of files (chronological is good)
build a cube across that ordered dimension. Beware wildcards do not
build a lexigraphically sorted list of names.\

"""

__author__  = 'Wayne Green'
__version__ = '0.1'

##############################################################################
#                                    Main
##############################################################################
if __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-o", "--output", action="store", dest="outputname",
                   default="cube.fits",
                   help="<str>     Output name of the cube.")

    (options, args) = opts.parse_args()

    files  = args   # the filenames in order)
    data   = []
    for filename in args:
        with fits.open(filename) as f:
          data.append(f[0].data)
    
    cube = np.array(data)
    nf   = fits.PrimaryHDU(data)
    nf.writeto(options.outputname, output_verify='fix', overwrite=True)

