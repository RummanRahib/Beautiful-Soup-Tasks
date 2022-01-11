import re

import openpyxl
import requests
from bs4 import BeautifulSoup

# active excel file, excel sheet, title, columns

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'NFL League Stats 2019'

try:
  url = 'https://www.nfl.com/standings/league/2019/REG'
  res = requests.get(url)
  res.raise_for_status()

  soup = BeautifulSoup(res.text, 'html.parser')
  
  # finding the table, header, and adding the header in excel file
  
  table = soup.find('table', class_="d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-standings--detailed d3-o-table--sortable {sortlist: [[4,1]], sortinitialorder: 'desc'}")
  headers = table.find_all('th')
  
  headerList = []
  
  for header in headers:
    headerTitle = header.get_text(strip=True)
    headerList.append(headerTitle)
    # print(headerTitle)
  
  sheet.append(headerList)
  
  # adding row data to the sheet
  
  tableDataList = table.find_all('tr')[1:]
  
  for tableData in tableDataList:
    raw_data = tableData.find_all('td')
    # Extraxting team full name separately as the full name and short name both appears with the html
    teamName = raw_data[0].find('div', class_='d3-o-club-fullname').text.strip().replace('\n', '')
    teamName= re.sub('\s+',' ', teamName)
    # print(teamName)
    tableRow = [data.text.replace('\n', '') for data in raw_data[1:]]
    tableRow.insert(0, teamName)
    sheet.append(tableRow)
    # print(tableRow)
  
  
except Exception as e:
  print(e)
  
excel.save('NFL League Stats 2019.xlsx')
