# customize IRAF login

# force the graphics buffer to be very large
# set cmbuflen=256000
gflush
# snap or = will drop off funky file name sgixxxx.eps in current dir.
#set stdplot = epsl

# Things to override from login.cl (wg 2018-11-21T08:42:18-0700)
set	imextn		      = "oif:imh fxf:fits,fit,fts fxb:fxb plf:pl qpf:qp stf:hhh,??h"

#############################################################################
# some useful routines outside of IRAF - declare a foreign task
# local to the sas project.
#############################################################################
task $ds9="$foreign"
task $iraffind="$foreign"
# Some handy bash scriptlets to have to hand.
task $r = ("$(ls -lt * | grep -v '[ ][.]' | head -10 ;)")  # show 10 recent changed files
task $ll = ("$(ls -1 $* | tee l.l | cat)")
task $makedirs = ("$(mkdir -p usw/Targets RawData PreAnalysis Reduce Analysis)")
task $flexspec = "home$flexspec.cl"

#Internal task -- 

# deftask("clpackage.xxxx")   # where xxxx is the task name
task $atfiles = "home$atfiles.cl"


# run the Goddard fitsverify on files(s) in less for my review.
# this is similar to "imheader my.fits l+ u+" but does not mess with
# the first seven header keys.
task $fvl  = ("$(~/bin/fitsverify -l $* | less -i)")


# define pixel directory
set imdir="home$images"

# set printer and plot device     # sgi2ueps.c 
# set printer=lw5
# set stdplot=lw5
# set stdplot=pgdump


# add other commands here but before keep
set imtype=fits
#!ds9 &
#!stty erase ?

# Some image sizes format to display at the image viewer (DS9):
#set stdimage=imt512
#set stdimage=imt800
#set stdimage=imt1024
#set stdimage=imt1600
#set stdimage=imt2048
#set stdimage=imt4096
set stdimage=imt8192


# load some packages at startup time for photometry
noao
imred
crutil
ccdred
obsutil

# load some basic packages for spectral analysis
twodspec
apextract
onedspec  

# set up to do intereactive images
images
tv     

# Some instrument parameters (Observatory and CCD camera).
setinst.site="elsauce"

setinst.dir="ccddb$"

# Default observatory "elsauce":
# ./noao/imred/ccdred/ccddb/sbo : default.cl  instruments.men
# remember to update iraf/noao/lib/obsdb.dat
# observatory set subaru
observatory set elsauce

set imclobber=yes
set clobber=yes

keep
