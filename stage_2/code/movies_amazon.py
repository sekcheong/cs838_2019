#import scrapy
from bs4 import BeautifulSoup
import requests
import re
import csv
#html = requests.get('https://www.walmart.com/browse/movies-tv-shows/movies/4096_530598?cat_id=4096_530598_530698&redirect=true#searchProductResult').text
#soup = BeautifulSoup(html, 'html.parser')
#for x in soup.find_all(class_ = "product-title-link line-clamp line-clamp-2"):
#	print x['href']

count1=0
count2=0

movie_tuples = []

class Movie:
	name = ""
	subtext = ""
	duration = ""
	genre = ""
	release_date = "" 
	country = ""
	language = ""
	directors = ""
	stars = ""


def get_movie_tuples(movie_links):
	global count1
	global count2
	for link in movie_links:
		count1 = count1 +1
		print link
		html = requests.get(link).text
		soup = BeautifulSoup(html, 'html.parser')
		#print soup
		movie = Movie()
		
		if(soup.find(class_="ProductTitle")):
			movie.name = soup.find(class_="ProductTitle").string.strip()
		else:
			continue
		print movie.name

		table = soup.find('tbody')
		if(not table):
			count2=count2 +1
			#print count1
			#print count2
			continue
		for tr in table.children:
			tds = list(tr.children)
			td1 = tds[0].text.strip()
			td2 = tds[1].text.strip()
			if(td1== "Duration"):
				movie.duration = td2
				print movie.duration
			elif(td1 == "Movie Genre"):
				movie.genre = td2
				print movie.genre
			elif(td1 == "Release Date"):
				movie.release_date = td2
				print movie.release_date
			elif(td1 == "Actors"):
				movie.stars = td2
				print movie.stars
			elif(td1 == "Director"):
				movie.directors = td2


			
		#print "movie.name: " + movie.name
		
		'''
		if(soup.find('time')):
			movie.duration = soup.find('time').string.strip()
		#print "movie.duration: " + movie.duration

		genres = []
		for x in soup.find_all(href=re.compile("genres&ref_=tt_ov_inf$")):
			genres.append(x.string.strip())
		genres = list(set(genres))
		for genre in genres:
			movie.genre = movie.genre + genre + ", "
		movie.genre = movie.genre[:-2]
		#print "movie.genre: " + movie.genre

		#movie.release_date = soup.find(href=re.compile("releaseinfo?ref_=tt_ov_inf$")).string
		movie.release_date = soup.find(title = "See more release dates").string.strip()
		#print "movie.release_date: " + movie.release_date

		movie.country = soup.find(href = re.compile("country_of_origin")).string
		#print "movie.country: " + movie.country
		
		movie.language = soup.find(href = re.compile("language")).string
		#print "movie.language: " + movie.language

		for x in soup.find_all(href = re.compile("/?ref_=tt_ov_dr$")):
			movie.directors = movie.directors + x.string.strip() + ", "
		movie.directors = movie.directors[:-2]
		#print "movie.directors: " + movie.directors
		
		#movie.stars = 
		stars = soup.find_all(href = re.compile("/?ref_=tt_ov_st_sm$"))
		stars.pop()
		for x in stars:
			movie.stars = movie.stars + x.string.strip() + ", "
		movie.stars = movie.stars[:-2]
		#print "movie.stars: " + movie.star
		'''
		movie_tuples.append(movie)
		print "###########tuples number:" + str(len(movie_tuples))

		

def get_movie_links(page_link, number):
	print "##################################"
	print len(movie_tuples)

	link = page_link
	html = requests.get(link).text
	soup = BeautifulSoup(html, 'html.parser')

	movie_links = []
	for x in soup.find_all(class_ = "product-title-link line-clamp line-clamp-2"):
		movie_links.append("https://www.walmart.com"+x['href'])

	#print movie_links
	get_movie_tuples(movie_links);

	#next_link = 
	#print next_link
	#if(len(movie_tuples)>=number):
	#	return
	#else:
	#	get_movie_links(next_link)




if __name__ == '__main__':
	#action = 25*35 
	get_movie_links('https://www.walmart.com/browse/movies-tv-shows/movies/4096_530598?cat_id=4096_530598_530698&redirect=true#searchProductResult', 1000)
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies-tv-shows/movies/4096_530598/?page=' + str(x)+ '&cat_id=4096_530598_530698&redirect=true', 1000)
	#comedy >=1000
	#get_movie_links('https://www.imdb.com/search/title?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=75c37eae-37a7-4027-a7ca-3fd76067dd90&pf_rd_r=W368VY09EEK5RCWHRX71&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1', 100)
	#animation >=1000
	#get_movie_links('https://www.imdb.com/search/title?genres=animation&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=W368VY09EEK5RCWHRX71&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_1', 150)
	
	print len(movie_tuples) 
	movie_tuples = list(set(movie_tuples))
	with open('test1.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['name', 'duration', 'genre', 'release_date', 'country', 'language', 'directors', 'stars'])
		for movie in movie_tuples:
			#print movie.name + ";" + movie.duration + ";" + movie.genre + + ";" + movie.release_date + ";" + movie.country + ";" + movie.language + ";" + movie.directors + ";" + movie.stars
			writer.writerow([movie.name.encode('utf-8'), movie.duration.encode('utf-8'), movie.genre.encode('utf-8'), movie.release_date.encode('utf-8'), movie.country.encode('utf-8'), movie.language.encode('utf-8'), movie.directors.encode('utf-8'), movie.stars.encode('utf-8')])








