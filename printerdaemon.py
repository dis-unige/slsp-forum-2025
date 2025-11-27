#!/usr/bin/env python
# coding: utf-8

# Code pour imprimer les bordereaux générés par Alma (jobs)
# SLSP Forum 2025


# Request to ALMA printouts

# Parameters
mylimit = '10'
headers = {'accept': 'application/json'}
mystatus = 'pending'
# other staus : printed, canceled
apikey = "xxx"
printer_id = '355935700005520'
filters = ['TEST1', 'NOT TO PRINT', 'TEST']

# to have ALL 

import requests

myurl = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts?status=' + mystatus + '&printer_id=' + printer_id + '&limit=' + mylimit + '&offset=0&apikey=' + apikey

r = requests.get(myurl, headers=headers, timeout=15)

def changestatus(my_id):
    # modifier le statut sur Alma
    try:
        r = requests.post('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts/' + my_id + '?op=mark_as_printed&apikey='+apikey, headers=headers, timeout=mytimeout)
    except:
        log('Job ' + my_id + ' : Modification du statut sur Alma Erreur -> TIMEOUT')
    else:
        # print('Status : ' + str(r.status_code))
        if (r.status_code == 200):
            log('Job ' + my_id + ' : Modification du statut sur Alma OK -> Printed')
        else:
            log('Job ' + my_id + ' : Modification du statut sur Alma Erreur -> Status code ' + str(r.status_code))


# print (r.text)

# Import all the content
import json
from weasyprint import HTML
data = r.json()
printouts = data['printout']

# Loop inside the printouts
for printout in printouts :
    toprint = 1
    printout_id = printout['id']
    printout_date = printout['date']
    printout_type = printout['printout']
    printout_letter = printout['letter']
    print(printout_id)
    
    # Filter
    for filterstr in filters:
        if (filterstr in printout_letter):
            print(filterstr + ' found')
            toprint = 0
    
    # Modify the HTML
    printout_letter = printout_letter.replace('<div class="messageBody">', '<div class="messageBody">TEST MODIFICATION DONE BY SLSP-DEVELOPER-FORUM 2025')
    
        
    # PRINT
    if toprint == 1:
        # print OK
        # So convert to PDF
        # import pdfkit
        # pdfkit.from_string(printout_letter, 'pdf/printed/' + str(printout_id) + '.pdf')
        # from weasyprint import HTML
        # HTML(printout_letter).write_pdf('pdf/printed/' + str(printout_id) + '.pdf')
        print ('Printed')
        # save the HTML file
        # print(printout_letter)
        HTML(string=printout_letter).write_pdf('pdf/printed/' + str(printout_id) + '.pdf')
    
        
    else :
        # filtered -> store the PDF
        print ('filtered')


