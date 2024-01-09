import csv
import requests
import datetime
import argparse
import pandas as pd
import math
from io import StringIO
import re
from colorama import init, Back, Style
init(autoreset=True)

#Get dates
def get_dates(startdate,enddate):
    dates = pd.DataFrame()
    if enddate and startdate:
        start = datetime.datetime.strptime(startdate, '%d/%m/%Y')
        end = datetime.datetime.strptime(enddate, '%d/%m/%Y')
        dif = end- start
        dif = dif.days
        i = math.ceil(dif/80)
        d1 = end
        for x in range(i):
            new_row = {}
            d2 = d1 - datetime.timedelta(days=80)
            d2_str = d2.strftime("%d/%m/%Y")
            d1_str = d1.strftime("%d/%m/%Y")
            new_row = pd.Series({'start_dates': d2_str, 'end_dates': d1_str})
            dates= dates.append(new_row, ignore_index=True)
            d1 = d2 - datetime.timedelta(days=1)
            i += 1
    else:
        enddate = datetime.date.today()
        startdate =  enddate- datetime.timedelta(days=60)
        enddate = datetime.datetime.strftime(enddate,'%d/%m/%Y')
        startdate = datetime.datetime.strftime(startdate,'%d/%m/%Y')
        dates = {'start_dates': [startdate], 'end_dates': [enddate]}
    return dates
    #if enddate and startdate:
        #gen datelist with those
    #if no enddate and startdate: 
        #enddate = today
        #startdate = 80 days ago
        #gen datelist

#download data
def get_csvs(dates):
    dates = pd.DataFrame(dates)
    csvnames = []
    num_rows = len(dates)
    url = 'https://www3.bcb.gov.br/novoselic/rest/resultadoLeilao/pub/contratosSwap/exportarTxt'
    for i in range(num_rows):
        start_date = dates.iloc[i]['start_dates']
        end_date = dates.iloc[i]['end_dates']
        filtro = '{' + f'"objetoLeilao":"CONTRATOS_SWAP","ofertante":"","dataInicial":"{start_date}","dataFinal":"{end_date}"' + '}' 
        data = {
            'filtro': filtro,
            'parametrosOrdenacao': "[]"
        }
        r = requests.post(url, data = data)
        text_content = r.text
        csv_content = StringIO(text_content)
        start = start_date[-4:] + '-' + start_date[:2] + '-' + start_date[3:][:-5]
        end = end_date[-4:] + '-' + end_date[:2] + '-' + end_date[3:][:-5]
        csv_file_path =  f'csvs/({i}){start}_{end}.csv'
        csvnames.append(csv_file_path)
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            for row in csv_content:
                csv_writer.writerow(row.strip().split(';'))
            print(str(r.status_code) + ' ' + start_date)
    return csvnames

