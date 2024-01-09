import requests
import json
import csv
import datetime
from datetime import date
import argparse 

def parse_args():
    parser = argparse.ArgumentParser(description="Python script to download timeseries data from Banco Central de Reserva del Peru Statistics Database")
    parser.add_argument("codes", help="time series code being retrieved. Can pass a single code or a list of codes in a .txt file")
    parser.add_argument('-sd',"--start_date", help="start date for data retrieval (MM/DD/YYYY)")
    parser.add_argument('-ed',"--end_date", help="end date for data retrieval (MM/DD/YYYY)")
    parser.add_argument('-o',"--output_file", help="name of output csv", default='data.csv')
    args = parser.parse_args()
    return args

def get_dates(start_date, end_date):
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y')
    else:
        end_date = date.today()
    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')
    else:
        start_date = end_date - datetime.timedelta(days=31) 
    return start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d')

def get_codes(codes):
    with open(codes, 'r') as file:
        code_list = [line.strip() for line in file]
    code_string = '-'.join(code_list)
    return code_string

def get_url(base_url, start_date, end_date, codes):
    base_url = base_url
    end_string = f'{codes}/json/{start_date}/{end_date}' 
    url = base_url + end_string 
    return url

def get_data(url, output_file):
    resp = requests.get(url)
    headers = ['',]
    for header in json.loads(resp.content)['config']['series']:
        headers.append(header['name'])
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
        ##Add each row to the csv    
    for data in json.loads(resp.content)['periods']:
        row = []
        date = data['name']
        numbers = data['values']
        row.append(date)
        for number in numbers:
            row.append(number)
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
            
    length = len(json.loads(resp.content)['periods'])
    csv_lastdate = date = json.loads(resp.content)['periods'][length-1]['name']
    print('Downloaded ' + output_file)
    print('Last date in csv: ' + csv_lastdate) ## For some reason 28th June 2021 will appear at the bottom of the csv. could have to do with the api idk doesn't affect data.

def main():
    print('Downloading data...')
    base_url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'
    args = parse_args()
    start, end = get_dates(args.start_date, args.end_date)
    if args.codes.endswith('.txt'):
        codes = get_codes(args.codes)
    else: 
        codes = args.codes
    url = get_url(base_url, start, end, codes)
    output_file = args.output_file
    get_data(url, output_file)
    
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    

    



#       _.-.       
#     -'    '      .-'-.
#   .',      '    '     '
#   ', `,     .  '.-.   '
#    '   \    ' ."   ".'
#     '.' \   ;.",    "-._
#      '   '. ,"  "-."    '.
#       _.--'.    ." ,.--.  .
#    , '     "-..".-'     \ '
#  -`     _.''".    ' .    '
# '     -'   "  '-     '.
# '    '    "     '      '
#  '.'     "       '    .'
#    ',    "        ' .'
#          "        ,'
#          "
#          "
#        _."._