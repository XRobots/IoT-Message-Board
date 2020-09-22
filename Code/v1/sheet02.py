#!/usr/bin/python
# -*- coding:utf-8 -*-

# importing the required libraries

import sys
import os
import csv
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
#import traceback

font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open('Messageboard')

# read old vaues from last tme

filename = "log.csv"  # log file to check previous data

f = open(filename, 'r')
csv_f = csv.reader(f)
f.close()

print("getting old data")

csv_length = 15
csv_old_values = [None]*csv_length
csv_new_values = [None]*csv_length
for row in csv_f:
    for i in range(csv_length):
        csv_old_values[i] = row[i]

print("getting data from sheet")

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get the cells in the first column

for i in range(csv_length):
    csv_new_values[i] = sheet_instance.acell(f'A{i+1}').value

# check if there is any new data since last time

if any(csv_old_values[i] != csv_new_values[i] for i in range(csv_length)):
    # write values to text log file
    csv = open(filename, 'w')
    for i in range(csv_length):
        csv.write(csv_new_values[i])
        csv.write(",")
    csv.close()

    # e-Paper display stuff

    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    # Drawing on the Vertical image
    Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    print ("rendering display")
    for i in range(csv_length):
        draw.text((2, 50*i), csv_new_values[i], font = font35, fill = 0)

    #print(var1, ":", var2, "     ", var3, ":", var4)

    epd.display(epd.getbuffer(Limage))
    epd.sleep()
    print("sleeping")

else:
    print("there was no new data")
