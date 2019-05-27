import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("old_tweet_ids").sheet1

def get_all_old_tweet_ids():
    vals = sum(sheet.get_all_values(), [])
    return list(vals)

def insert_new_id(x):
    row_count = len(get_all_old_tweet_ids())
    sheet.insert_row([str(x)], row_count+1)

