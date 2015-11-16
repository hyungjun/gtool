#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gtfile.py
# CREATED BY : hjkim @IIS.2015-07-29 11:19:30.645538
# MODIFED BY :
#
# USAGE      : $ ./gtfile.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import time
import  os,sys
from    optparse                    import OptionParser


#import  struct

from    numpy                       import memmap, array, concatenate, resize, dtype

try:
    from    cf2.utils               import OrderedDict
except:
    from    collections             import OrderedDict

from    gtcfg                       import __gtConfig__
from    gtchunk                     import __gtChunk__
from    gtvar                       import __gtVar__
from    gthdr                       import __gtHdrFmt__


class gtFile( __gtHdrFmt__ ):
    '''
    gt=gtool(path, iomode,unit)

        * iomode : [
                    'r',    # read (native mode of numpy.memmap for existing file)
                    'r+',   # read and write (native mode of numpy.memmap for existing file)
                    'w',    # write
                    'ow'    # over write
                    ]

    # access ATTR
    gt.header[varName].DATE = '19990101 000000'
    gt.header[varName].UTIM = 'HOUR'        # ['HOUR','DAY'] only
    gt.header[varName].TDUR = 24

    gt.data = array()


    ******
    HEADER
    ******
    1  "IDFM":[int,"%16i",9010],                # req
    2  "DSET":[str,"%-16s",''],                 # req
    3  "ITEM":[str,"%-16s",''],                 # req
    4  "EDIT1":[str,"%-16s",''],
    5  "EDIT2":[str,"%-16s",''],
    6  "EDIT3":[str,"%-16s",''],
    7  "EDIT4":[str,"%-16s",''],
    8  "EDIT5":[str,"%-16s",''],
    9  "EDIT6":[str,"%-16s",''],
    10 "EDIT7":[str,"%-16s",''],
    11 "EDIT8":[str,"%-16s",''],
    12 "FNUM":[int,"%16i",1],
    13 "DNUM":[int,"%16i",1],
    14 "TITL1":[str,"%-16s",''],
    15 "TITL2":[str,"%-16s",''],
    16 "UNIT":[str,"%-16s",''],
    17 "ETTL1":[str,"%-16s",''],
    18 "ETTL2":[str,"%-16s",''],
    19 "ETTL3":[str,"%-16s",''],
    20 "ETTL4":[str,"%-16s",''],
    21 "ETTL5":[str,"%-16s",''],
    22 "ETTL6":[str,"%-16s",''],
    23 "ETTL7":[str,"%-16s",''],
    24 "ETTL8":[str,"%-16s",''],
    25 "TIME":[int,"%16i",0],
    26 "UTIM":[str,"%-16s",'HOUR'],
    27 "DATE":[str,"%-16s",'00000000 000000'],  # req
    28 "TDUR":[int,"%16i",0],
    29 "AITM1":[str,"%-16s",''],                # req
    30 "ASTR1":[int,"%16i",0],                  # req
    31 "AEND1":[int,"%16i",0],                  # req
    32 "AITM2":[str,"%-16s",''],                # req
    33 "ASTR2":[int,"%16i",0],                  # req
    34 "AEND2":[int,"%16i",0],                  # req
    35 "AITM3":[str,"%-16s",''],                # req
    36 "ASTR3":[int,"%16i",0],                  # req
    37 "AEND3":[int,"%16i",0],                  # req
    38 "DFMT":[str,"%-16s",''],
    39 "MISS":[float,"%16.7e",-999.],
    40 "DMIN":[float,"%16.7e",-999.],
    41 "DMAX":[float,"%16.7e",-999.],
    42 "DIVL":[float,"%16.7e",-999.],
    43 "DIVL":[float,"%16.7e",-999.],
    44 "STYP":[int,"%16i",1],
    45 "COPTN":[str,"%-16s",''],
    46 "IOPTN":[int,"%16i",0],
    47 "ROPTN":[float,"%16.7e",0.],
    48 "DATE1":[str,"%-16s",''],
    49 "DATE2":[str,"%-16s",''],
    50 "MEMO1":[str,"%-16s",''],
    51 "MEMO2":[str,"%-16s",''],
    52 "MEMO3":[str,"%-16s",''],
    53 "MEMO4":[str,"%-16s",''],
    54 "MEMO5":[str,"%-16s",''],
    55 "MEMO6":[str,"%-16s",''],
    56 "MEMO7":[str,"%-16s",''],
    57 "MEMO8":[str,"%-16s",''],
    58 "MEMO9":[str,"%-16s",''],
    59 "MEMO10":[str,"%-16s",''],
    60 "CDATE":[str,"%-16s",''],
    61 "CSIGN":[str,"%-16s",''],
    62 "MDATE":[str,"%-16s",''],
    63 "MSIGN":[str,"%-16s",''],
    64 "SIZE":[int,"%16i",0]
    '''

    def __init__(self, gtPath, mode='r', struct='native'):
        '''
        struct  : ['simple', 'native']
                   'simple' : uniform file structure (singel var)
                   'native' : contains multiple vars & dims
        '''

        if mode in ['r','c','r+']:
            self.__rawArray__   = memmap(gtPath, 'S1', mode)

        elif mode == 'w+':
            gtFile  = open(gtPath, 'w')
            gtFile.close()
            #self.__rawArray__   = memmap(gtPath, 'S1', 'r+')

            self.__rawArray__   = array([], 'S1')
            self.gtPath         = gtPath

        else:
            raise ValueError, '%s is not supported option'%mode


        self.curr       = 0
        self.hdrBytes   = __gtConfig__.hdrsize
        self.size       = self.__rawArray__.size

        self.__chunks__ = []
        self.__vars__   = OrderedDict()

        self.__pos__    = OrderedDict()

        self.struct     = struct

        if struct == 'simple':
            # cache varName for simple structure
            size            = self.pos[0]
            self.varName    = __gtChunk__( self.__rawArray__, 0, size ).header['ITEM'].strip()

        self.iomode     = mode
        self.__version__= __gtConfig__.version



    def __getitem__(self, k):
        return self.__chunks__[k]
        #pos     = self.chunks[k].pos
        #size    = self.chunks[k].size

        #rawArray= self.__rawArray__[pos: pos+size]

        #return __gtChunk__( pos, size, self.__rawArray__ )


