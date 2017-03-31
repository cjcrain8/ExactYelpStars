 #!/user/bin/python


"""

##################################################
##												##
## 	YELP STARS: CAL POSTING & MIN WAGE			##
## 												##
##	Chelsea Crain								##
##	12/03/2016									##
##												##
## 	Parses exact yelp stars by restaurant		##
##												##
##################################################


"""

from __future__ import print_function, division
from lxml import html
import csv, sys
from itertools import izip_longest
import itertools
from os.path import join, dirname, realpath
from pandas import Series, DataFrame
import pandas as pd
from os import path
from datetime import date
import fileinput
import os
import numpy
import time 
from shutil import copyfile
from selenium import webdriver
import time, os, re, codecs, math, random, csv, datetime
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import smtplib
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import sys

path = "C:\Users\Chelsea\Documents\Research\MinWage\YelpStars"

output_file_name = os.path.join(path, "yelp_stars_Feb2017.csv")


def get_done_list():

	try:
		df = pd.read_csv(output_file_name)
		done_list = df['url'].tolist()
	except:
		file = open(output_file_name, 'w')
		file.write("url" + "," + 'feb17' + "\n")
		file.close()
		df = pd.read_csv(output_file_name)
		done_list = df['url'].tolist()
	
	return done_list
	
		
def get_rest_list():

	df = pd.read_csv(os.path.join(path,"main_restaurants.csv"))
	return (df['url'].tolist())


def get_to_rest_page():
	
	opts = Options()

	opts.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
	
	driver = webdriver.Chrome('C:\Program Files (x86)'
				'\Google\Chrome\Application\chromedriver.exe', chrome_options=opts)
	
	return driver
	

def not_enough_reviews(rest):
	
	star_list =["NA"]
	output_file = open(output_file_name, 'a')	
	output_file.write(rest)
	for star in star_list:
		output_file.write("," + star)
	output_file.write('\n')
	output_file.close()
	print("Not enough reviews")
		
	
def main():
	
	try:
		rest_list = get_rest_list()
		done_list = get_done_list()	
		# print(done_list)
		
		driver = get_to_rest_page()
		i=0
		for rest in rest_list:
			# if i >1:
				# break
				
			if rest in done_list:
				print("already got this one: %s" %rest)
				continue
			print(rest)
			url = "https://www.yelp.com" + rest
			driver.get(url)

				
			try:
				details = driver.find_element_by_class_name('rating-details').click()
			
			except:
				not_enough_reviews(rest)
				continue
			
			
			star_list = []
			
			
			month = 1 # Feb is second month
			done = False
			right = 15
			while done == False:
				print("month # %s" %month)
				up = 0
				# start = driver.find_element_by_class_name('flot-base')
				try:
					start = driver.find_elements_by_xpath('//*[@class="flot-tick-label tickLabel"]')[month]
					
				except:
					star_list.append("NA")
					month+=1
					if len(star_list)==1:
						done = True
					
					continue
					
				found_stars = False
				while found_stars == False:
					up = up - 10
					# print(up)
					action = webdriver.common.action_chains.ActionChains(driver)
					action.move_to_element_with_offset(start, right, up)
					# action.click()
					action.perform()
					try:
						stars = driver.find_element_by_xpath('//*[@class="js-flotTooltip u-absolute"]')
						# print("FOUND EM!!")
						# print(stars.text)
						star_list.append(stars.text)
						found_stars = True
						
					except:
						found_stars = False
					
					if up < -210:
						print("OH SHITTTTTT")
						star_list.append("NA")
						# details = driver.find_element_by_class_name('rating-details').click()
						found_stars = True
						# time.sleep(10)

					
				# right = right + 42
				
				# if right > 470:
					# right = 470

				if len(star_list)==1:
					done = True
					
				month+=1
			i+=1
				
			output_file = open(output_file_name, 'a')	
			output_file.write(rest)
			for star in star_list:
				output_file.write("," + star)
			output_file.write('\n')
			output_file.close()
	except:
		sys.exit()
	
	print("all done!!!")
	time.sleep(60)
	
	
if __name__ == '__main__':
    main()
	
	
	
	
	
	
	
	
	
	
	
	
	
	