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


import  os,sys,datetime
from    optparse        import OptionParser

from    numpy           import array, arange
from    gtfile          import gtFile   as gtopen
#from    cf2.GridCoordinates.regrid  import regrid


def test_chunkwise_encoding( aSrc, outPath ):
    gtOut       = gtopen( outPath, mode='w+' )

    print(  '\t## encoding (version: %s) ###'%gtOut.__version__ )
    print(  '\t   source array:', aSrc.shape, aSrc.dtype, 'Min:%s'%aSrc.min(), 'Max:%s'%aSrc.max() )
    print( )

    for a in aSrc:

        print(  '\t\tappend:', a.shape, a.min(), a.max() )
        gtOut.append( a )

    print( )
    print(  '\t   out path: %s'%outPath, gtOut.vars )
    print(  '='*80 )

    return True


def test_chunkwise_decoding( srcPath, aSrc ):
    gtSrc       = gtopen( srcPath, 'r' )
    print(  '\t## decoding (version: %s) ###'%gtSrc.__version__ )
    print(  '\t   source file:', srcPath )
    print( )

    Data    = []
    for chunk in gtSrc:

        data    = chunk.data
        print(  '\t\tget a chunk:', data.shape, data.min(), data.max(), data.dtype )

        Data.append( data )

    Data    = array( Data )
    chkFlag     = all(Data.flatten() == aSrc.flatten())

    print( )
    print(  '\t   identical to aSrc?', chkFlag, Data.shape )
    print(  '='*80 )

    return chkFlag


def test_modification( srcPath ):
    gtSrc       = gtopen( srcPath, 'r+' )#, struct='simple' )
    gtVar       = gtSrc.vars['']

    print(  '\t## modification (version: %s) ###'%gtSrc.__version__ )
    print(  '\t   source file:', srcPath )
    print( )

    print(  '\t origial header' )
    print(  gtVar.header )

    varName     = 'test'
    gtVar.header['ITEM']    = varName
    print(  '\t   set "ITEM" as "test"' )

    gtVar.header['UTIM']    = 'DAY'
    print(  '\t   set "UTIM" as "DAY"' )

    sDTime      = datetime.datetime(2000,1,1)
    delT        = datetime.timedelta(days=1)
    DTime       = [sDTime+delT*i for i in range( gtVar.shape[0] ) ]
    TStamp      = [dtime.strftime('%Y%m%d %H%M%S ') for dtime in DTime ]
    gtVar.header['DATE']    = TStamp
    print(  '\t   set "DATE" as %s - %s'%(TStamp[0], TStamp[-1]) )

    print(  gtVar.header )
    print(  '='*80 )

    chkFlag     = ( gtVar.header['DATE'] == tuple(TStamp) )     \
                 &( varName == gtVar.header['ITEM'].strip() )

    return chkFlag


def test_varwise_decoding( srcPath, aOri ):

    gtSrc       = gtopen( srcPath, 'r', struct='simple' )
    gtVar       = gtSrc.vars['test']

    print(  '\t## variable-wise decoding (version: %s) ###'%gtSrc.__version__ )
    print(  '\t   source file:', srcPath )
    print( )

    print(  '\t   variables in gt file:', gtSrc.vars )
    print(  '\t   "test" variable     :', gtVar )
    print(  '\t   header of "test" var:', gtVar.header )

    aSrc       = gtVar[:]

    for a in aSrc:

        print(  '\t\titer aSrc:', a.shape, a.min(), a.max() )

    print(  '='*80 )

    chkFlag     = all(aSrc.flatten() == aOri.flatten())

    print( )
    print(  '\t   identical to aOri?', chkFlag, aSrc.shape )
    print(  '='*80 )

    return chkFlag


def test_export_to_netcdf( srcPath, ncPath ):
    print '\t## export to netcdf ###'
    print '\t   source file:', srcPath
    print '\t   netcdf file:', ncPath

    gtSrc       = gtopen( srcPath, 'r' )
    gtVar       = gtSrc.vars[ 'test' ]

    print gtVar.export2nc( ncPath, mode='w' )

    return True


def main(args,opts):

    testFlag    = []        # flag for the entire test seq.

    outPath     = './test.gt'

    print( )
    print(  'testing cf.io.gtool...' )
    print( )

    aSrc        = arange(10*180*360).reshape(10,1,180,360)
    aSrc        = aSrc.astype('float32')
    print(  '='*80 )

    testFlag.append( test_chunkwise_encoding( aSrc, outPath ))
    testFlag.append( test_chunkwise_decoding( outPath, aSrc ))
    testFlag.append( test_modification( outPath )            )
    testFlag.append( test_varwise_decoding( outPath, aSrc )  )
    testFlag.append( test_export_to_netcdf( outPath, outPath[:-3]+'.nc' ) )


    print(  testFlag )

    return all( testFlag )

    '''
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

        print(  gt.header['ITEM'], gt.data.shape, gt.data.dtype, aOut.shape, aOut.dtype
    '''



if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    parser  = OptionParser(usage=usage,version=version)

#    parser.add_option('-r','--rescan',action='store_true',dest='rescan',
#                      help='rescan all directory to find missing file')

    (options,args)  = parser.parse_args()

#    if len(args) == 0:
#        parser.print( _help()
#    else:
#        main(args,options)

#    LOG     = LOGGER()
    main(args,options)


