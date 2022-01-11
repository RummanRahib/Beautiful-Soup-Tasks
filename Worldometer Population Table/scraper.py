import openpyxl
import requests
from bs4 import BeautifulSoup

# active excel file, excel sheet, title, columns

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'World Population 2020'

try:
  url = 'https://www.worldometers.info/world-population/'
  res = requests.get(url)
  res.raise_for_status()

  soup = BeautifulSoup(res.text, 'html.parser')
  
  # finding the table, header, and adding the header in excel file
  
  table = soup.find('table', class_='table table-striped table-bordered table-hover table-condensed table-list')
  headers = table.find_all('th')
  
  headerList = []
  
  for header in headers:
    headerTitle = header.get_text()
    headerList.append(headerTitle)
    # print(headerTitle)
    
  sheet.append(headerList)
  
  # adding row data to the sheet
  
  tableDataList = table.find_all('tr')[1:]
  
  for tableData in tableDataList:
    raw_data = tableData.find_all('td')
    tableRow = [data.text.replace(' ', '') for data in raw_data]
    sheet.append(tableRow)
    # print(tableRow)
  
  
except Exception as e:
  print(e)
  
excel.save('World Population from Worldometers.xlsx')
