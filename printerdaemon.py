#!/usr/bin/env python
# coding: utf-8

# SLSP Forum 2025 - Python and Alma's API for printing
# Printing slips at circulation desks

# Main libraries used
import requests
import json
import time

################################
# Parameters
################################
# Time between API calls in seconds
sleeptime = 60
# Amount of letters imported in each API call
mylimit = '10'
# Status of letters imported [pending, printed, canceled]
mystatus = 'pending'
# Alma API Key with R/W rights in task-lists
apikey = "XXX"
# Printer ID [code number, use the script https://github.com/dis-unige/almaprinter/blob/main/printers.py to obtain it. Use 'ALL' instead]
printer_id = 'XXX'
# Texts used as filter criteria, if found the letter won't be printed
filters = ['TEST1', 'NOT TO PRINT', 'TEST']

################################
# Start the infinite loop
################################
while True:
    print('#######################################')
    print('Date: ' + datetime.datetime.now().strftime('%d.%m.%Y %X'))
    print('Wating ' + str(sleeptime) + ' seconds...')
    time.sleep(sleeptime - ((time.monotonic() - starttime) % sleeptime))

    ################################
    # 1. Request the API
    ################################

    myurl = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts?status=' + mystatus + '&printer_id=' + printer_id + '&limit=' + mylimit + '&offset=0&apikey=' + apikey
    headers = {'accept': 'application/json'}
    r = requests.get(myurl, headers=headers, timeout=15)
    # print (r.text)
    data = r.json()
    printouts = data['printout']
    total_record_count = data['total_record_count']
    print('API call OK : ' + str(total_record_count) + ' printouts found')
    if total_record_count > 0 :
        ################################
        # 2. Loop inside the printouts
        ################################
        for printout in printouts :
            noprint = 0
            printout_id = printout['id']
            printout_date = printout['date']
            printout_type = printout['printout']
            printout_letter = printout['letter']
            print(printout_id + ' START')
            
            ################################
            # 3. Test the filter texts
            ################################
            for filterstr in filters:
                if (filterstr in printout_letter):
                    print(printout_id + ': FILTER TEXT FOUND "' + filterstr + '"')
                    noprint = noprint + 1 
               
            ################################
            # 4. Modify the HTML
            ################################
            # save the original HTML file
            with open('html/original/' + str(printout_id) + '.html', 'w', encoding='utf-8') as f:
                f.write(printout_letter)
                f.close()
            # Modifications of HTML
            printout_letter = printout_letter.replace('<div class="messageBody">', '<div class="messageBody">TEST MODIFICATION DONE BY SLSP-DEVELOPER-FORUM 2025')
            # save the modified HTML file
            with open('html/modified/' + str(printout_id) + '.html', 'w', encoding='utf-8') as f:
                f.write(printout_letter)
                f.close()
                
            ################################    
            # 5. convert to PDF
            ################################
            # print(printout_letter_modif)
            # testing html -> pdf convert libraries
            
            # pdfkit
            # import pdfkit
            # pdfkit.from_string(printout_letter_modif, 'pdf/printed/' + str(printout_id) + '.pdf')
            
            # xhtml2pdf
            # from xhtml2pdf import pisa
            # with open('pdf/printed/' + str(printout_id) + '.pdf', 'w+b') as result_file:
                # pisa_status = pisa.CreatePDF(printout_letter, dest=result_file,)

            # weasyprint
            from weasyprint import HTML
            if noprint == 0:
                # not filtered
                HTML(string=printout_letter).write_pdf('pdf/printed/' + str(printout_id) + '.pdf')
                print (printout_id + ': PDF generated and stored in printed folder')
            else:
                # filtered
                HTML(string=printout_letter).write_pdf('pdf/filtered/' + str(printout_id) + '.pdf')
                print (printout_id + ': PDF generated and stored in filtered folder')

            ################################    
            # 6. send PDF to printer
            ################################
            # TO BE DONE
            
            ################################    
            # 7. change the status in Alma
            ################################
            try:
                r = requests.post('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/task-lists/printouts/' + printout_id + '?op=mark_as_printed&apikey='+apikey, headers=headers, timeout=15)
            except:
                print(printout_id + ': ERROR in status modification -> TIMEOUT')
            else:
                # print('Status : ' + str(r.status_code))
                if (r.status_code == 200):
                    print(printout_id + ': status modification OK -> Printed')
                else:
                    print(printout_id + ': ERROR in status modification -> Status code ' + str(r.status_code))
            print(printout_id + ' END')
    else :
        print('No printouts found')


