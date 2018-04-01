# -*- coding: utf-8 -*-

from pimper.pimper import Pimper
import os


#src = r"G:\ICE-9\autism\Vah"
#src = r"C:\Python34\Projects\search_images\images"
dst = r"C:\Python34\Projects\pimp-my-collection\sorted_images"
unkn = r"C:\Python34\Projects\pimp-my-collection\sorted_images\unknown3"
#dst = r"C:\Python34\Projects\search_images\images\sorted"
#proxy_server = "46.101.168.186:5292"
#proxy_server = "94.177.236.219:1189" #https://hidemy.name/en/proxy-list/
#proxy_server = "203.74.4.6:80"
#proxy_server = "188.165.194.110:8888"
proxy_server = "163.172.175.210:3128"


#print (os.listdir(path=src))
#for i in os.listdir(path=src)[8:]:
#	print ("Now in", i, "full path:", src + r'\n'[:-1] + i)
#	pimper = Pimper(src + r'\n'[:-1] + i, src + r'\n'[:-1] + i, src + r'\n'[:-1] + i + r"\unknown", proxy_server=proxy_server, fast_proxy=True)
#	pimper.pimp()

#src = r"G:\ICE-9\autism\Vah\Love Live Sunshine"
#src = r"C:\Users\root\Pictures"
src = r"C:\Users\root\Downloads\mobi\new"
#src = r"C:\Users\root\Pictures\2ch.hk-b-163992165-images"
pimper = Pimper(src, dst, unkn, proxy_server=proxy_server, fast_proxy=True)
pimper.pimp()