#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-astroconda-pdb)
# (wg-python-fix-pdbrc)
#
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "pydoc3 %s" (buffer-file-name)))
#
#############################################################################
### HEREHEREHERE

import os
import optparse
import sys
import re
import numpy  as np
import pandas as pd
from astropy.io          import fits
from astropy.table       import QTable, Table, Column
from astroplan           import Observer, FixedTarget, AirmassConstraint
from astropy.time        import Time
from astropy.coordinates import EarthLocation
from astroquery.simbad   import Simbad

elsauce  = EarthLocation(lat=-30.47069, lon= -70.764941, height=1565.427 )
observer = Observer(location=elsauce,name='El Sauce', timezone='Chile/Continental')

__FSDEBUG = [False,True][os.getenv('FSDEBUG') == '']

# to handle the Unicode filenames from Win1X
_encoding = 'utf-8'                         # deal with nt's UTF issues.
if(os.name == 'nt'):
    _encoding = 'utf-16'
# with io.open(listname,'r',encoding=_encoding) as f:

# (wg-python-types)
#############################################################################
#
#
#  /home/wayne/bin/obslist.py
# (wg-python-emacs-help)
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['ObsListException','ObsList']   # list of quoted items to export
# class ObsListException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class ObsList(object,targetnames):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self,targetnames=None):                    # ObsList::__init__()
#     def load(self,newnames=None):                           # ObsList.load()
#     def debug(self,msg="",skip=[],os=sys.stderr):           # ObsList::debug()
# if __name__ == "__main__":
#
#
#
#
#
#############################################################################

__doc__ = """

/home/wayne/bin/obslist.py
[options] files...



from astropy.table import QTable, Table, Column
import pandas as pd

tbl = Table()
tbl['targets']=mytargets
print(tbl)
df = tbl.to_pandas()

2024-12-13T20:58:52-0700
"""
 

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['ObsListException','ObsList']   # list of quoted items to export

