import configparser

import pygsheets
import pandas as pd
import os

def export_to_google_sheets(data):
  config = configparser.ConfigParser()
  config.read("../config.ini")

  table = config['Google Sheets']['table']

  gc = pygsheets.authorize(service_account_file=os.path.abspath("../google_sheets_auth.json"))
  print("Authorized to Google Sheets")

  #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
  sh = gc.open_by_url("")
  #select the first sheet 
  wks = sh[0]

  current_records = wks.get_all_records()

  # Fill data
  for channel in data:
    posts_in_google = [(current_records.index(item), item['ID публикации']) for item in filter(lambda n: n.get('Название ТГ-канала') == channel['title'], current_records)]
    if (posts_in_google):
      (last_post_position, last_post_id) = posts_in_google[-1]
      print(last_post_id)
      last_parsed_post = channel['messages'].index(next(filter(lambda n: n.get('id') == last_post_id, channel['messages'])))
      new_posts = channel['messages'][:last_parsed_post]
      old_posts = channel['messages'][last_parsed_post:]
      for post in old_posts:
        post_to_update = [current_records.index(item) + 2 for item in filter(lambda n: n.get('Название ТГ-канала') == channel['title'] and n.get('ID публикации') == post['id'], current_records)][0]
        wks.update_value(addr=(post_to_update, 6), val=post['views'])
      print(new_posts)
      for post in new_posts:
        wks.insert_rows(row=last_post_position+2, values=[channel["title"], post["id"], post["date"], post["message"], post["post_link"], post["views"]])
    else:
      last_row = len(current_records)
      for post in channel['messages']:
          wks.insert_rows(row=last_row+1, values=[channel["title"], post["id"], post["date"], post["message"], post["post_link"], post["views"]])

