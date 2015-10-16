#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : gthdr.py
# CREATED BY : hjkim @IIS.2015-07-29 11:09:16.855574
# MODIFED BY :
#
# USAGE      : $ ./gthdr.py
#
# DESCRIPTION:
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse        import OptionParser


import  datetime

from    numpy           import array, dtype

try:
    from    cf2.utils   import OrderedDict
except:
    from    collection  import OrderedDict

from    gtcfg           import __gtConfig__


class __gtHdrFmt__(object):
    fmt = OrderedDict([
("IDFM",[int,"%16i",9010]),     ("DSET",[str,"%-16s",'']),      ("ITEM",[str,"%-16s",'']),      #00
("EDIT1",[str,"%-16s",'']),     ("EDIT2",[str,"%-16s",'']),     ("EDIT3",[str,"%-16s",'']),     #03
("EDIT4",[str,"%-16s",'']),     ("EDIT5",[str,"%-16s",'']),     ("EDIT6",[str,"%-16s",'']),     #06
("EDIT7",[str,"%-16s",'']),     ("EDIT8",[str,"%-16s",'']),     ("FNUM",[int,"%16i",1]),        #09
("DNUM",[int,"%16i",1]),        ("TITL1",[str,"%-16s",'']),     ("TITL2",[str,"%-16s",'']),     #12
("UNIT",[str,"%-16s",'']),      ("ETTL1",[str,"%-16s",'']),     ("ETTL2",[str,"%-16s",'']),     #15
("ETTL3",[str,"%-16s",'']),     ("ETTL4",[str,"%-16s",'']),     ("ETTL5",[str,"%-16s",'']),     #18
("ETTL6",[str,"%-16s",'']),     ("ETTL7",[str,"%-16s",'']),     ("ETTL8",[str,"%-16s",'']),     #21
("TIME",[int,"%16i",0]),        ("UTIM",[str,"%-16s",'HOUR']),  ("DATE",[str,"%-16s",'00000000 000000']),#24
("TDUR",[int,"%16i",0]),        ("AITM1",[str,"%-16s",'']),     ("ASTR1",[int,"%16i",1]),       #27
("AEND1",[int,"%16i",0]),       ("AITM2",[str,"%-16s",'']),     ("ASTR2",[int,"%16i",1]),       #30
("AEND2",[int,"%16i",0]),       ("AITM3",[str,"%-16s",'']),     ("ASTR3",[int,"%16i",1]),       #33
("AEND3",[int,"%16i",0]),       ("DFMT",[str,"%-16s",'UR4']),   ("MISS",[float,"%16.7e",-999.]),#36
("DMIN",[float,"%16.7e",-999.]),("DMAX",[float,"%16.7e",-999.]),("DIVL",[float,"%16.7e",-999.]),#39
("DIVL",[float,"%16.7e",-999.]),("STYP",[int,"%16i",1]),        ("COPTN",[str,"%-16s",'']),     #42
("IOPTN",[int,"%16i",0]),       ("ROPTN",[float,"%16.7e",0.]),  ("DATE1",[str,"%-16s",'']),     #45
("DATE2",[str,"%-16s",'']),     ("MEMO1",[str,"%-16s",'']),     ("MEMO2",[str,"%-16s",'']),     #48
("MEMO3",[str,"%-16s",'']),     ("MEMO4",[str,"%-16s",'']),     ("MEMO5",[str,"%-16s",'']),     #51
("MEMO6",[str,"%-16s",'']),     ("MEMO7",[str,"%-16s",'']),     ("MEMO8",[str,"%-16s",'']),     #54
("MEMO9",[str,"%-16s",'']),     ("MEMO10",[str,"%-16s",'']),    ("CDATE",[str,"%-16s",'']),     #57
("CSIGN",[str,"%-16s",'']),     ("MDATE",[str,"%-16s",'']),     ("MSIGN",[str,"%-16s",'']),     #60
("SIZE",[int,"%16i",0])                                                                         #63
    ])

    dictDFMT    = {'UR4':'>f4', dtype('>f4'):'UR4',
                   'UR8':'>f8', dtype('>f8'):'UR8',
                         }

    dictUTIM    = {'HOUR':datetime.timedelta(seconds=3600),
                   'SEC':datetime.timedelta(seconds=1),
                        }


    def __init__(self,header=None):
        if header != None:
            for (k,v),hdr in map(None,self.fmt.items(),header):
                self.__dict__[k]    = v[0](hdr.strip())

            self.dtype  = self.dictDFMT[self.DFMT]
            self.delT   = self.dictUTIM[self.UTIM] * self.TDUR
            self.dtime  = datetime.datetime.strptime(self.DATE,'%Y%m%d %H%M%S')


    def gen_header( self, header=None, **kwargs ):

        header  = [ v[1]%( v[2] if k not in kwargs else
                    v[0]( kwargs[k] )
                         )
                                    for k,v in self.fmt.items() ]

        return header


    def auto_fill( self, headers=None, **kwargs ):
        '''
        headers : <list> of header
        '''

        keys    = self.fmt.keys()

        if headers == None:

            header  = [ ( v[1]%v[2], ) for k,v in self.fmt.items() ]

            # for self.iomode == 'w+':
            kwargs[ "CSIGN" ]   = 'cf.io.gtool %s'%__gtConfig__.version
            kwargs[ "CDATE" ]   = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
            # ------------------------
        else:

            header  = zip(*headers)

            # for self.iomode == 'r+':
            kwargs[ "MSIGN" ]   = 'cf.io.gtool %s'%__gtConfig__.version
            kwargs[ "MDATE" ]   = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
            # ------------------------


        for k,v in kwargs.items():

            cast, fmt, default  = self.fmt[k]

            V   = (v, ) if not type(v) in [list, tuple] else v

            header[ keys.index(k) ] =  [ fmt%( cast(v) ) for v in V ]


        nMax    = max( [len(h) for h in header] )

        header  = [ h if len(h) == nMax else h*nMax
                            for h in header ]

        return zip(*header)


    '''
    def str2dict(self,header):
        return OrderedDict( ( k, v[0](hdr.strip()) ) for (k,v),hdr in map(None,self.fmt.items(),header) )
    '''


