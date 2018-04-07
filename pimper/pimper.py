# -*- coding: utf-8 -*-

import os
import sys
import shutil
import re
import selenium.webdriver.support.ui as ui
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException


#debug = True
debug = False

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Обязательные параметры:
	src - папка с картинками, которые нужно отсортировать
Необязательные параметры:
	dest - папка, в которую кидать отсортированные
	unknown - неопознанные
	chromedriver_location - путь к папке с chromedriver.exe,
		так же должен быть в переменной PATH
	proxy_server - адрес прокси-сервера в формате x.x.x.x:x
	fast_proxy - если прокси быстрое, то стоит поставить True
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Pimper:
	def __init__(self, src, dest=None, unknown=None, chromedriver_location=None, proxy_server=None, fast_proxy=False):

		if chromedriver_location is None:
			self.chromedriver_location = os.path.abspath(os.path.dirname(sys.argv[0])) + "\chromedriver_win32\chromedriver.exe"
		else:
			self.chromedriver_location = chromedriver_location
		if debug:
			print ("Chrome location:", self.chromedriver_location)

		if debug:
			print ("src:", src)
			print ("dest:", dest)

		self.f = open(r'C:\Python34\Projects\pimp-my-collection\text.txt', 'a')
		self.f.write('\n' + str(datetime.today()) + '\n')
		self.titles = []

		#Куда кидать отсортированные
		if dest is None:
			try:
				self.dest = os.path.abspath(os.path.dirname(sys.argv[0]))
				os.chdir(self.dest)
				os.mkdir("sorted_images")
			except OSError:
				if debug:
					print ("dest folder already exists")
				pass
			finally:
				self.dest = (self.dest + "\sorted_images")
				os.chdir(self.dest)
		else:
			self.dest = dest
			try:
				os.chdir(self.dest)
			except FileNotFoundError:
				print ("No such directory:", self.dest)
				exit(1)

		#Папка для картинок без сурса
		if unknown is None:
			try:
				os.mkdir("unknown")
			except OSError:
				if debug:
					print ("unkn folder already exists")
				pass
			finally:
				self.unknown = self.dest + r"\unknown"
		else:
			self.unknown = unknown
			try:
				os.mkdir(self.unknown)
			except OSError:
				if debug:
					print ("unknown folder already exists")
				pass

		if debug:
			print ("dest:", self.dest)
			print ("unknown:", self.unknown)

		#Откуда берем картинки
		self.folder = src
		try:
			self.images = os.listdir(path=self.folder)
		except FileNotFoundError:
			print ("No such directory:", self.folder)
			exit(1)

		if debug:
			for i in self.images:
				try:
					print (i)
				except UnicodeEncodeError:
					i = i.encode('ascii', 'ignore')
					print ("bad unicode:", i)

		self.sleep_time = 3
		self.proxy_sleep_time = 3
		self.waiting_time = 15
		self.fast_proxy = fast_proxy
		#Новая версия - новая прокси
		from selenium.webdriver import Proxy
		if proxy_server is None:
			proxy_server = "163.172.175.210:3128" #https://free-proxy-list.net/
			settings = {
			        "httpProxy": proxy_server,
        			"sslProxy": proxy_server
			    }
			self.proxy_server = Proxy(settings)
		else:
			settings = {
			        "httpProxy": proxy_server,
        			"sslProxy": proxy_server
			    }
			self.proxy_server = Proxy(settings)

		from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
		from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
		cap = DesiredCapabilities.CHROME.copy()
		cap['platform'] = "WINDOWS"
		cap['version'] = "10"
		#Без прокси
		self.driver = ChromeDriver(desired_capabilities=cap, executable_path=self.chromedriver_location)

		#С прокси
		self.proxy_server.add_to_capabilities(cap)
		self.driver2 = ChromeDriver(desired_capabilities=cap, executable_path=self.chromedriver_location)

	def find_on_yandere(self):
		try:
			source = self.driver.find_element_by_class_name('tag-type-copyright')
		except NoSuchElementException:
			if debug:
				print ("no source")
			return None

		if debug:
			print (source)
			print (source.text)

		source2 = source.find_elements_by_css_selector('a')

		if debug:
			print (source2)
			for i in source2:
				print (i.text)
				print (i.get_attribute('href'))

			print (source2[1].text)

		return source2[1].text

	def find_on_sankaku(self, addr):
		try:
			source = self.driver2.find_element_by_class_name('tag-type-copyright')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except TimeoutException:
			if debug:
				print ("time out")
			self.driver2.get(addr)
			sleep(self.proxy_sleep_time)
			source = self.driver2.find_element_by_class_name('tag-type-copyright')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except NoSuchElementException:
			if not self.fast_proxy:
				if debug:
					print ("no element")
				self.driver2.get(addr)
				sleep(self.proxy_sleep_time)

				try:
					source = self.driver2.find_element_by_class_name('tag-type-copyright')
					sleep(self.proxy_sleep_time)
				except NoSuchElementException:
					if debug:
						print ("actually no element")
					return None
			else:
				return None

		if debug:
			print (source)
			print (source.text)

		if not self.fast_proxy:
			sleep(self.proxy_sleep_time)

		try:
			source2 = source.find_elements_by_css_selector('a')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except TimeoutException:
			sleep(self.proxy_sleep_time)

		if debug:
			print (source2)
			for i in source2:
				print (i.text)
				print (i.get_attribute('href'))

			print (source2[0].text)

		return source2[0].text

	def find_on_eshuushuu(self):
		got_source = False
		source = self.driver.find_elements_by_class_name('quicktag')
		check = self.driver.find_elements_by_tag_name('dt')

		if debug:
			for i in source:
				it = i .text
				try:
					print (it)
					print (i.get_attribute('span'))
				except UnicodeEncodeError:
					it = it.encode('ascii', 'ignore')
					print ("bad unicode:", it)

			print (check)
			print ("possible source:", source[1].text[1:len(source[1].text)-1])

		for i in check:
			if debug:
				print (i.text)
			if i.text.find("Source") != -1:
				return source[1].text[1:len(source[1].text)-1]

		return None

	def find_on_danbooru(self, addr):
		try:
			source = self.driver2.find_element_by_class_name('category-3')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except TimeoutException:
			if debug:
				print ("time out")
			self.driver2.get(addr)
			sleep(self.proxy_sleep_time)
			source = self.driver2.find_element_by_class_name('category-3')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except NoSuchElementException:
			if not self.fast_proxy:
				if debug:
					print ("no element")
				self.driver2.get(addr)
				sleep(self.proxy_sleep_time)

				try:
					source = self.driver2.find_element_by_class_name('category-3')
					sleep(self.proxy_sleep_time)
				except NoSuchElementException:
					if debug:
						print ("actually no element")
					return None
			else:
				return None

		if debug:
			print (source)

		try:
			source2 = source.find_elements_by_css_selector('a')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except TimeoutException:
			if debug:
				print ("time out source 2")
			sleep(self.proxy_sleep_time)

		if debug:
			print (source2)
			for i in source2:
				print (i.text)
				print (i.get_attribute('href'))

			print ("source:", source2[1].text)

		return source2[1].text

	def find_on_gelbooru(self, addr):
		try:
			source = self.driver2.find_element_by_class_name('tag-type-copyright')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except TimeoutException:
			if debug:
				print ("time out")
			self.driver2.get(addr)
			sleep(self.proxy_sleep_time)
			source = self.driver2.find_element_by_class_name('tag-type-copyright')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except NoSuchElementException:
			if not self.fast_proxy:
				if debug:
					print ("no element")
				self.driver2.get(addr)
				sleep(self.proxy_sleep_time)

				try:
					source = self.driver2.find_element_by_class_name('tag-type-copyright')
					sleep(self.proxy_sleep_time)
				except NoSuchElementException:
					if debug:
						print ("actually no element")
					return None
			else:
				return None

		if debug:
			print (source)

		try:
			source2 = source.find_elements_by_css_selector('a')
			if not self.fast_proxy:
				sleep(self.proxy_sleep_time)
		except TimeoutException:
			if debug:
				print ("time out source 2")
			sleep(self.proxy_sleep_time)

		if debug:
			print (source2)
			for i in source2:
				print (i.text)
				print (i.get_attribute('href'))

			print ("source:", source2[1].text)

		return source2[1].text

	def move_image(self, folder_name):
		img = (self.img_name[1:len(self.img_name)]).encode('ascii', 'ignore')
		#Сурс не нашелся
		if folder_name is None:
			dest = (self.unknown).encode('ascii', 'ignore')
			try:
				if debug:
					print ("src:", self.folder + self.img_name)
					print ("dst:", dest)
				shutil.copy(self.folder + self.img_name, self.unknown)
				os.remove(self.folder + self.img_name)
				print ("image", img, "successfully moved in", dest)
			except:
				print ("Error while moving image", img)
		#Сурс найден
		else:
			dest = (self.dest + r'\n'[:-1] + folder_name).encode('ascii', 'ignore')
			#Убираем запрещенные символы для имени папки
			forbidden_symbols = re.findall('[*|\:"<>?/]', folder_name)
			for symb in forbidden_symbols:
				if debug:
					print (symb)
				folder_name = folder_name.replace(symb, "").lower()
			if debug:
				print ("new folder name:", folder_name)
			print ("writing...")
			if (folder_name not in self.titles):
				try:
					self.f.write(folder_name + '\n')
					self.titles.append(folder_name)
				except UnicodeEncodeError:
					pass
			try:
				os.mkdir(folder_name)
			except OSError:
				if debug:
					print ("folder", folder_name, "already exists")
				pass
			try:
				shutil.copy(self.folder + self.img_name, folder_name)
				os.remove(self.folder + self.img_name)
				print ("image", img, "successfully moved in", dest)
			except OSError:
				print ("Error while moving image", img)
			sleep(self.sleep_time)

	#Приоритет сайтов
	def sort_addresses(self, pic_addr):
		variants = self.driver.find_element_by_id('pages').find_elements_by_tag_name('td')
		if debug:
			print ("find %")
			for i in variants:
				try:
					print (i.text)
				except UnicodeEncodeError:
					new_i = i.text.encode('ascii', 'ignore')
					print ("bad unicode:", new_i)
			for addr in pic_addr:
				addr2 = addr.get_attribute('href')
				print ("trying", addr2)
			print ("1st variant:", variants[6].text, "len =", len(variants), "len var = ", len(variants[6].text))

		#Второе найденное similarity
		if len(variants[6].text) == 0:
			pos = 9
		else:
			pos = 10
		priority = 6
		best_addr = pic_addr[0].get_attribute('href')
		if (best_addr.find("danbooru")) != -1:
			if debug:
				print ("danbooru[0]")
			priority = 3
		elif (best_addr.find("sankaku")) != -1:
			if debug:
				print ("sankaku[0]")
			priority = 4
		elif (best_addr.find("gelbooru")) != -1:
			if debug:
				print ("gelbooru[0]")
			priority = 5
		elif (best_addr.find("shuushuu")) != -1:
			if debug:
				print ("shuushuu[0]")
			priority = 2
		elif (best_addr.find("yande")) != -1:
			if debug:
				print ("yandere[0]")
			priority = 1

		if priority > 1:
			for addr in pic_addr[1:len(pic_addr)]:
				addr2 = addr.get_attribute('href')

				if pos > len(variants):
					break
				similarity = int(re.search('\d+', variants[pos].text).group())
				if debug:
					print ("similarity =", similarity)
				#if similarity >= 70:
				if (addr2.find("danbooru")) != -1:
					if debug:
						print ("danbooru", priority)
					if priority > 3:
						best_addr = addr2
						priority = 3
				elif (addr2.find("sankaku")) != -1:
					if debug:
						print ("sankaku", priority)
					if priority > 4:
						best_addr = addr2
						priority = 4
				elif (addr2.find("gelbooru")) != -1:
					if debug:
						print ("gelbooru", priority)
					if priority > 5:
						best_addr = addr2
						priority = 5
				elif (addr2.find("shuushuu")) != -1:
					if debug:
						print ("shuushuu", priority)
					if priority > 2:
						best_addr = addr2
						priority = 2
						break
				elif (addr2.find("yande")) != -1:
					if debug:
						print ("yandere", priority)
					if priority > 1:
						best_addr = addr2
						priority = 1
						break

				pos += 4 #Следующее similarity

		if debug:
			print ("best_addr:", best_addr)
		return best_addr, priority

	def search_for_source(self, pic_addr):
		best_addr, priority = self.sort_addresses(pic_addr)
		folder_name = None

		if debug:
			print ("trying", best_addr)

		if priority == 1:
			print ("searching on yandere")
			try:
				self.driver.get(best_addr)
			except WebDriverException as inst:
				if debug:
					print (inst)
				exit(1)
			folder_name = self.find_on_yandere()
		elif priority == 4:
			print ("searching on sankaku")
			try:
				self.driver2.get(best_addr)
				sleep(self.proxy_sleep_time)
			except TimeoutException:
				if debug:
					print ("time out in if")
				sleep(self.proxy_sleep_time)
			except WebDriverException as inst:
				if debug:
					print (inst)
				exit(1)
			folder_name = self.find_on_sankaku(best_addr)
		elif priority == 2:
			print ("searching on e-shuushuu")
			try:
				self.driver.get(best_addr)
			except WebDriverException as inst:
				if debug:
					print (inst)
				exit(1)
			folder_name = self.find_on_eshuushuu()
		elif priority == 3:
			print ("searching on danbooru")
			try:
				self.driver2.get(best_addr)
				sleep(self.proxy_sleep_time)
			except TimeoutException:
				if debug:
					print ("time out in if")
				sleep(self.proxy_sleep_time)
			except WebDriverException as inst:
				if debug:
					print (inst)
				exit(1)
			folder_name = self.find_on_danbooru(best_addr)
		elif priority == 5:
			print ("searching on gelbooru")
			try:
				self.driver2.get(best_addr)
				sleep(self.proxy_sleep_time)
			except TimeoutException:
				if debug:
					print ("time out in if")
				sleep(self.proxy_sleep_time)
			except WebDriverException as inst:
				if debug:
					print (inst)
				exit(1)
			folder_name = self.find_on_gelbooru(best_addr)

		if folder_name is None:
			print ("No relevant match for", self.img_name[1:len(self.img_name)])
		self.move_image(folder_name)

	def iqdb_actions(self):
		for image in self.images:

			print ("\nprocessing", self.images.index(image) + 1, "of", len(self.images))

			self.img_name = r'\n'[:-1] + image

			if debug:
				try:
					print (self.folder + self.img_name)
				except UnicodeEncodeError:
					print ("bad unicode")
			sleep(self.sleep_time)

			if ((image[len(image)-4:] != ".jpg") and (image[len(image)-4:] != ".png") and (image[len(image)-5:] != ".jpeg")):
				try:
					print ("Unsupported format:", image)
				except UnicodeEncodeError:
					image = image.encode('ascii', 'ignore')
					print (image)
			else:
				self.driver.get("http://iqdb.org/")
				#Вставляем изображение
				element = ui.WebDriverWait(self.driver, self.waiting_time).until(lambda driver: self.driver.find_element_by_id("file"))

				if debug:
					print (element)

				element.send_keys(self.folder + self.img_name)

				#Сабмитим
				element  = ui.WebDriverWait(self.driver, self.waiting_time).until(lambda driver: self.driver.find_element_by_xpath("//input[@value='submit']"))

				if debug:
					print (element)

				try:
					element.click()
				except TimeoutException:
					sleep(self.sleep_time)

				sleep(self.sleep_time)

				#Ищем лучшее совпадение
				try:
					pic_addr = ui.WebDriverWait(self.driver, self.waiting_time).until(lambda driver: self.driver.find_elements_by_css_selector('.image a'))
				except TimeoutException:
					print ("Image", image, "is to o large")
					self.move_image(None)
				else:
					if debug:
						print (pic_addr)

					matches = ui.WebDriverWait(self.driver, self.waiting_time).until(lambda driver: self.driver.find_element_by_xpath('//*[@id="pages"]/div[2]/table/tbody/tr[1]/th'))

					if debug:
						print ("matches:", matches)
						print (matches.text)

					if (matches.text.find("No")) != -1:
						print (matches.text, "for", image)
						self.move_image(None)
					else:
						self.search_for_source(pic_addr)

					sleep(self.sleep_time)

	def pimp(self):
		if debug:
			print ("proxy mode:", self.fast_proxy)
		try:
			self.iqdb_actions()
		except KeyboardInterrupt:
			print ("Stop working...")
		finally:
			self.driver.quit()
			self.driver2.quit()
			self.f.close()
			print ("Job's done")