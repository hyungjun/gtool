#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : __init__.py
# CREATED BY : hjkim @IIS.2015-07-30 13:33:35.971884
# MODIFED BY :
#
# USAGE      : $ ./__init__.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    gtfile          import gtFile           as gtopen


def main(args,opts):
    print( args )
    print( opts )

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


