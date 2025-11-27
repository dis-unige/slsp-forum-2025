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
apikey = "l8xx152e3d4717324728be090543e0808e0d"
printer_id = '355935700005520'
filters = ['TEST1', 'NOT TO PRINT', 'TEST']

# to have ALL 

import requests

myurl = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts?status=' + mystatus + '&printer_id=' + printer_id + '&limit=' + mylimit + '&offset=0&apikey=' + apikey

r = requests.get(myurl, headers=headers, timeout=15)

# print (r.text)

# Import all the content
import json
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
    printout_letter = printout_letter.replace('<div class="messageBody">', '<div class="messageBody">TEST MODIFICATION')
    
        
    # PRINT
    if toprint == 1:
        # print OK
        # So convert to PDF
        import pdfkit
        myoptions = {'minimum-font-size': '12',}
        # pdfkit.from_string(printout_letter, 'pdf/printed/' + str(printout_id) + '.pdf', options = myoptions)
        
        # from weasyprint import HTML
        # pdf = HTML(printout_letter).write_pdf('pdf/printed/' + str(printout_id) + '.pdf')
        
        import os
        from pyhtml2pdf import converter
        converter.convert(printout_id + '.html', 'pdf/printed/' + printout_id + '.pdf')
    
        print ('Printed')
        # save the HTML file
        # print(printout_letter)
        html_file = open(printout_id + '.html','w', encoding='utf-8')
        html_file.write(printout_letter)
        html_file.close()       
        
    else :
        # filtered -> store the PDF
        print ('filtered')


