#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE

#############################################################################
# 
#  /home/wayne/iraf/sasiraf/bin/newsite.py
# 
# add new site to the database using a webapp.
# 
# 
# 
#emacs helpers
# (insert (buffer-file-name))
#
# (ediff-current-file)
# (wg-python-fix-pdbrc)
# (find-file-other-frame "./.pdbrc")
# (wg-python-fix-pdbrc)   # PDB DASH DEBUG end-comments
#
# (setq mypdbcmd (concat (buffer-file-name) "<args...>"))
# (progn (wg-python-fix-pdbrc) (pdb mypdbcmd))
#
# (wg-astroconda-pdb)       # IRAF27
# (wg-astroconda3-pdb)      # CONDA Python3
#
# (set-background-color "light blue")
# (wg-python-toc)
#               
#############################################################################
import optparse
import re
import sys
# (wg-python-graphics)
__doc__ = """

/home/wayne/iraf/sasiraf/bin/newsite.py
[options] files...

drop table if exists site;
create table site
(
  id integer PRIMARY KEY AUTO INCREMENT,
  sitename   text UNIQUE, -- guarantee the unique name
  abbrev     text,
  uuid       text,
  obsgeo_b   float,
  obsgeo_l   float,
  obsgeo_h   float
);
insert into site (sitename,uuid,obsgeo_b,obsgeo_l,obsgeo_h) VALUES
   ("Green's Acre Observatory","GAO", '7eaa326c-8c66-11e9-b683-526af7764f64', 40.1039591,-105.201653,1524.0 )

"""

_GAO=r'7eaa326c-8c66-11e9-b683-526af7764f64'
_DCO=r'54ecc3c2-8c76-4e76-aaf5-9cc323074484'
_LGO=r'bcfd1c69-a422-405c-b0df-db4b114ad9c3'

__author__  = 'Wayne Green'
__version__ = '0.1'

% (iv (setq tmp (* 5000.0 12.0 2.54 )))   152400.0 

# Handy funcitons r2s,d2s,s2r,s2d
##############################################################################
# r2s Convert RA in degrees to sexa in hours
#
##############################################################################
def r2s (pobjra):
   """Convert RA in degrees (float or string) to sexigesimal in hours.
   Leading zero for pretty pringing. This is related to a custom
   postgresql function. Negative angles for hour angles can be supported
   by this code.
   Should test for -24 < pobjra < 24
   fmt:  '-HH:MM:SS.ss' ' HH:MM:SS.ss' ftmlen = %12s
   """

   pobjra = float(pobjra) / 15.0;         #  divide degrees into hours first

   idegs = math.floor(pobjra);            #  get the degrees part
   isecs = 60.0 * (pobjra - idegs);       #  get the
   imins = math.floor(isecs);             #  Nail down minutes
   isecs = 60.0 * (isecs - imins);        #  get the float seconds
   sign  = " "

   if(idegs < 0):
      pdegs = "%d" % (0.0 - idegs)
      sign  = "-"
   elif (idegs >= 0 and idegs < 10):
      pdegs = "0%d" % idegs
   else:
      pdegs = "%d" % idegs
   pdegs = sign + pdegs

   pmins = '%d' % imins
   if( imins < 10):
      pmins = '0' + pmins

   psecs = "%.2f" % isecs
   if( isecs < 10.0):
      psecs = '0' + psecs

   ret = "%s:%s:%s" % (pdegs, pmins, psecs)

   return ret

# r2s

##############################################################################
# d2s - convert declination in degrees to sexadecimap
#
##############################################################################
def d2s (pobjdec):
   """Convert declinatin in degrees (float or string) to sexigecimal in
   degrees.  Leading zero for pretty pringing. This is related to a
   custom postgresql function.

   """
   psign = '+';
   pobjdec = float(pobjdec)
   if(pobjdec < 0.0):
      psign='-' ;
      pobjdec = 0.0 - pobjdec;

   idegs = math.floor(pobjdec);            #  get the degrees part
   isecs = 60.0 * (pobjdec - idegs);  #  borrow psec, to get the minutes
   imins = math.floor(isecs);              #  Nail down minutes
   isecs = 60.0 * (isecs - imins);    #  get the float seconds

   pdegs = "%d" % idegs
   if( idegs < 10.0):
      pdegs = '0' + pdegs        #  pad degrees with leading zero

   pmins = "%d" % imins
   if(imins < 10):
      pmins = '0' + pmins;        #  pad minutes with leading zero

   psecs = "%.2f" % isecs
   if(isecs < 10.0):
      psecs = '0' +  psecs       #  pad seconds with leading zero

   ret = "%s%s:%s:%s" % (psign, pdegs, pmins, psecs)

   return ret;

# d2s d2s(12.34567)

##############################################################################
# s2r - convert a sexigesimal RA TO a floating point degrees.
#   input is string hh:mm[:ss.s] Will take ra.ddddd ra:mm.mmm as well.
#   The truncated forms appear in SIMBAD query output.
##############################################################################
coordre = re.compile(r'[dmsh: ]+')
def s2r(rastr):  # PDB -DEBUG
   """Convert a sexigesimal RA to a floating point degrees."""
   if(type(rastr) != type(1.0)):  # PDB -DEBUG
      ra = None
      try:
         parts = list(map(float, coordre.split(rastr)[:3]))
         if(len(parts) == 1):
            ret = parts[0] * 15.0     # a straight hrs.xxxxxxx
         elif(len(parts) == 2):
            ret = (parts[0] + (parts[1] / 60.0)) * 15.0
         elif(len(parts) == 3):
            ret = (parts[0] + (parts[1] / 60.0) + parts[2]/3600.0) * 15.0
      except:
         raise ValueError("s2r: Unable to convert %s to degrees ra" % rastr)
   else:
      ret = rastr

   return ret

# def s2r  s2r('12.34567') s2r('12:13.4567') s2r('12:13:45.67') s2r('20 08 24')


##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################

if __name__ == "__main__":
   opts = optparse.OptionParser(usage="%prog "+__doc__)

   opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

   (options, args) = opts.parse_args()

   #if(len(args) == 0 ): args.append(None)
   for filename in args:
      with open(filename,'r') if filename else sys.stdin as f:
         for l in f:
            if('#' in l):
               continue
            parts = map(str.strip,l.split()) 



