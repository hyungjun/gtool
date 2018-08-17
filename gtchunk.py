#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gtchunk.py
# CREATED BY : hjkim @IIS.2015-07-29 13:53:41.653761
# MODIFED BY :
#
# USAGE      : $ ./gtchunk.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser


import  struct

from    numpy           import dtype, concatenate

from    gthdr           import __gtHdr__
from    gtcfg           import __gtConfig__



class __gtChunk__( __gtConfig__ ):

    def __init__(self, *args, **kwargs):
    #def __init__(self,  __rawArray__, header=None):
        '''
        /* decodeing mode */
        args    = [ __rawArray__, self.curr, chunkSize ]    # __rawArray__: entire gtool file
        kwargs  = {}

        /* encoding mode */
        args    = [ __rawArray__ ]                          # __rawArray__: appended/extended chunk
        kwargs  = {'header': ... }
        '''

        if 'header' in kwargs:
            # encoding mode

            __rawArray__    = args[0]
            header          = kwargs['header']

            __rawArray__    = self.chunking( __rawArray__, header )
            pos             = 0
            size            = __rawArray__.size

        else:
            # decoding mode
            __rawArray__, pos, size = args

        self.__rawArray__   = __rawArray__
        self.pos            = pos
        self.size           = size

        self.hsize          = self.hdrsize


    '''
    def __repr__(self):

        return self.header.__repr__()
    '''

    def chunking( self, data, header ):
        '''
        encoding header + data chunk
        '''

        chksumHdr   = __gtConfig__.chksumHdr
        header      = list( ''.join(header) )

        data.dtype  = 'S1'
        chksumData  = list( struct.pack( '>i4', data.size ) )

        chunk       = concatenate( [ chksumHdr, header, chksumHdr,
                                     chksumData, data.flatten(), chksumData ] )

        return chunk



    @property
    def header(self):

        sIdx    = self.pos + 4
        eIdx    = self.pos + self.hsize - 4

        __header__      = self.__rawArray__[sIdx:eIdx]

        __header__.dtype= 'S16'

        return __gtHdr__( [__header__] )


    @property
    def data(self):

        sIdx    = self.pos + self.hsize + 4
        eIdx    = self.pos + self.size - 4
        data    = self.__rawArray__[sIdx:eIdx]

        # NEED to consider ASTR1 :: e.g.) self.header['AEND3'] - self.header['ASTR3'] +1
        shape       = map( int, [
                                 self.header['AEND3'],
                                 self.header['AEND2'],
                                 self.header['AEND1']] )
        # ------------------------------------------------------------------------------

        data.dtype  = {''   :dtype('>f4'),
                       'UR4':dtype('>f4'),
                       'UR8':dtype('>f8')}[ self.header['DFMT'].strip() ]

        data.shape  = shape

        return data


def main(args,opts):
    print(  args )
    print(  opts )

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


