import openpyxl
import requests
from bs4 import BeautifulSoup

# active excel file, excel sheet, title, columns

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'IMDB 250 Top Rated Movies'
sheet.append(['Movie Rank', 'Movie Title', 'Release Year', 'Rating'])
# print(excel.sheetnames)


try:
  url = 'https://www.imdb.com/chart/top/'
  response = requests.get(url)
  response.raise_for_status()
  
  soup = BeautifulSoup(response.text, 'html.parser')
  
  # finding the main list of all movies
  
  movies = soup.find('tbody', class_='lister-list').find_all('tr')
  
  # extracting individual movie details from the list
  
  for movie in movies:
    movieDetails = movie.find('td', class_='titleColumn')
    movieRank = movieDetails.get_text(strip=True).split('.')[0]
    movieTitle = movieDetails.a.text
    movieYear = movieDetails.span.text.strip('()')
    movieRating = movie.find('td', class_='ratingColumn imdbRating').strong.text.strip()
    print(movieRank, movieTitle, movieYear, movieRating)
    
    # adding individual movie details to the excel sheet
    sheet.append([movieRank, movieTitle, movieYear, movieRating])
  
except Exception as e:
  print(e)
  
# saving the excel file

excel.save('IMDB 250 Top Rated Movies.xlsx')

