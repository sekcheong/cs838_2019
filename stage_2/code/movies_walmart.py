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

movie_tuples = {}

class Movie:
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
	global count1
	global count2
	for link in movie_links:
		count1 = count1 +1
		#print link
		html = requests.get(link).text
		soup = BeautifulSoup(html, 'html.parser')
		#print soup
		movie = Movie()
		
		if(soup.find(class_="ProductTitle")):
			movie.name = soup.find(class_="ProductTitle").string.strip()
		else:
			continue
		#print movie.name

		table = soup.find('tbody')
		if(not table):
			count2=count2 +1
			#print count1
			#print count2
			continue
		for tr in table.children:
			tds = list(tr.children)
			td1 = tds[0].text.strip()
			if(tds[1]):
				td2 = tds[1].text.strip()
			else:
				td2 = " "
			if(td1== "Duration"):
				movie.duration = td2
				#print movie.duration
			elif(td1 == "Movie Genre"):
				movie.genre = td2
				#print movie.genre
			elif(td1 == "Release Date"):
				movie.release_date = td2
				#print movie.release_date
			elif(td1 == "Actors"):
				movie.stars = td2
				#print movie.stars
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
		movie_tuples[movie.name] = movie
		#print "###########tuples number:" + str(len(movie_tuples))

		

def get_movie_links(page_link):
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
	#action
	get_movie_links('https://www.walmart.com/browse/movies-tv-shows/action-movies/4096_530598_530698')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies-tv-shows/movies/4096_530598/?page=' + str(x)+ '&cat_id=4096_530598_530698&redirect=true')
	print len(movie_tuples)
	#comedy 
	get_movie_links('https://www.walmart.com/search/?query=comedy%20movies&cat_id=0&typeahead=comedy')
	for x in range(2, 51):
		get_movie_links('https://www.walmart.com/search//?query=comedy%20movies&page=' + str(x)+ '&cat_id=0&typeahead=comedy')
	print len(movie_tuples)
	#drama
	get_movie_links('https://www.walmart.com/browse/movies/drama-movies/4096_530598_530705')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies/drama-movies/4096_530598_530705/?page=' + str(x)+ '&cat_id=4096_530598_530705')
	print len(movie_tuples)
	#kids
	get_movie_links('https://www.walmart.com/browse/movies/kids-movies/4096_530598_530701')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies/kids-movies/4096_530598_530701/?page=' + str(x)+ '&cat_id=4096_530598_530701')
	print len(movie_tuples)
	#science fiction
	get_movie_links('https://www.walmart.com/browse/movies/science-fiction-movies/4096_530598_530715')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies/science-fiction-movies/4096_530598_530715/?page=' + str(x)+ '&cat_id=4096_530598_530715')
	print len(movie_tuples)
	#Romance
	get_movie_links('https://www.walmart.com/browse/movies/romance-movies/4096_530598_530714')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies/romance-movies/4096_530598_530714/?page=' + str(x)+ '&cat_id=4096_530598_530714')
	print len(movie_tuples) 

	#classic
	get_movie_links('https://www.walmart.com/browse/movies-tv-shows/classic-movies/4096_530598_530702')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies-tv-shows/classic-movies/4096_530598_530702/?page=' + str(x)+ '&cat_id=4096_530598_530702')
	print len(movie_tuples)

	#animated
	get_movie_links('https://www.walmart.com/browse/movies/animated-movies/4096_530598_530699')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies/animated-movies/4096_530598_530699/?page=' + str(x)+ '&cat_id=4096_530598_530699')
	print len(movie_tuples)

	#musical
	get_movie_links('https://www.walmart.com/browse/movies-tv-shows/musical-movies/4096_530598_530712')
	for x in range(2, 26):
		get_movie_links('https://www.walmart.com/browse/movies-tv-shows/musical-movies/4096_530598_530712/?page=' + str(x)+ '&cat_id=4096_530598_530712')
	print len(movie_tuples)



	#movie_tuples = list(set(movie_tuples))
	print "write csv"
	with open('../data/movies_walmart.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['name', 'duration', 'genre', 'release_date', 'directors', 'stars'])
		for name in movie_tuples:
			movie = movie_tuples[name]
			#print movie.name + ";" + movie.duration + ";" + movie.genre + + ";" + movie.release_date + ";" + movie.country + ";" + movie.language + ";" + movie.directors + ";" + movie.stars
			writer.writerow([movie.name.encode('utf-8'), movie.duration.encode('utf-8'), movie.genre.encode('utf-8'), movie.release_date.encode('utf-8'), movie.directors.encode('utf-8'), movie.stars.encode('utf-8')])

	print "done"






