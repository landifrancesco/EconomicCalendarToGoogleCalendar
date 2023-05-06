import pandas as pd
import datetime as dt

LOCAL_GMT = 2
INPUT_FILE = "calendar-event-list.csv"
OUTPUT_FILE = "google_calendar.csv"

try:
    df = pd.read_csv(INPUT_FILE)  # read the input file and put in a dataframe
    del df["Id"]  # delete id column
    df.Start = df.Start.apply(pd.to_datetime)  # transform column to datetime format
except Exception:
    print("Error on the INPUT FILE, please download the calendar from: https://www.fxstreet.com/economic-calendar")

df['Day'] = [d.date() for d in df['Start']]  # day formatted as mm/dd/yyyy
df['Time'] = [d.time() for d in df['Start']]  # time formatted as hh:mm in GMT +0

# converto GMT +0 to local GMT
if GMT >= 0:
    df['Time2'] = df['Time'].apply(lambda x: (dt.datetime.combine(dt.datetime(1, 1, 1), x, ) + dt.timedelta(
        hours=GMT)).time())

if GMT < 0:
    df['Time2'] = df['Time'].apply(lambda x: (dt.datetime.combine(dt.datetime(1, 1, 1), x, ) - dt.timedelta(
        hours=GMT)).time())

newdf = pd.DataFrame(
    columns=["Subject", "Start Date", "Start Time", "End Date", "End Time", "All day event", "Description", "Location",
             "Private"])  # create a new dataframe with Google Calendar's columns needed for the import process
newdf['Subject'] = df['Name']
newdf['Start Date'] = df['Day']
newdf['End Date'] = df['Day']
newdf['Start Time'] = df['Time2']
newdf['End Time'] = df['Time2']
newdf['All day event'] = "False"
newdf['Description'] = df['Currency'] + " | " + df['Impact']
newdf['Location'] = ""
newdf['Private'] = "True"

try:
    newdf.to_csv(OUTPUT_FILE, sep=',', encoding='utf-8', index=False)  # create the output file
except Exception:
    print("Error on the OUTPUT FILE")
finally:
    print("Script terminated.")