# testing: my wr targets, SIMBAD names
_testlist = [ "EM* AS 431",
              "HD 195177",
              "EM* AS 422",
              "MR 110",
              "MR 112",
              "WR 150",
              "LS III +44 21",
              "HD 213049",
              "HD 211853",
              "HD 211564",
              "HD 214419",
              "HD 193793",
              "MR 114",
              "MR 119",
              "HD 219460B",
              "V* PZ Cas",
              "HD 6327",
              "HD 9974",
              "HD 197406",
              "MR 121",
              "EM* AS 513",
              "BD+62 2296B",
              "HD 17638",
              "HD 16523",
              "HD 4004",
              "NGC 40",
              "HD 45166",
              "HD 50896",
              "HD 56925",
              "MR 8",
              "HD 62910",
              "HD 63099",
              "HD 65865",
              "[MJ98] B14",
              "HD 151932",
              "HD 152408",
              "HD 152270",
              "HD 326823",
              "HD 157451",
              "THA 31-1",
              "LS 3982",
              "MR 59",
              "WRAY 15-1656",
              "CD-38 11746",
              "WRAY 15-1666",
              "CPD-33 4347",
              "HD 156327",
              "HD 157504",
              "HD 158860",
              "HD 320102",
              "[S75] 6",
              "HD 163758",
              "MR 74",
              "HD 318016",
              "WRAY 15-1736",
              "HD 318139",
              "HD 164270",
              "MR 63",
              "EM* AS 268",
              "MR 80",
              "HD 313848",
              "HD 313846",
              "HD 313643",
              "SS73 123",
              "HD 165763",
              "HD 165688",
              "HD 168206",
              "HD 169010",
              "THA 20-1",
              "EM* AS 320",
              "MR 89",
              "HD 177230",
              "Hen 2-427",
              "HD 187282",
              "WR 126",
              "MR 96",
              "HD 186943",
              "HD 190002",
              "EM* AS 374",
              "HD 192103",
              "HD 190918",
              "HD 191765",
              "HD 192641",
              "HD 192163",
              "HD 228766",
              "WR 142",
              "HD 193928",
              "HD 193077",
              "HD 193576",
              "* gam02 Vel",
              "Ve 6-15",
              "CD-45 4482",
              "Ve 6-14",
              "HD 76536",
              "HD 79573",
              "LHA 120-S 61",
              "LHA 120-S 28",
              "HD 32228",
              "HD 270952",
              "LHA 120-S 9",
              "HD 33133",
              "HD 269748",
              "HD 37680",
              "HD 269828",
              "HD 38030",
              "HD 269891",
              "RMC 135",
              "RMC 139",
              "RMC 140",
              "HD 269928",
              "HD 38344",
              "HD 38448",
              "HD 269956",
              "Brey 57",
              "Brey 73",
              "Brey 76",
              "Brey 79",
              "Brey 81",
              "Brey 84",
              "HD 269818",
              "HD 269687",
              "Brey 70",
              "LHA 120-S 142",
              "Brey 95a",
              "BAT99 97",
              "BAT99 113",
              "Cl* NGC 2070 MH 57",
              "Brey 75",
              "Brey 74a",
              "BAT99 108",
              "BAT99 110",
              "BAT99 111",
              "BAT99 112",
              "BAT99 114",
              "HD 269858",
              "LHA 120-S 125",
              "HD 38282",
              "LHA 120-S 131",
              "BAT99 106",
              "BAT99 109",
              "Cl* NGC 2070 MEL 53a",
              "RMC 140a",
              "BAT99 80",
              "RMC 140b",
              "CPD-69 394",
              "HD 269926",
              "BAT99 78",
              "RMC 136",
              "HD 34632",
              "HD 269698",
              "Brey 16a",
              "HD 36521",
              "HD 269546",
              "HD 269333",
              "Brey 41",
              "LHA 120-S 108",
              "HD 36402",
              "HD 35517",
              "HD 269227",
              "HD 269445",
              "HD 34169",
              "HD 37026",
              "HD 269582",
              "[H2013] LMCe 584",
              "HD 32109",
              "Brey 10a",
              "HD 268856",
              "HD 32402",
              "SK -67 18",
              "HD 86161",
              "HD 37248",
              "Brey 40a",
              "SV* HV 5560",
              "HD 36156",
              "HD 36063",
              "WR 19",
              "V* V712 Car",
              "WR 20b",
              "THA 35-II-42",
              "HD 89358",
              "SS 215",
              "CPD-60 1619",
              "HD 88500",
              "HD 91421",
              "[MS70] 1",
              "HD 92809",
              "HD 90657",
              "HD 95435",
              "HD 93129A",
              "HD 93162",
              "WR 28",
              "THA 35-II-117",
              "WR 35a",
              "HD 93131",
              "HD 94546",
              "V* AG Car",
              "LSWR 4",
              "HD 92740",
              "WRAY 15-682",
              "[MS70] 4",
              "HD 94305",
              "Cl* NGC 3603 MDS C",
              "MR 37",
              "MR 35",
              "HD 97152",
              "MR 39",
              "HD 97950",
              "WR 36",
              "Cl* NGC 3603 BLW A1",
              "Cl* NGC 3603 MDS B",
              "WR 39",
              "WR 35",
              "MR 32",
              "THA 35-II-153",
              "HD 96548",
              "LIN 547",
              "[W65] c18",
              "LIN 160",
              "RMC 31",
              "HD 5980",
              "SMC AB 7",
              "HD 104994",
              "MR 41",
              "Cl Hogg 15 4",
              "HD 311884",
              "* tet Mus",
              "WR 49",
              "CPD-61 3569",
              "V* WX Cen",
              "MR 48",
              "HD 119078",
              "HD 115473",
              "HD 117297",
              "WRAY 16-136",
              "HD 117688",
              "MR 51",
              "HD 121194",
              "MR 53",
              "WR 62a",
              "WRAY 15-1254",
              "HD 136488",
              "WRAY 16-172",
              "MR 55",
              "HD 134877",
              "WRAY 15-1297",
              "HD 143414",
              "HD 137603",
              "HD 147419",
              "GSC 08334-00500",
              "MR 62",
              "HD 152386",
              "WRAY 15-1600",
              "MR 66",
              "MR 67",
              "HD 156385",
              "WR 44-1",
              "MR 61",
              "MR 18",
              "Brey 56",
              "WR 72",
              "WR 43-3",
              "WR 111-9",
              "PHR J1134-5243",
              "MR 87",
              "MR 97",
              "Brey 77",
             ]