#format data
def copy_together(csvnames):
    newfile = []
    for csv_name in csvnames:
        with open(csv_name, 'r') as file:
            newfile += list(csv.reader(file))
    with open('csvs/all_unformatted.csv', "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(newfile)

#convert dates
def format_dates_columns():
    formatted = []
    with open('csvs/all_unformatted.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            try: 
                prazo = int(row[7])
                date1 = datetime.datetime.strptime(str(row[2]), '%d/%m/%Y')
                date1_ = date1.strftime('%Y%m%d')
                
                date2 = datetime.datetime.strptime(str(row[8]), '%d/%m/%Y')
                date2_ = date2.strftime('%Y%m%d')
                
                date3 = datetime.datetime.strptime(str(row[9]), '%d/%m/%Y')
                date3_ = date3.strftime('%Y%m%d')
                
                accepted = str(row[10]).replace('.', '')
                offered = str(row[11]).replace('.', '')
                price = str(row[12]).replace(',', '.')
                rate = str(row[14]).replace(',', '.') 
            
                
                new_row = [date1_,str(row[7]),str(row[5]),str(row[3]),str(row[4]),date2_,date3_,accepted,offered,price,rate]
                formatted.append(new_row)
            except ValueError:
                try: 
                    prazo = int(row[5])
                    date1 = datetime.datetime.strptime(str(row[1]), '%d/%m/%Y')
                    date1_ = date1.strftime('%Y%m%d')
                    
                    date2 = datetime.datetime.strptime(str(row[6]), '%d/%m/%Y')
                    date2_ = date2.strftime('%Y%m%d')
                    
                    date3 = datetime.datetime.strptime(str(row[7]), '%d/%m/%Y')
                    date3_ = date3.strftime('%Y%m%d')
                    
                    
                    accepted = str(row[8]).replace('.', '')
                    offered = str(row[9]).replace('.', '')
                    price = str(row[10]).replace(',', '.')
                    rate = str(row[12]).replace(',', '.')
                    
                
                    new_row = [date1_,str(row[5]),str(row[4]),str(row[2]),str(row[3]),date2_,date3_,accepted,offered,price,rate]
                    formatted.append(new_row)
                except ValueError:
                    continue        
        with open('csvs/formatted_dates_columns.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(formatted)   

def noaccept_blanks():    
    noaccept = []
    with open('csvs/formatted_dates_columns.csv','r') as file:
        reader = csv.reader(file)
        for row in reader:
            if float(row[7]) == 0 and float(row[9]) == 100 and float(row[10]) == 0:
                row[7] = '-'
                row[9] = '-'
                row[10] = '-'
                noaccept.append(row)
                continue
            elif float(row[7]) == 0 and float(row[9]) == 0 and float(row[10]) == 0 and row[8] is '':
                row[7] = '-'
                row[8] = '-'
                row[9] = '-'
                row[10] = '-'
                noaccept.append(row)
                continue
            elif float(row[7]) == 0 and float(row[9]) == 0 and float(row[10]) == 0:
                row[7] = '-'
                row[9] = '-'
                row[10] = '-'
                noaccept.append(row)
                continue
            elif row[8] is '':
                row[8] = '-'
                noaccept.append(row)
                continue
            else:
                noaccept.append(row)
    with open('csvs/noaccept_1e9.csv','w',newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(noaccept)

def scan_repeat_operations():
    formatted2 = []
    with open('csvs/noaccept_1e9.csv', 'r') as file:
        csv_reader = csv.reader(file)
        unique = []
        two_operation = []
        three_operation = []
        four_operation = []
        five_operation = []
        for row in csv_reader:
            opnum = 1
            datecodetype = [row[0], row [1], row[2]]
            if datecodetype not in unique:
                unique.append(datecodetype)
                formatted2.append(row)
            else: 
                opnum=2
                if datecodetype not in two_operation:
                    two_operation.append(datecodetype)
                    op2 = str(row[1]) + '    Second Operation'
                    row = [row[0], op2, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
                    formatted2.append(row)
                else:
                    opnum=3
                    if datecodetype not in three_operation:
                        three_operation.append(datecodetype)
                        op3 = str(row[1]) + '    Third Operation'
                        row = [row[0], op3, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
                        formatted2.append(row)
                    else: 
                        opnum=4
                        if datecodetype not in four_operation:
                            four_operation.append(datecodetype)
                            op4 = str(row[1]) + '    Fourth Operation'
                            row = [row[0], op4, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
                            formatted2.append(row)
                        else:
                            opnum = 5
                            if datecodetype not in five_operation:
                                five_operation.append(datecodetype)
                                op4 = str(row[1]) + '    Fifth Operation'
                                row = [row[0], op4, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
                                formatted2.append(row)
                                print('Fifth repeat operation detected for '+row[0]+ ' ' +row [1] +' '+ row[2] + '. Confirm in source file. If there is a fifth operation of the same type on the same day of the same duration, we will need a new 6th letter in the code to accomadate')
                                fifthoperation = True
                                with open('fifthOperation.err','w'):
                                    file.write('Fifth repeat operation detected for '+row[0]+ ' ' +row [1] +' '+ row[2] + '.')  
        with open('fxauct_.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            header = ",,,,'Comunicado', 'Inicio', 'Vencimento', 'Qtd. aceita','QTD. OFERTADA','Cotaco','Taxa linear (% a.a.)'"
            for row in formatted2:
                csv_writer.writerow(row)

#generate codes from data
def gen_codes():
    codes = []
    codes_dic = []
    repeat = []
    fourdigit = []
    with open('fxauct_.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            #row 1 can be 1, 2, 3, or 4 digits long. it can have a second, third, or fourth operation, which we want to remove from the string
            duration = row[1][:4]
            duration = duration.replace(' ','')
            duration_l = len(str((int(duration))))
            if duration_l == 1:
                code_number = '00' + duration
            if duration_l == 2:
                code_number = '0' + duration
            if duration_l == 3:
                code_number = duration
            if duration_l == 4:
                print('Four digit operation detected!') #unlikely error
                fourdigit = True
                fourdigit.append(row[1])
                continue
            
            if row[2] == 'Compradora':
                operation = ' /// Compradora       '
                try:
                    int(row[1])
                    op = 'B'
                    operation = duration + operation
                except ValueError:
                    operation = row[1]  + operation #Dictionary entry
                    if 'Second Operation' in row[1]:
                        op = 'U'
                    if 'Third Operation' in row[1]:
                        op = 'Y'
                    if 'Fourth Operation' in row[1]:
                        op = 'I'
            if row[2] == 'Vendedora':
                operation = ' /// Vendedora       '
                try:
                    int(row[1])
                    op = 'S'
                    operation = duration + operation
                except ValueError:
                    operation = row[1] + operation #Dictionary entry
                    if 'Second Operation' in row[1]:
                        op = 'E'
                    if 'Third Operation' in row[1]:
                        op = 'L'
                    if 'Fourth Operation' in row[1]:
                        op = 'N'
            seventh_letter = ['C','I','V','A','O','T','R']
            for i in range(len(seventh_letter)):
                
                code = f'BR{(code_number)}{op}{seventh_letter[i]}'
                if code not in codes or code in repeat:
                    codes.append(code)
                else:
                    repeat.append(codes)
                    continue
                series = ['Comunicado', 'Inicio', 'Vencimento', 'Qtd. aceita','Qtd. ofertada','Cotaco','Taxa linear (% a.a.)']
                if i == 5 or i == 6:
                    dp = '/// *1 /// 3' 
                else: 
                    dp = '/// *1 /// 0'
                
                entry_dic = f'{code}  {dp}  |||  {operation} ||| {series[i]}'
                if entry_dic not in codes_dic:
                    codes_dic.append(entry_dic)
                dic_header= [
                    'MATCH_HEADING ||| NONE ',
                    'DATES ||| yyyymmdd ||| ',
                    'DELIMITER ||| , ',
                    'TRANS ||| " |||   ',
                    'TRANSC ||| \' |||  ',
                    'TRANS ||| - |||  ', 
                ]
                with open('fxauct.dic','w') as file:
                    for entry in dic_header:
                        file.write(entry +  '\n')
                    for entry in codes_dic:
                        file.write(entry +  '\n')
    if fourdigit:
        with open('fourdigit.err','w'):
                    file.write('\n'.join(fourdigit))
    return codes
                    
#check if there are codes not already on DB
def check_NIF(codes):
    new_codes = []
    existing_codes=[]
    with open('codes_existing.lst','r') as file:
        for e_code in file:
            e_code = e_code.replace(' ','')
            e_code = e_code.replace('\n', '')
            existing_codes.append(e_code)
        for code in codes:
            if code not in existing_codes:
                new_codes.append(code)
    if new_codes:
        print('New codes not on network:' + ', '.join(new_codes))
        with open('new/new_codes.lst','w',newline='') as file2:
            for code in new_codes:
                file2.write(code + '\n')
    return new_codes

def gen_dic_for_add(new_codes):
    entry_dic =[]
    codes_dic = []
    for code in new_codes:        
        if len(code) > 7:
            print('INVALID CODE: '+code)
            continue        
        if code[6] in ['T','R']:
            dp = '/// *1 /// 3 ' 
        else: 
            dp = '/// *1 /// 0 '
        
        duration = int(code[2:][:-2])
        
        if code[5] is 'B':
            operation = ' /// Compradora    '  
        if code[5] is 'S': 
            operation = ' /// Vendedora    '  
        if code[5] is 'U': 
            operation = '    Second Operation /// Compradora    '  
        if code[5] is 'Y': 
            operation = '    Third Operation /// Compradora    '  
        if code[5] is 'I': 
            operation = '    Fourth Operation /// Compradora    '  
        if code[5] is 'E': 
            operation = '    Second Operation /// Vendedora    '  
        if code[5] is 'L': 
            operation = '    Third Operation /// Vendedora    '  
        if code[5] is 'N': 
            operation = '    Fourth Operation /// Vendedora    ' 
        
        operation = str(duration) + operation
        
        seventh_letter = ['C','I','V','A','O','T','R']
        serieslist = ['Comunicado', 'Inicio', 'Vencimento', 'Qtd. aceita','Qtd. ofertada','Cotaco','Taxa linear (% a.a.)']
        for i in range(len(seventh_letter)):
            if code[6] == seventh_letter[i]:
                series = serieslist[i]
        entry_dic = f'{code}  {dp}  |||  {operation}  |||  {series}'
        if entry_dic not in codes_dic:
            codes_dic.append(entry_dic)
        dic_header= [
                    'MATCH_HEADING ||| NONE ',
                    'DATES ||| yyyymmdd ||| ',
                    'DELIMITER ||| , ',
                    'TRANS ||| " |||   ',
                    'TRANSC ||| \' |||  ',
                    'TRANS ||| - |||  ', 
                ]
        with open('new/add.dic','w',newline='') as file:
            for entry in dic_header:
                file.write(entry +  '\n')
            for entry in codes_dic:
                file.write(entry + '\n')
        with open('new/addCodes.txt', 'w',newline='') as file:
            file.write('\n'.join(new_codes))

#take inputs for: start date, enddate, 
def parse_args():
    parser = argparse.ArgumentParser(description='Get data for Brazil FX Swaps, generate new codes as needed.')
    parser.add_argument('-sd',"--start_date",type=str,help='startdate DD/MM/YYYY')
    parser.add_argument('-ed',"--end_date",type=str,help='enddate DD/MM/YYYY')
    args = parser.parse_args()
    return args

def main():
    #Alerts!:
    fourdigit = False #contract duration is four digits long. needs a code that looks like A23 (1023)
    fifthoperation = False #a fifth repeat operation in a day. would need a new code in 6th letter.
    #
    
    args = parse_args()
    startdate = None
    enddate = None
    if args.start_date is not None:
        startdate = args.start_date
    if args.end_date is not None:
        enddate = args.end_date
    dates = get_dates(startdate,enddate)
    csvnames = get_csvs(dates)
    copy_together(csvnames)
    print('combined csvs')
    format_dates_columns()
    print('formatted dates and columns')
    noaccept_blanks()
    print('set zeros to 1e9')
    scan_repeat_operations()
    print('scanned for repeat operations')
    codes = gen_codes()
    print('generated codes')
    new_codes = check_NIF(codes)
    print('checked for new codes') 
    h = ['','','','','Comunicado', 'Inicio', 'Vencimento', 'Qtd. aceita','QTD. OFERTADA','Cotaco','Taxa linear (% a.a.)']
    with open('fxauct_.csv','r') as file:
        r = csv.reader(file)
        with open('fxauct.csv','w',newline='') as file2:
            w = csv.writer(file2)
            w.writerow(h)
            w.writerows(r)
        
    if new_codes:
        gen_dic_for_add(new_codes)
        message = f"{Back.RED}NEW CODES FOUND: RUN ADD.BAT TO GENERATE LABELS AND PARAMETERS{Style.RESET_ALL}"
        print(message)
    
    if fourdigit:
        message = f"{Back.MAGENTA}FOUR DIGIT OPERATION FOUND! CHECK FOURDIGIT.ERR{Style.RESET_ALL}"
        print(message)
    
    if fifthoperation:
        message = f"{Back.RED}FIVE REPEATING OPERATIONS FOUND! CHECK FIFTHOPERATION.ERR{Style.RESET_ALL}"
        print(message)
   
if __name__ == "__main__":
    main()
