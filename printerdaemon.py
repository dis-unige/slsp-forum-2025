#!/usr/bin/env python
# coding: utf-8

# Code pour imprimer les bordereaux générés par Alma (jobs)
# SLSP Forum 2025


# Request to ALMA printouts

# Parameters
mylimit = 50
apikey = 'headers = {'accept': 'application/json'}'
mystatus = 'pending'
headers = {'accept': 'application/json'}

import requests
myurl = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts?status=' + mystatus + '&printer_id=' + printer_id + '&limit=' + mylimit + '&offset=0&apikey=' + apikey

r = requests.get(myurl, headers=headers, timeout=15)

