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


class DimensionPreset( object ):
    presets     = {
                    'GLON': [ 'linear', ( 0, 360) ],
                    'GLAT': [ 'linear', (-90, 90) ],
            }
    pass


class gtDim( DimensionPreset ):

    def __init__( self, dimcode ):
        '''
        dimcode     <str>       ex) 'GLON360IM'
        '''

        self.dimcode            = dimcode
        dimid, nitem, auxcode   = self.decode_dimecode()

        self.dimid              = dimid
        self.nitem              = int( nitem )
        self.auxcode            = '' if auxcode == None     else auxcode

        self.coords             = self.get_coords()


    def decode_dimecode( self ):
        '''
        @return
        dimid, nitem, auxcode
        '''
        return re.match( r'^([A-Z]+)(\d+)([A-Z]+)?', self.dimcode ).groups()


    def get_coords( self ):

        if not self.dimid in self.presets:
            raise KeyError, '{} is not defined yet.'.format(self.dimid)

        else:
            crdtype, bounds     = self.presets[ self.dimid ]

        if crdtype == 'linear':

            offset  = abs( (bounds[0] - bounds[1]) / 2. / self.nitem ) if 'M' in self.auxcode   \
                 else 0

            coords  = np.linspace( bounds[0]+offset, bounds[1]-offset, self.nitem )

        else:
            raise ValueError, '{} is not supported yet.'.format( crdtype )
         

        if 'I' in self.auxcode:
            return coords[::-1]

        else:
            return coords


    def __repr__(self):

        strDim      = ['\n   ** DIMENSIONS **   ',]
        dimFmt      = '[ %s]  %-16s :%s, (%i)'
        axname      = ' '

        strDim.append( dimFmt%( axname, 
                                self.dimcode, 
                                self.coords,
                                #'[%s ... %s]'%(self.coords[0], self.coords[-1]) if self.coords != [] else '[]', 
                                len( self.coords ) ))
#        print(  '[%s ... %s]'%(str(aCrd[0]),str(aCrd[0])),  array([0.0])==[] )

        return '\n'.join(strDim)



def main(args,opts):
    print(  args )
    print(  opts )

    print gtDim( 'GLON360M'  )
    print gtDim( 'GLAT180IM' )


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


