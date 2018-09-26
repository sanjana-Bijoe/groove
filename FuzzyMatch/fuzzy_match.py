import csv
from fuzzywuzzy import fuzz
import re
import os


def check_domains(name,domain):
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/FuzzyMatch/tlds') as f:
        tlds = f.read().split()
    max_val = 0
    domain_splitup = re.split(r"[^a-zA-Z0-9-]", domain.lower())
    for i in domain_splitup:
        if "."+i in tlds:
            break
        max_value = max([fuzz.token_sort_ratio(name.lower(), i),
             fuzz.token_set_ratio(name.lower(), i),
             fuzz.partial_ratio(name.lower(), i),   
            ])
        if max_value > max_val:
            max_val = max_value
            
    return max_val
    

def fuzzy_match(pfile, text_name, name):
    ifile = open(pfile, "rb")
    reader = csv.reader(ifile)
    f = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/FuzzyMatch/output.csv"
    ofile = open(f, 'a')
    writer = csv.writer(ofile)
    headers = reader.next()
    index1 = headers.index(name)
    index2 = headers.index(text_name)
    headers.insert(index2+1,text_name+"_"+name+"_"+"Confidence")
    writer.writerow(headers)

    for row in reader:
        if row[index1]=="" or row[index1]=="":
            confidence = 'No match data'
        else:
            confidence = check_domains(row[index1],row[index2])
        row.insert(index2+1,confidence)
        writer.writerow(row)
    ifile.close()
    ofile.close()
    os.rename(f, pfile)   

if __name__ == '__main__':
    pfile = raw_input("File Path Name: ")
    text_name = raw_input("Name Column Name: ")
    name = raw_input("LinkedIn Column Name: ")
    fuzzy_match(pfile, text_name, name)