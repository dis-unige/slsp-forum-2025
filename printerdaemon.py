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
    printout_id = printout['id']
    printout_date = printout['date']
    printout_type = printout['printout']
    printout_letter = printout['letter']
    print(printout_id)