#    @property
#    def chunks(self):
#        '''
#        for delayed process
#        '''
#        if not hasattr( self, '__chunk__'):
#            self.__chunks__ = [ chunk for chunk in self ]
#
#        return self.__chunks__



    @property
    def pos(self):

        if hasattr( self, '__pos__' ):
            return self.__pos__

        else:
            self.__pos__    = OrderedDict()

            pos             = 0
            defaultSize     = self.get_chunksize( 0 )

            while pos < self.size:

                chunkSize   = self.get_chunksize( pos ) if self.struct == 'native'  \
                     else defaultSize

                self.__pos__[ pos ] = chunkSize

                pos += chunkSize

        return self.__pos__



    @property
    def vars(self):

        s=time.time()
        if len( self.__vars__.keys() ) == 0 or not hasattr( self, '__vars__' ):

            self.__vars__   = OrderedDict()

            for chunk in self:#.__chunks__:

                # speed-up for 'simple' structure
                varName     = chunk.header['ITEM'].strip() if not hasattr( self, 'varName' )    \
                         else self.varName

                if not varName in self.__vars__:
                    self.__vars__[varName] = []

                self.__vars__[varName].append( chunk )

        return OrderedDict( [(k, __gtVar__(v) ) for k,v in self.__vars__.items()] )


    def get_chunksize(self, curr):
        if curr in self.__pos__.keys():
            return self.__pos__[ curr ]

        else:
            dataPos         = curr + self.hdrBytes

            dataSize        = self.__rawArray__[dataPos: dataPos+4]
            dataSize.dtype  = '>i4'
            dataSize        = 4+dataSize[0]+4

            chunkSize       = self.hdrBytes + dataSize

            self.__pos__[self.curr] = self.curr+chunkSize

            return chunkSize


    def __iter__(self):
        return self


    def next(self):

        if self.curr == self.size:
            self.curr   = 0
            raise StopIteration

        chunkSize       = self.get_chunksize( self.curr )
