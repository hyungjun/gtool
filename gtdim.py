#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gtdim.py
# CREATED BY : hjkim @IIS.2018-08-15 11:19:30.645538
# MODIFED BY :
#
# USAGE      : 
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys,re
from    optparse                    import OptionParser

import  numpy       as np

from    coords                      import Coords


class __gtDim__( Coords ):

    def __init__( self, dimensions, dimnames=['AITM1', 'AITM2', 'AITM3'] ):

        print dimensions

        for dim, dname in map( None, dimensions, dimnames ):

            setattr( self, dname, Dimemsion( dim, dname ) )

        self.dimnames   = dimnames
            

    def __repr__(self):

        return '\n'.join( [ str( self.__dict__[ dname ] ) for dname in self.dimnames ] )


class Dimemsion( Coords ):

    def __init__( self, dimension, dimname ):
        '''
        @IN
        dimension   <str>       dimcode ex) 'GLON360IM'
                    <1d-array>  coordinates 

        dimname     <str>       gtool axis ['AITM1', 'AITM2', 'AITM3']

        e.g.) Dimemsion( 'GLON360M', 'AITM1' )

        @@ 'NUMBER' is default when if dimid (e.g., GLON, GLAT,..) has not been defind at ./coords
        '''

        if type( dimension ) == str:

            dimid, nitem, auxcode   = self.decode_dimecode( dimension )
            auxcode                 = '' if auxcode == None     else auxcode

            self.coords             = getattr( self, dimid, self.NUMBER )( int( nitem ), auxcode )
            self._dimcode           = dimension

            #if hasattr( self, dimid )   \
            #                     else '{} but used "NUMBER" because not pre-defined yet'.format( dimension )

        else:

            self.coords             = dimension

        self.dimname    = dimname


    @property
    def dimcode( self ):

        dimid   = self.decode_dimecode( self._dimcode )[0]
        dimcode = self._dimcode

        if hasattr( self, '_dimcode' ):
            return dimcode if hasattr( self, dimid )        \
              else '{} replaced with "NUMBER{}" because yet pre-defined'.format( self._dimcode, self.coords.size )

        else:
            return 'undefined'


    def decode_dimecode( self, dimension ):
        '''
        @return
        dimid, nitem, auxcode
        '''
        return re.match( r'^([A-Z]+)(\d+)([A-Z]+)?', dimension ).groups()


    def __repr__(self):

        strDim      = []
        dimFmt      = '** DIM [%s] %s (%i; %s) **'

        strcoords   = str( self.coords ) if self.coords.size < 8    \
                 else ' '.join( [ str( self.coords[:3] )[:-1], '...',
                                  str( self.coords[-3:])[1:] ] )

        strcoords   = '%-45s,'%strcoords

        strDim.append( dimFmt%( 
                                self.dimname, 
                                strcoords,
                                len( self.coords ),
                                self.dimcode,
                                ))
#        print(  '[%s ... %s]'%(str(aCrd[0]),str(aCrd[0])),  array([0.0])==[] )

        return '\n'.join(strDim)



def main(args,opts):
    print(  args )
    print(  opts )

    #print Dimemsion( 'GLON360M', 'AITM1'  )
    #print Dimemsion( 'GLAT180IM' )
    #print Dimemsion( np.linspace(-89.5,89.5,180), dimname='latitudes' )

    gtdim   = __gtDim__( ['GLON360M', 'GLAT180IM', 'WLEVC6'] )

    print gtdim

    #print gtdim.AITM1
    #print gtdim.AITM2
    #print gtdim.AITM3


    return


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