query = """
select main_id,allfluxes.*,onames.* from basic
   join allfluxes on allfluxes.oidref = basic.oid
   join onames    on onames.oidref    = basic.oid
"""

##############################################################################
# ObsListException
#
##############################################################################
class ObsListException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(ObsListException,self).__init__("ObsList "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" ObsList: {e.__str__()}\n"
# ObsListException

##############################################################################
# ObsList
#
##############################################################################
class ObsList(object,targetnames):
    """ Given a list of files, array or a @filename, develop an observing list.
        For each target get the MAIN_ID, pgmname, ra, dec, otype, otypes, fluxes, 
        and auxillary names for the target.

        There is a 1:many between MAIN_ID and auxillary names.
        Save fluxes and otypes in a PostgreSQL jason statement.

        fluxes from SIMBAD table allfluxes

    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self,targetnames=None):                    # ObsList::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.targetnames    = targetnames                    # the file, or list of files for this query.
        self.simbadname     = None
        self.aliases        = {}
        self.ra             = None
        self.dec            = None
        self.sptype         = None
        self.vmag           = None
        self.simbad         = Simbad()                    # get our instance
        self.results        = []                          # the row from the results.
        self.table          = None                        # The table returned from astroquery of simbad
        self.auxnames       = []                          # alternate names 
        self.queryfields    = [ 'main_id', 'otype', 'sptype', 'dec(d;ICRS)', 'id(1)', 'otype(V)', 'ra(d;ICRS)', 
                                'flux(U)', 'flux(B)', 'flux(V)', 'flux(R)', 'flux(I)', 'flux(J)', 'flux(H)', 'flux(K)',
                                'flux(u_)', 'flux(g_)', 'flux(r_)', 'flux(i_)', 'flux(z_)'
                              ]
        fields              = self.simbad.get_votable_fields() + self.queryfields # blend in our fields 
        self.aliases        = self.simbad.query_objectids("Polaris")
        for fld in fields:
            self.simbad.add_votable_fields(fld)

    ### ObsList.__init__()

    def load(self,newnames=None):                           # ObsList.load()
        """Load the target files;
        If no list offered, try the self.targetnames
        Permit pandas df
        @ files
        csv files.
        TODO determine the format of this csv file -> pandas format.
        """
        extensionre = re.compile(r'.csv$',re.IGNORECASE)
        ret = None
        if(newnames is None):
            newnames = self.targetnames
        if(newnames is not None):                         # have a go
            if(type(targetnames) == type("")):            # its a string
                if(extensionre.search(targetname)):
                   # load pandas frame
            elif(f"{type(targetnames)}" == "<class 'pandas.core.frame.DataFrame'>"):
                # it is already a pandas frame
            else:
                ret = None
        else:
            if(ret is None):
                raise ObsListException(f"ObsList: don't know how to load {type(newnames)}")\
            raise ObsListException(self.debug(f"ObsList: Load fail {type(newnames)}"))
        return self
    ### ObsList.load()

    def debug(self,msg="",skip=[],os=sys.stderr):           # ObsList::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("ObsList - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### ObsList.debug()

    __ObsList_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class ObsList



##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    # (wg-python-atfiles)
    for filename in args:
        with open(filename,'r') if filename else sys.stdin as f:
            for l in f:
                if('#' in l):
                    continue
                parts = map(str.strip,l.split())

