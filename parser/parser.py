import configparser

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import Message, MessageReactions

def parse_channels():
    # Reading Configs
   config = configparser.ConfigParser()
   config.read("../config.ini")

   # Setting configuration values
   api_id = config['Telegram']['api_id']
   api_hash = config['Telegram']['api_hash']

   api_hash = str(api_hash)

   phone = config['Telegram']['phone']
   username = config['Telegram']['username']

   channels = config['Telegram']['channels'].split()
   parse_limit = int(config['Telegram']['limit'])

   # Create the client and connect
   client = TelegramClient(username, api_id, api_hash)

   parsed_channels = []

   async def main():
      await client.connect()
      print("Client Created")

      for channel in channels:
            print(f'Parsing {channel} ...')
            entity = await client.get_entity(channel)
            posts = await client(GetHistoryRequest(
            peer=entity,
            limit=parse_limit,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0))
            channel_title = entity.title
            messages = []
            for message in posts.messages:
               messages.append({
                  "id": message.id,
                  "date": message.date.strftime("%d/%m/%Y, %H:%M:%S"),
                  "message": message.message,
                  "post_link": f"https://t.me/c/{entity.id}/{message.id}",
                  "views": message.views,
                  "reactions": [(result.reaction.emoticon, result.count) for result in message.reactions.results] if message.reactions is not None else []
               }) 
            parsed_channels.append({
               "title": channel_title,
               "messages": messages
            })
         




   client.loop.run_until_complete(main())
   return parsed_channels


if __name__ == '__main__':
    parsed_data = parse_channels()
    print(parsed_data)