from bs4 import BeautifulSoup
import csv
from haverhelpers import hrequests

def get_site(site_url):
    response = hrequests("GET", site_url,proxyLocation="Mexico")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup
    

def get_date(soup):
    date = soup.find('title')
    if date.text:
        print('Found date: ' + date.text) 
    else: 
        print('Date not found.')
    return date.text[36:][:-18]
 
def get_number(soup):
    number = soup.find('h2', class_='px-last font_xl font_extra_bold margin-xxs-right')
    if number.text:
        print('Found value: ' + number.text) 
    else: 
        print('Value not found.')
    return number.text     

def write_csv(date, number, csv_filename):     
     with open(csv_filename, mode='w', newline = '') as csv_file:
          csv_writer = csv.writer(csv_file)
          csv_writer.writerow(['Date', 'S&P/BMV CPI'])
          csv_writer.writerow([date,number])
     print('Downloaded data to '+ csv_filename)

     
def main():
     site_url = 'https://www.bloomberglinea.com/quote/MEXBOL:IND/'
     csv_filename = "bloom.csv"
     soup = get_site(site_url)
     date = get_date(soup)
     number = get_number(soup)
     write_csv(date, number, csv_filename)
     
if __name__ == "__main__":
     main()
