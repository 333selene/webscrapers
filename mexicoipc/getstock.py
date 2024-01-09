from bs4 import BeautifulSoup
from haverhelpers import hrequests
from haverhelpers import headless_selenium
import csv
import time


def BB_get_site(site_url):
    response = hrequests("GET", site_url,proxyLocation="Mexico")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup
    

def BB_get_date(soup):
    date = soup.find('title')
    if date.text:
        print('Found date: ' + date.text) 
    else: 
        print('Date not found.')
    return date.text[36:][:-18]
 
def BB_get_number(soup):
    number = soup.find('h2', class_='px-last font_xl font_extra_bold margin-xxs-right')
    if number.text:
        print('Found value: ' + number.text) 
    else: 
        print('Value not found.')
    return number.text     

def BB_write_csv(date, number, csv_filename):     
     with open(csv_filename, mode='w', newline = '') as csv_file:
          csv_writer = csv.writer(csv_file)
          csv_writer.writerow(['Date', 'S&P/BMV CPI'])
          csv_writer.writerow([date,number])
     print('Downloaded data to '+ csv_filename)
     
def BMV_get_data(url):
    driver = headless_selenium()
    driver.get(url)
    bsobj = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    data = []
    for li in bsobj.find('dl', {'id':'viewIPC'}).find_all('li'):
        field = li.text.strip().split(':')[0]
        value = li.find('span').text.strip()
        if field.lower() == 'date':
            data = [[field,value]] + data
        else:
            data.append([field,value])
    return data

def BMV_write_csv(data, csvname):
    with open(csvname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print('Downloaded data to '+ csvname)

def main():
     retries = 0
     max_retries = 50
     retry_delay = 10
     while retries < max_retries:
          ##Get Bloomberg
          site_url = 'https://www.bloomberglinea.com/quote/MEXBOL:IND/'
          csv_filename = "bloom.csv"
          soup = BB_get_site(site_url)
          date = BB_get_date(soup)
          number = float(BB_get_number(soup).replace(',',''))
          
          ##Get BMV
          bmv_url = 'https://www.bmv.com.mx/'
          csvname = 'ipc.csv'
          data = BMV_get_data(bmv_url)
          bmv_data = float(data[1][1].replace(',',''))
          ##compare BB and BMV:
          if bmv_data / number != 1:
               print('BMV data [' + str(bmv_data) + '] and Bloomberg data [' + str(number) +'] do not match. Final data may not be out, retrying.')
               retries += 1 
               if retries < max_retries:
                    print(f'Retrying in {retry_delay} seconds...')
                    time.sleep(retry_delay)
               else: 
                    print("Max retries reached. Exiting.")
          else:
               print('Data from both sources match, writing to csv...')
               BB_write_csv(date, number, csv_filename)
               BMV_write_csv(data,csvname)   
               break
                              
if __name__ == "__main__":
    main()
