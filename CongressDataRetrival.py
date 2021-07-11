#Retrieve Data from Congress Application and format it as JSON

import csv, json, zipfile
import requests
import fitz
import os
from datetime import datetime


#House of Represenatives

#globals
current_year = str(datetime.today().year)
current_directory = os.getcwd()
doc_id = ''

#get last name of represenative from user
represenative_name = input("Represenative's Last Name: ")
represenative_name = represenative_name.lower() #force the name into lowercase for directory name creation later in the file

house_zip_url = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/" + current_year + "FD.ZIP"
house_pdf_base_url = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/" + current_year + "/"

zip_file_request = requests.get(house_zip_url)
new_zipfile_name = represenative_name + current_year + ".zip"

#download zip file 
with open(new_zipfile_name, 'wb') as file:
    file.write(zip_file_request.content)

with zipfile.ZipFile(new_zipfile_name) as z:
    z.extractall('.')

with open('2021FD.txt') as f:
    for line in csv.reader(f, delimiter = '\t'):
        
        if line[1].lower() == represenative_name:
            date = line[7]
            doc_id = line[8]
        
            pdf_doc_source = requests.get(f"{house_pdf_base_url}{doc_id}.pdf")

            #create directory for represenative if it doesn't exist
            if not os.path.exists(current_directory + "/" + represenative_name):
                try:
                    os.makedirs(current_directory + "/" + represenative_name)
                except OSError as exc: # Guard against race condition
                    if exc.errno != zipfile.error.EEXIST:
                        pass


            #Write newest file under Represenative's name
            #need ability to save to a directory under the represenatives name. 
            with open(represenative_name + f"/{doc_id}.pdf", 'wb+') as pdf_file:
                pdf_file.write(pdf_doc_source.content)

            #extract text from PDF file to JSON format
            document = fitz.open(represenative_name + f"/{doc_id}_{date}.pdf")