#        rawArray        = self.__rawArray__[ self.curr: self.curr+chunkSize ]
#        chunk           = __gtChunk__( rawArray )

        print '###',self.curr, chunkSize
        chunk           = __gtChunk__( self.__rawArray__, self.curr, chunkSize )

        self.curr += chunkSize

        return chunk


    def extend(self):
        return


    def append(self, Data, headers=None, **kwargs):
        '''
        Data    : nd-array in rank-4 (T, Z, Y, X)
        headers : <type>    in [ __gtHdr__, iterable, ]??,
        '''

        if headers == None:
            native_code = sys.byteorder == 'little' and '<' or '>'
            byteorder   = Data.dtype.byteorder
            byteorder   = byteorder if byteorder != '=' else native_code


            if byteorder == '<':
                Data        = Data.byteswap()
                byteorder   = '>'

            dtypedescr  = byteorder + Data.dtype.kind + str(Data.dtype.itemsize)
            Data.dtype  = dtypedescr

            Data        = Data.reshape(1,1,180,360)
            dfmt                        = self.dictDFMT[ Data.dtype ]
            aend4, aend3, aend2, aend1  = Data.shape

            kwargs[ 'AEND1' ]   = aend1,
            kwargs[ 'AEND2' ]   = aend2,
            kwargs[ 'AEND3' ]   = aend3,
            kwargs[ 'DFMT'  ]   = dfmt,
            kwargs[ 'SIZE'  ]   = aend1*aend2*aend3,


        if kwargs != {}:
            headers             = self.auto_fill( headers=headers, **kwargs )


        for data, header in map(None, Data, headers):

            chunk       = __gtChunk__( data, header=header )
            self.__chunks__.append( chunk )

            varName     = header[2].strip()

            if not varName in self.__vars__:
                self.__vars__[varName] = []

            self.__vars__[varName].append( chunk )

            # write to memmap --------------------------------------------------
            pos         = self.__rawArray__.size
            #size        = 4+len(header)+4 + 4+data.size+4

            __memmap__          = memmap( self.gtPath, 'S1', 'r+',
                                          shape=(self.__rawArray__.size+chunk.size)
                                        )
            __memmap__[pos:]    = chunk.__rawArray__
            self.__rawArray__   = __memmap__
            '''
            self.__rawArray__   = concatenate( [self.__rawArray__, chunk] )
            # in case using 'concatenate' need to add write routine
            '''
            # ------------------------------------------------------------------



class __gtDim__(gtFile):
    '''
    TODO
    i. to be integrated into class __gtHdr__
    ii. fix a bug for reading wrong value
    '''

    def __init__(self,crdNAME):
        '''
        crdNAME: list of pre-defined coordination name [AITM1, AITM2, AITM3]
        '''

        AITM1, AITM2, AITM3     = crdNAME

        self.__dictDim__        = OrderedDict()
        self.__dictDim__[ 'z' ] = array( self.get_coord( AITM3 )[1].flatten() )
        self.__dictDim__[ 'y' ] = array( self.get_coord( AITM2 )[1].flatten() )
        self.__dictDim__[ 'x' ] = array( self.get_coord( AITM1 )[1].flatten() )

        self.names  = (AITM3, AITM2, AITM1)


    def get_coord(self,crdName):
        srcFName    = 'GTAXLOC.%s'%crdName
        srcPath     = os.path.join(GTOOL_DIR,srcFName)

        self.curr       = 0
        self.hdrBytes   = 1032      # = 4+1024+4
        self.__rawArray__  = memmap(srcPath, 'S1', 'r')

        Headers, Vars   = self.scan_structure()

        crdName         = Vars.keys()[0]

        return crdName, Vars[crdName][0][:]


    def __getitem__(self,k):
        return self.__dictDim__[k]


    def __repr__(self):

        strDim      = ['\n   ** DIMENSIONS **   ',]
        dimFmt      = '[ %s]  %-16s :%s, (%i)'

        for crdName, axName in map( None, self.names, self.__dictDim__.keys() ):
            aCrd    = self.__dictDim__[axName]
            strDim.append( dimFmt%(axName, crdName, '[%s ... %s]'%(aCrd[0],aCrd[-1]) if aCrd != [] else '[]', len(aCrd)) )
#            print '[%s ... %s]'%(str(aCrd[0]),str(aCrd[0])),  array([0.0])==[]

        return '\n'.join(strDim)



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


