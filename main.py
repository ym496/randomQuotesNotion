import os
import requests
import schedule
import time


token = os.environ['token']
block_id = os.environ['quoteBlockId']


def random321quote():
  url = requests.get("https://www.jcquotes.com/api/quotes/random")
  return url.json()["rawText"][:-14]


def calloutContent(block_id):
  b = requests.get(f'https://api.notion.com/v1/blocks/{block_id}',
                   headers={
                     'Authorization': '{}'.format(token),
                     'Notion-Version': '2022-06-28'
                   })

  return b.json()['callout']['rich_text'][0]['plain_text']


update = {"callout": {"rich_text": [{"text": {"content": random321quote()}}]}}


def updateblock(block_id, update):
  requests.patch(f'https://api.notion.com/v1/blocks/{block_id}',
                 json=update,
                 headers={
                   'Authorization': '{}'.format(token),
                   'Notion-Version': '2022-06-28',
                   "Content-Type": "application/json"
                 })




schedule.every(5).minutes.do(updateblock,block_id=block_id,update=update)

while True:
    schedule.run_pending()
    time.sleep(180)

