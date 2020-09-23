#!/usr/bin/python
# -*- coding:utf-8 -*-

# importing the required libraries

import csv
import sys
import time
import os

from PIL import Image, ImageDraw, ImageFont
import gspread
from oauth2client.service_account import ServiceAccountCredentials

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5_V2

# define global constants
WHITE = 255
GREY = 35
BLACK = 0
FONT = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), GREY)

def get_sheet(sheet_name, i):   # encapsulate code into functions
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(i)
    return sheet_instance
    
def write_to_e_paper(values):
    assert len(values) <= 15   # could probably do with some better error handling
    # e-Paper display stuff
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    # Drawing on the Vertical image
    image = Image.new('1', (epd.height, epd.width), WHITE)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    print("rendering display")
    for i, value in enumerate(values):    # no need to special case each row
    	draw.text((2, 50*i), value, font=FONT, fill=BLACK)   # PEP8 says no spaces around ´=´ when using it for keyword arguments

    epd.display(epd.getbuffer(image))
    epd.sleep()
    print("sleeping")

if __name__ == "__main__":   # only runs this code if script is directly called, not when being imported from
    # get the instance of the Spreadsheet
    sheet = get_sheet('Messageboard', 0)
    print("getting data from sheet")
    # get the cells in the first column
    values = sheet_instance.get_col(0) # might also start at 1, not sure...
    
    # read old vaues from last time
    filename = "log.csv"  # log file to check previous data
    # TODO: check that the file actually exists
    with open(filename, 'r') as f:     # use ´with´ to ensure file is properly closed
        old_values = next(csv.reader(f))   # is a list of values now, much easier to use

    # check if there is any new data since last time
    if values != old_values:  # much easier than comparing each value yourself
        write_to_e_paper(values)
        
        # write values to text log file
        # only write file if the values changed
        with open(filename, 'w') as csv:
            writer = csv.writer(csv)    # there is also a csv.writer
            writer.writerow(values)
    else:
        print("there was no new data")

