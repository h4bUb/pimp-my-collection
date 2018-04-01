# -*- coding: utf-8 -*-

from pimper.pimper import Pimper
import os


dst = r"C:\Python34\Projects\pimp-my-collection\sorted_images"
unkn = r"C:\Python34\Projects\pimp-my-collection\sorted_images\unknown3"
proxy_server = "163.172.175.210:3128"
src = r"C:\Users\root\Downloads\mobi\new"
pimper = Pimper(src, dst, unkn, proxy_server=proxy_server, fast_proxy=True)
pimper.pimp()
