import os
from openai import OpenAI
from dotenv import load_dotenv 
import time

load_dotenv()

from utils.RequestSender import requestSender


open_ai_api_key: str = os.environ.get('OPENAI_API_KEY')
user_id: int = int(os.environ.get('USER_ID'))
session_key: str = os.environ.get('SESSION_KEY')
gpt_message_id = ';;;'


client = OpenAI(
    api_key=open_ai_api_key
)


def ask_gpt(question: str):
  completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": "You are a quiz assistant, skilled in answering test questions based on Android Studio. You will get qestion with possible answers and you need to choose the correct ones. There can be more than one correct answer - you need to choose all of them. Make your responses short and concentrate on correct answers."},
      {"role": "user", "content": question}
    ]
  )

  return completion.choices[0].message.content


def response_handler(res):
   if res is None or len(res) == 0 or res[0] is None or res[0].get('data') is None:
      return None
   else:
      return res[0].get('data')


def get_messages():
  res = requestSender.post_req(
        f"https://eportal.pwr.edu.pl/lib/ajax/service.php?sesskey={session_key}&info=core_message_get_conversations",
        [{"index":0,"methodname":"core_message_get_conversations","args":{"userid":f"{user_id}","type":None,"limitnum":51,"limitfrom":0,"favourites":True,"mergeself":True}}]
    )
  return response_handler(res)


def post_message(message: str, conversationId: int):
   res = requestSender.post_req(
        f"https://eportal.pwr.edu.pl/lib/ajax/service.php?sesskey={session_key}&info=core_message_send_messages_to_conversation",
        [{"index":0,"methodname":"core_message_send_messages_to_conversation","args":{"conversationid":conversationId,"messages":[{"text": message}]}}]
    )
   return response_handler(res)


def get_conversation_id():
  res = requestSender.post_req(
        f"https://eportal.pwr.edu.pl/lib/ajax/service.php?sesskey={session_key}&info=core_message_get_self_conversation",
        [{"index":0,"methodname":"core_message_get_self_conversation","args":{"userid":user_id,"messagelimit":100,"messageoffset":0,"newestmessagesfirst":True}}]
    )
  return response_handler(res)['id']
   

processed_messages = []
conversation_id = get_conversation_id()

while True:
  time.sleep(5)
  data = get_messages()


  if data is None or data['conversations'] is None or len(data['conversations']) == 0:
      print("No conversations")
      continue

  messages = data['conversations'][0]['messages']
  for message in messages:
      if message['text'] in processed_messages:
          continue
      
      if gpt_message_id in message['text']:
          processed_messages.append(message['text'])
          continue

      content = message['text'].replace("<br />", "\n").replace("<p>", "").replace("</p>", "")

      print("ASKING GPT")
      answer = ask_gpt(content)
      print("posting answer", answer)
      post_message(f"({gpt_message_id}){answer}", conversation_id)

  


