KSET.org 
========

Author: [Veljko Dragsic](https://github.com/veljkodragsic)



## Quick Guide

Use `virtualenv` to get things running.

    mkdir kset-org && cd kset-org
    virtualenv --no-site-packages env

    git clone git@github.com:KSET/kset-org.git kset



    cp kset/profile.example profile
    source profile

    pip install -r requirements.txt


## Requirements
  *  `python2.7` 
  *  `python2.7-dev` 
  *  `virtualenv` 
  *  `python-pip` 
  *  `libjpeg`, `libpng`, `libgif` (with `-dev` packages)
  *  `libsasl` (with `-dev`)
