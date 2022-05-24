#!/usr/bin/env python3
import argparse, requests
import xlwt, xlrd, json, time

from sys import exit
from time import sleep
from random import choice
from threading import Thread
from bs4 import BeautifulSoup
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main(args):

  # Sheet's variables.
  q = 1
  w = 2 # NOTE: Variable W is for when working within spreadsheet. Python starts at 0 and counts upwards from there. Excel starts at 1, causing there to be a downwards shift in cells within formulas.
  wb = xlwt.Workbook()
  ws = wb.add_sheet('Scraped LinkedIn Employees', cell_overwrite_ok=True)
  compname ="Edeka_" 
  compname = compname[:-4] + "Scraped.xls"
  
  ## Column vars.
  col_offset = 10
  col_fname = 0
  col_lname = 1
  col_job = 2
  col_email = 3
  col_pwned = 4
  col_breaches = 5
  col_passwords = 6
  
  # Names.
  f_name = "First Name:"
  l_name = "Last Name:"
  job_name = "Job Title:"
  email_name = "Email:"
  
  pwned_name = "Pwned:"
  breaches_name = "Breaches:"
  passwords_name = "Passwords Breached:"
  
  # Write the name of the columns.
  ws.write(0, col_fname, f_name)
  ws.write(0, col_lname, l_name)
  ws.write(0, col_job, job_name)
  ws.write(0, col_email, email_name)
  
  # when args.hibp != ""
  ws.write(0, col_pwned, pwned_name)
  ws.write(0, col_breaches, breaches_name)
  ws.write(0, col_passwords, passwords_name)
  
  # Width of each column, for later adjustment.
  f_size = len(f_name)
  l_size = len(l_name)
  job_size = len(job_name)
  email_size = len(email_name)
  pwned_size = len(pwned_name)
  breaches_size = len(breaches_name)
  passwords_size = len(passwords_name)
  
  file1 = open(args.file,'r')
  lines = file1.readlines()
  for line in lines:
   line=line.rstrip('\n')
   # Write the person's info
   email=line
   ws.write(q, col_email, email)
   
   # initial request
   breaches_pass = []
   hibp_url = "https://haveibeenpwned.com/api/v3/breaches"
   response = requests.get(hibp_url, headers={'hibp-api-key':args.hibp})
   response_json = json.loads(response.content)

   # Add every breach that contains password exposition to a list.
   for breach in response_json:
     if "Passwords" in breach["DataClasses"]:
       breaches_pass.append(breach["Name"])

   # request with email
   hibp_url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
   hibp_email = line 
   hibp_request = hibp_url + hibp_email
   # The API doesn't like getting spammed.
   time.sleep(1.5)
   
   response = requests.get(hibp_request, headers={'hibp-api-key':args.hibp})
   response_code = response.status_code

   # Prints the result to each email.
   if response_code == 200:
       print(bcolors.FAIL + "Found in Breach - " + hibp_email)
   else:
       print(bcolors.OKBLUE + "Not found - " + hibp_email)
   # If the response is positive..
   if response_code == 200:
       # Writes pwned col to yes.
       ws.write(q, col_pwned, "Y")
       response_json = json.loads(response.content)

       breaches_string = ""
       passwords_string = ""
   
       breached_n = len(response_json)
   
       # Adds every breach name to a list.
       for i in range(0, breached_n):
           breach = response_json[i]["Name"]
   
           # Adds breach to breach list.
           breaches_string += breach
           if i != breached_n-1:
               breaches_string += ", "
   
           # If breach contains passwords leak, adds it to pass_breach list.
           if breach in breaches_pass:
               if len(passwords_string) != 0:
                   passwords_string += " - "
   
               passwords_string += breach
   
       # Checks for the longest width.
       if len(breaches_string) > breaches_size:
           breaches_size = len(breaches_string)
       if len(passwords_string) > passwords_size:
           passwords_size = len(passwords_string)
   
   
       # Writes breached services.
       ws.write(q, col_breaches, breaches_string)
       ws.write(q, col_passwords, passwords_string)
   
   # Otherwise..
   else:
       # Writes no to pwned col.
       ws.write(q, col_pwned, "N")
   
   w = w + 1
   q = q + 1
  
  #id = data['first'] + ":" + data['last']
  
  #if name and id not in found_names:
  #    found_names[id] = data
  
          # Finally, sets the coiums width to their maximum.
  #ws.col(col_fname).width = 257 * f_size + col_offset
  #ws.col(col_lname).width = 257 * l_size + col_offset
  #ws.col(col_job).width = 257 * job_size + col_offset
  ws.col(col_email).width = 257 * email_size + col_offset
  ws.col(col_pwned).width = 257 * 8 + col_offset
  ws.col(col_breaches).width = 257 * breaches_size + col_offset
  ws.col(col_passwords).width = 257 * passwords_size + col_offset
  
  # Write to the actual file.
  wb.save(compname)
  currentdir = os.getcwd()
  print("Scrape Complete! Results saved to " + currentdir + "/" + compname)

if __name__ == '__main__':
    VERSION = "1.0"

    args = argparse.ArgumentParser(description="", formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)

    args.add_argument('-p', '--hibp', type=str, default="", help="HIBP API key")
    args.add_argument('-f', '--file', type=str, default="", help="Input file containing e-mail line by line")

    args = args.parse_args()
#    safe = args.safe
    debug = False

    try:
        main(args)
    except KeyboardInterrupt:
        print("[!] Key event detected, closing...")
        exit(0)
