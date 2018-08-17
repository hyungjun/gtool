#!/usr/bin/env python

from distutils.core import setup

setup( name                 = 'gtool',
       version              = '0.6',
       description          = 'gtool io sub module of coreFrame',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       url                  = '',
       package_dir          = {'gtool':'./'},
       packages             = ['gtool'],
       install_requires     = ['numpy'],
      )
