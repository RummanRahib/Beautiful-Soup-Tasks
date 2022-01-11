import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()
searchTerm = 'macbook+pro+m1'
url = f'https://www.amazon.co.uk/s?k={searchTerm}'

dealsList = []

# getting the data from url

def getData(url):
  res = session.get(url)
  
  # rendering all js scripts to avoid getting blocked by amazon as a bot
  res.html.render(sleep=1)
  
  soup = BeautifulSoup(res.html.html, 'html.parser')
  return soup

# parsing the html

def getDeals(soup):
  products = soup.find_all('div', {'data-component-type': 's-search-result'})
  for item in products:
    title = item.find('a', {'class': 'a-link-normal s-link-style a-text-normal'}).text.strip()
    shortTitle = title[:30]
    link = item.find('a', {'class': 'a-link-normal s-link-style a-text-normal'})['href']
    
    # getting prices, not all product will have sale price and old price
    
    try:
      salePrice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('£', '').strip())
      oldPrice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('£', '').strip())
      
    except:
      
      # hell, some products don't have any price
      
      try:
        oldPrice = float(item.find('span', {'class': 'a-offscreen'}).text.replace('£', '').strip())
      except:
        salePrice = 0
        oldPrice = 0
      
    # getting reviews
    
    try:
      reviews = float(item.find('span', {'class':'a-size-base'}).text.strip())
      
    except:
      reviews = 0
    
    # dictionary for info
    
    saleItem = {
      'Title': title,
      'Short_Title': shortTitle,
      'Link': link,
      'Sale_Price': salePrice,
      'Original_Price': oldPrice,
      'Reviews': reviews
    }
    # print(saleItem['Title'])
    dealsList.append(saleItem)
  return    
    
# function for picking items for multiple pages // works for any amazon pagination

def getNextPage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.co.uk' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return


print('--start--')

while True: 
  soup = getData(url)
  getDeals(soup)
  url = getNextPage(soup)
  if not url:
    break
  else:
    print(url)
    print(len(dealsList))

df = pd.DataFrame(dealsList)

# adding another column for discount
df['Discount (%)'] = (100 - (df.Sale_Price / df.Original_Price) * 100.0)

# sorting with highest discount
# df = df.sort_values(by=['Discount (%)'], ascending=False)

df.to_csv('amazon_search_scraping.csv', index=False)
# print(df.head())

print('--done--')  
