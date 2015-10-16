#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gtcfg.py
# CREATED BY : hjkim @IIS.2015-07-31 12:33:08.944683
# MODIFED BY :
#
# USAGE      : $ ./gtcfg.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser
from    cf.util.LOGGER  import *

import  struct

class __gtConfig__(object):

    hdrsize     = 1032          # = 4+1024+4

    chksumHdr   = list( struct.pack( '>i4', hdrsize-8 ) ) # w/o checksum



@ETA
def main(args,opts):
    print args
    print opts

    return


if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    parser  = OptionParser(usage=usage,version=version)

#    parser.add_option('-r','--rescan',action='store_true',dest='rescan',
#                      help='rescan all directory to find missing file')

    (options,args)  = parser.parse_args()

#    if len(args) == 0:
#        parser.print_help()
#    else:
#        main(args,options)

#    LOG     = LOGGER()
    main(args,options)