class __gtHdr__(__gtHdrFmt__):

    def __init__(self, headers=None, **kwargs):
        '''
        headers : <list> : __memmap__<S16>
        '''

        # when header == None (e.g., newly generated gtfile) -------------------
        if headers == None or kwargs != {}:

            self.__headers__    = self.auto_fill( headers, **kwargs )
        # ----------------------------------------------------------------------

        else:
            self.__headers__    = headers
            #self.__headers__    = headers    if type( headers ) == list   else [ headers ]

        self.keys           = self.fmt.keys()


    @property
    def __get_str__(self):

        chksumHdr   = list( struct.pack( '>i4', self.hdrBytes-8 ) ) # w/o checksum
        header      = list( ''.join(header) )

        [ list( ''.join( __header__ ) ) for __header__ in self.__headers__]

        return


    @property
    def __hdr__(self):


        __hdr__     = [ attr[0] if len(set( attr )) == 1 else
                        attr
                                    for attr in zip(*self.__headers__) ]

        return __hdr__


    def template(self, **kwargs):
        __headers__ = array( self.__headers__[:] )

        return self.auto_fill(__headers__, **kwargs)


    def __repr__(self):
        hdr         = self.__hdr__

        nCol        = 3

        put2note    = [ k for k, v in map( None, self.keys, hdr ) if hasattr( v, '__iter__' ) ]

        '''
        for k,v in map( None, self.keys, hdr ):
            print k,v
        print self.keys.index(k), hdr[63]
        print put2note
        '''

        strOut      = [ ]
        Line        = ['[00]  ']


        for i in range(0, len( hdr ), nCol):
            strOut.append(  '[%02d]  '%i
                          + ''.join( ['%-6s :%s:  '%(k, v if k not in put2note else
                                      '   ** NOTE **   ')
                                                 for k, v  in map( None,
                                                                   self.keys[i:i+nCol],
                                                                   hdr[i:i+nCol] )
                                      ] )
                          )

        if put2note == []:
            return '\n'+'\n'.join(strOut)+'\n'


        # when put2noet != [] --------------------------------------------------
        strNote     = ['\n   ** NOTE **   ',]
        noteFmt     = '[%02d]  %-6s :%s, (%i)'

        for k in put2note:
            idx = self.keys.index( k )
            v   = hdr[ idx ]

            if not hasattr(v, '__iter__'):  v = [v]

            strNote.append( noteFmt%( idx, k, '[%s ... %s]'%(v[0], v[-1]), len(v) ) )

        return '\n'+'\n'.join(strOut + strNote)+'\n'
        # ----------------------------------------------------------------------


    def __getitem__(self,k):
        hdr         = self.__hdr__

        return hdr[ self.keys.index(k) ]


    def __setitem__(self, k, v):

        fn, fmt, default    = self.fmt[k]
        idx                 = self.fmt.keys().index(k)

        if not hasattr(v, '__iter__') :
            v   = [v] * len( self.__headers__)


        for __header__, v in map(None, self.__headers__, v):
            __header__[idx] = v if type(v) == str and len( v ) == 16 else \
                              fmt%fn( v )


#        print self.__headers__
#        print type( self.__headers__ )
#        print v, type(v), len(v), len( fmt%v )
        return



    '''
    def __setitem__(self,k,v):
#        if k not in ['TIME','dIdx','mIdx']: self.__dictHdr__[k]  = self.fmt[k][0](v)
        if k not in ['TIME','dIdx','mIdx']: self.__dictHdr__[k]  = self.fmt[k][1]%v
        else                              : self.__dictHdr__[k]  = v
    '''


    '''
    def __iter__(self):
        for key in self.__dictHdr__:
            yield key
    '''


    '''
    @property
    def template(self):
        Template    = []
        for _k,_v in self.header.items():
            if _k in ['dIdx','mIdx']:   continue    # skip records for file structure

            if type(_v) not in [list,tuple]:
                _v  = __gtHdrFmt__.fmt[_k][0](_v)   # convert back to defalut type
                Template.append(self.fmt[_k][1]%_v)

            else:
                Template.append(_v)

        return Template
    '''


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


