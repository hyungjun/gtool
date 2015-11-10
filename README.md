# gtool io submodule

Installation
------------
$ python setup.py install

Dependency
----------
numpy only

Chunk-wise Access
-----------------
### Read .gt file
```python
In [1]: from gtool import gtopen

In [2]: for i, chunk in enumerate( gtfile ): print '%3i'%i, chunk.data.shape, chunk.header['DATE']
  0 (1, 2, 360, 720) 20000101 120000
  1 (1, 2, 360, 720) 20000102 120000
  2 (1, 2, 360, 720) 20000103 120000
.
.
.
363 (1, 2, 360, 720) 20001229 120000
364 (1, 2, 360, 720) 20001230 120000
365 (1, 2, 360, 720) 20001231 120000
```

### Write .gt file
```python
In [1]: from gtool import gtopen

```

Variable-wise Access
--------------------

### Read gt file

```python
In [1]: from gtool import gtopen

In [2]: gt=gtopen('Wg')

In [3]: gt.vars
Out[3]: OrderedDict([('GLW', GLW, (365, 6, 360, 720) : >f4)])
```

### Modify gt file

```python
In [1]: from gtool import gtopen

In [2]: gt=gtopen('./RSTA190101')

In [3]: for k,v in gt.vars.items(): v.header['DATE']='19010101 000000 '
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
/data1/hjkim/ELSE/miroc/data_med/hlf/<ipython-input-3-541e035fb23e> in <module>()
----> 1 for k,v in gt.vars.items(): v.header['DATE']='19010101 000000 '

/usr/local/lib/python2.7/dist-packages/cf2/io/gtool/gthdr.pyc in __setitem__(self, k, v)
    227         for __header__, v in map(None, self.__headers__, v):
    228             __header__[idx] = v if type(v) == str and len( v ) == 16 else \
--> 229                               fmt%fn( v )
    230
    231

RuntimeError: array is not writeable

In [4]: gt=gtopen'./RSTA190101', 'r+')

In [5]: for k,v in gt.vars.items(): v.header['DATE']='19010101 000000 '

In [6]: gt.vars['GLG'].header
Out[6]:

[00]  IDFM   :            9010:  DSET   :GPCC.n-v1.1     :  ITEM   :GLG             :
[03]  EDIT1  :                :  EDIT2  :                :  EDIT3  :                :
[06]  EDIT4  :                :  EDIT5  :                :  EDIT6  :                :
[09]  EDIT7  :                :  EDIT8  :                :  FNUM   :               1:
[12]  DNUM   :               1:  TITL1  :soil temperature:  TITL2  :                :
[15]  UNIT   :K               :  ETTL1  :                :  ETTL2  :                :
[18]  ETTL3  :                :  ETTL4  :                :  ETTL5  :                :
[21]  ETTL6  :                :  ETTL7  :                :  ETTL8  :                :
[24]  TIME   :               0:  UTIM   :HOUR            :  DATE   :19010101 000000 :
[27]  TDUR   :               0:  AITM1  :GLON720M        :  ASTR1  :               1:
[30]  AEND1  :             720:  AITM2  :GLAT360IM       :  ASTR2  :               1:
[33]  AEND2  :             360:  AITM3  :GLEVC6          :  ASTR3  :               1:
[36]  AEND3  :               6:  DFMT   :UR8             :  MISS   :  -0.9990000E+03:
[39]  DMIN   :  -0.9990000E+03:  DMAX   :  -0.9990000E+03:  DIVL   :  -0.9990000E+03:
[42]  DIVL   :  -0.9990000E+03:  STYP   :               1:  COPTN  :                :
[45]  IOPTN  :               0:  ROPTN  :   0.0000000E+00:  DATE1  :19790101 000000 :
[48]  DATE2  :19790101 000000 :  MEMO1  :                :  MEMO2  :                :
[51]  MEMO3  :                :  MEMO4  :                :  MEMO5  :                :
[54]  MEMO6  :                :  MEMO7  :                :  MEMO8  :                :
[57]  MEMO9  :                :  MEMO10 :                :  CDATE  :20120116 142510 :
[60]  CSIGN  :MIROC           :  MDATE  :20120116 142510 :  MSIGN  :MIROC           :
[63]  SIZE   :         1555200:
```
