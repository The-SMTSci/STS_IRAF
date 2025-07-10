#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /home/git/pre/pre.DarkExperiment/data/work/foo
# (wg-python-fix-pdbrc)

import optparse
import numpy as np
from astropy.io import fits

#############################################################################
# makecube.py
#############################################################################
__doc__ = """

makecube -- given a list of files in from the command line; or for no files
  use a file called l.l -- make a cube, and 2D images for the mean -- drawn
  across each depth for each (row,column). This produces the statistics
  just for each pixel. The 2D cubemean.fits shows the mean value for
  the handful of pixels at that precise location for all images.

  No test that the images are the samesize is done.

  Options:
  -o set the filename for the output cube default is cube.fits
     Note: the base name is taken as the 'cube' part, and used
     for the other images.
  -s set a sigma-clip value: default is 1.5
  -v make a small report, lines appear as comments.


"""

__author__  = 'Wayne Green'
__version__ = '0.1'


##############################################################################
# loadll
##############################################################################
def loadll(fname):
    """Open list fname, read each filename, make a list of strings, return"""
    flist = []
    with open(fname,'r') as f:
        for n in f:
            flist.append(n.strip())
    return flist

# fname

##############################################################################
#                                    Main
##############################################################################
if __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-o", "--output", action="store", dest="outputname",
                   default="cube.fits",
                   help="<str>     Output name of the cube.")

    opts.add_option("-s", "--sclip", action="store", dest="sigmaclip",
                   default="1.5",
                   help="<int>     img.mean() + img.std() * sclip.")

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose.")

    (options, args) = opts.parse_args()

    sclip           = float(options.sigmaclip)
    basename,_,     = list(map(str.strip,options.outputname.split('.')))[:2] # ignore ext
    basename        = "cube"

    if(len(args) == 0):                                 # missing args, try...
        files  = loadll('l.l')                          # the filenames in order
    else:
        files  = args

    data            = []                                 # basis for the cube

    for filename in files:                               # add file's data to basis
        with fits.open(filename) as f:
            data.append(f[0].data)                       # accumulate the images

    cube            = np.array(data)                     # make a [Z,Y,X] cube.
    nf              = fits.PrimaryHDU(data)
    nf.writeto(f"{basename}.fits", output_verify='fix', overwrite=True)

    cubemean        = np.nanmean(cube, axis=0)           # each cubemean pixel is mean across time
    cubestd         = np.nanstd(cube,axis=0)

    nf              = fits.PrimaryHDU(cubemean)
    nf.writeto(f"{basename}mean.fits", output_verify='fix', overwrite=True)

    nf              = fits.PrimaryHDU(cubestd)
    nf.writeto(f"{basename}std.fits", output_verify='fix', overwrite=True)

    test            = cubemean.mean() + cubestd.mean() * sclip  # get a working limit -s
    wbright         = np.where(cubemean > test)          # where px exceed this
    bright          = np.zeros_like(cubemean)            # zero image
    bright[wbright] = cubemean[wbright]                  # set bad values into the zero img.
    nf              = fits.PrimaryHDU(bright)
    nf.writeto(f"{basename}bright.fits", output_verify='fix', overwrite=True)
    if(options.verboseflag):
        mean = cubemean.mean()
        cstd = cubestd.mean()
        print(f"# mean: {mean:7.3f} std : {cstd:7.3f} sclip: {sclip:7.3f}")
        print(f"# Bad px found : {len(wbright[0])} > {mean + cstd  * sclip:7.3f}")
