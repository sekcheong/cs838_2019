#import scrapy
from bs4 import BeautifulSoup
import requests
import re
import csv

movie_tuples = {}

class Movie:
	#rating_score = ""
	def __init__(self):
		self.name = ""
		#subtext = ""
		self.duration = ""
		self.genre = ""
		self.release_date = "" 
		#self.country = ""
		#self.language = ""
		self.directors = ""
		self.stars = ""


def get_movie_tuples(movie_links):
	for link in movie_links:
		html = requests.get(link).text
		soup = BeautifulSoup(html, 'html.parser')
		movie = Movie()
		
		if(soup.find('h1', class_="")):
			movie.name = soup.find('h1', class_="").text.strip()
		else:
			continue
		#print "movie.name: " + movie.name

		if(soup.find('time')):
			movie.duration = soup.find('time').string.strip()
		else:
			movie.duration = " "
		#print "movie.duration: " + movie.duration

		genres = []
		for x in soup.find_all(href=re.compile("genres&ref_=tt_ov_inf$")):
			genres.append(x.string.strip())
		genres = list(set(genres))
		if(genres):
			for genre in genres:
				movie.genre = movie.genre + genre + ", "
			movie.genre = movie.genre[:-2]
		else:
			movie.genre = " "
		#print "movie.genre: " + movie.genre

		#movie.release_date = soup.find(href=re.compile("releaseinfo?ref_=tt_ov_inf$")).string
		if(soup.find(title = "See more release dates")):
			movie.release_date = soup.find(title = "See more release dates").string.strip()
		else:
			movie.release_date = " "
		'''
		#print "movie.release_date: " + movie.release_date
		if(soup.find(href = re.compile("country_of_origin"))):
			if(soup.find(href = re.compile("country_of_origin")).string):
				movie.country = soup.find(href = re.compile("country_of_origin")).string
		else:
			movie.country = " "
		#print "movie.country: " + movie.country
		
		if(soup.find(href = re.compile("language"))):
			if(soup.find(href = re.compile("language")).string):
				movie.language = soup.find(href = re.compile("language")).string
		else:
			movie.language = " "
		#print "movie.language: " + movie.language
		'''

		directors = soup.find_all(href = re.compile("/?ref_=tt_ov_dr$"))
		if(directors):
			for x in directors:
				movie.directors = movie.directors + x.string.strip() + ", "
			movie.directors = movie.directors[:-2]
		else:
			movie.directors = " "
		#print "movie.directors: " + movie.directors
		
		#movie.stars = 
		stars = soup.find_all(href = re.compile("/?ref_=tt_ov_st_sm$"))
		if(stars):
			stars.pop()
			for x in stars:
				movie.stars = movie.stars + x.string.strip() + ", "
			movie.stars = movie.stars[:-2]
		else:
			movie.stars = " "
		#print "movie.stars: " + movie.star
	
		movie_tuples[movie.name] = movie
		#print "###########tuples number:" + str(len(movie_tuples))



def get_movie_links(page_link, number):
	print "##################################"
	print len(movie_tuples)

	link = page_link
	html = requests.get(link).text
	soup = BeautifulSoup(html, 'html.parser')

	movie_links = []
	for x in soup.find_all(href=re.compile("/?ref_=adv_li_tt$")):
		movie_links.append("https://www.imdb.com"+x['href'])
	get_movie_tuples(movie_links);

	next_link = "https://www.imdb.com"+ soup.find(href = re.compile("ref_=adv_nxt$"))['href']
	#print next_link
	if(len(movie_tuples)>=number):
		return
	else:
		get_movie_links(next_link, number)




if __name__ == '__main__':
	#action >=1000
	get_movie_links('https://www.imdb.com/search/title?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=W368VY09EEK5RCWHRX71&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2', 1000)
	#comedy >=1000
	get_movie_links('https://www.imdb.com/search/title?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=75c37eae-37a7-4027-a7ca-3fd76067dd90&pf_rd_r=W368VY09EEK5RCWHRX71&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1', 2000)
	#animation >=1000
	get_movie_links('https://www.imdb.com/search/title?genres=animation&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=W368VY09EEK5RCWHRX71&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_1', 3000)
	
	print len(movie_tuples) 
	#movie_tuples = list(set(movie_tuples))
	print "write csv"
	with open('../data/movies_IMDb.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['name', 'duration', 'genre', 'release_date', 'directors', 'stars'])
		for name in movie_tuples:
			movie = movie_tuples[name]
			'''
			print movie.name.encode('utf-8') 
			print movie.duration.encode('utf-8') 
			print movie.genre.encode('utf-8') 
			print movie.release_date.encode('utf-8')
			print movie.country.encode('utf-8')
			print movie.language
			print movie.language.encode('utf-8')
			print movie.directors.encode('utf-8')
			print movie.stars.encode('utf-8')
			'''
			writer.writerow([movie.name.encode('utf-8'), movie.duration.encode('utf-8'), movie.genre.encode('utf-8'), movie.release_date.encode('utf-8'), movie.directors.encode('utf-8'), movie.stars.encode('utf-8')])

	print "done"






