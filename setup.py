#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 打包成 pip 包：http://xiaoh.me/2015/12/11/python-egg/

from setuptools import setup, find_packages

setup(
    name = "tornado_directmail_aliyun",
    version = "1.0.2",
    keywords = ("pip", "aliyun", "tornado", "directmail"),
    description = "aliyun directmail sdk",
    long_description = "aliyun directmail sdk for tornado",
    license = "MIT Licence",

    url = "https://github.com/haozi3156666/tornado-ali-directmail.git",
    author = "haolee",
    author_email = "haolee1990@qq.com",

    packages=['tornado_directmail'],
    include_package_data = True,
    platforms = "any",
    install_requires = []
)