#############################################################
# Team: The Emperor
# Names: Jackson Sikes, Thomas Nguyen, Austin Harvey, John Norris, Luke McMillan, Nolan Yelverton, Than Nguyen, Trinh Vo
# Date: 5/7/21
# Version: Python 3.8
# Description: This is a program that takes an epoch time from stdin, and the current time and uses the difference between
#   the two to make a changing 'password'
#############################################################
from sys import stdin, stdout
from datetime import datetime, date, timedelta
import pytz
import hashlib

DEBUG = False
inputted = []
formatT = "%Y %m %d %H %M %S"
code = 'disintuitive'

epoch =   '2000 01 02 03 04 05'
current = '2001 01 02 03 04 06'

#Converts the epoch and current time to UTC in order to easily obtain a time difference
#this is all assuming US/Central as the timezone
def time_to_UTC(time, format = formatT, tz = 'US/Central'):
    #creates a datetime object from the provided time string in the format specificed
    date_time = datetime.strptime(time, format)
    
    #takes care of daylight savings times, and time zone
    time_central = pytz.timezone(tz).localize(date_time)
    time_utc = time_central.astimezone(pytz.utc)
    
    return time_utc
    
#Hashes the data provided to it
def make_hash(data):
    return hashlib.md5(str(data).encode()).hexdigest()


#########
# MAIN
#########

#takes the epoch time from stdin, and if there is a supplied 'current' system time it takes that too
"""
for item in stdin:
    item = item.rstrip('\n')
    inputted.append(item)

epoch = inputted[0]

#sets the current time based on whether it was given from stdin
if(len(inputted) == 2):
    current = inputted[1]
    
else:
    time = datetime.now()
    current = time.strftime(formatT)
"""

#calls the function to turn the times into UTC
epoch_dt = time_to_UTC(epoch)
current_dt = time_to_UTC(current)

#determines the difference in seconds between the times, and
#also finds the start of the interval that the code lasts for
diffSecs = (current_dt - epoch_dt).total_seconds()
start = int(diffSecs - (diffSecs%60))

#creates the hash of the start of the time for the code
hashed = make_hash(make_hash(start))

if(DEBUG):
    print(f"Epoch:\t {epoch}")
    print(f"Current: {current}")
    print(f"Diff:\t {diffSecs}")
    print(f"Start:\t {start}")
    print(f"Hash:\t {hashed}")
    print("Code:\t ", end = '')

#goes through the hash to find the first two letters from the left
#   and the first two numbers from the right to make the code
l = 0
i = 2
before = ''
after = ''

for j in range(len(hashed)-1):
    if(l < 2):
        if(not hashed[j].isdigit()):
            before += hashed[j]
            l += 1
        
    if(i < 4):
        if(hashed[len(hashed) - (1+j)].isdigit()):
            after += hashed[len(hashed) - (1+j)]
            i += 1
            
    if(l >= 2 and i >= 4):
        break
    
code += before + after + hashed[len(hashed)//2]
        
print(code)
