#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : __main__.py
# CREATED BY : hjkim @IIS.2015-07-30 13:33:35.971884
# MODIFED BY :
#
# USAGE      : $ ./__main__.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser

from    cf2.io.gtool                import gtFile
from    cf2.GridCoordinates.regrid  import regrid


def main(args,opts):
    print args
    print opts

    srcPath     = args[0]
    outPath     = args[1]
#    srcPath     = 'Restart'
#    outPath     = 'Initial'

    nFold       = 2

    gtSrc       = gtFile( srcPath, 'r' )
    gtOut       = gtFile( outPath, mode='w+' )

    for gt in gtSrc:

        aOut    = regrid( gt.data, 2 )

        shp     = aOut.shape

        d       = {'AEND1': shp[3],
                   'AEND2': shp[2],
                   'AITM1': 'GLON%iM'%(shp[3]),
                   'AITM2': 'GLAT%iIM'%(shp[2]),
                   'SIZE' : reduce( lambda x,y:x*y, shp ),
                   }

        gtOut.append(aOut, gt.header.template( **d ))

        print gt.header['ITEM'], gt.data.shape, gt.data.dtype, aOut.shape, aOut.dtype


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


