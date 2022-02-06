import logging
import os

from dotenv import load_dotenv
load_dotenv()

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

token = os.getenv("SLACK_TOKEN")

client = WebClient(token=token)
logger = logging.getLogger(__name__)

bot_id = client.auth_test()["user_id"]

def fetch_conversations():
    try:
        result = client.conversations_list(types="mpim")
        return save_conversations(result["channels"])
    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))

def save_conversations(conversations):
    conversations_store = {}

    conversation_id = ""
    for conversation in conversations:
        conversation_id = conversation["id"]

        conversations_store[conversation_id] = conversation

    return conversations_store

def userid_to_name(id):
    return client.users_profile_get(user=id)["profile"]["real_name"]

def extract(m, members):
    time = m["ts"]

    sender_id = m["user"]
    receiver_id = [x for x in members if x != sender_id][0]

    sender = userid_to_name(sender_id)
    receiver = userid_to_name(receiver_id)

    body = m["blocks"][0]["elements"][0]["elements"][0]["text"]
    return [int(float(time) * 1e6), sender, receiver, body]


def upload_conversations(last):
    conversations_store = fetch_conversations()

    updates = []

    for id in conversations_store:
        messages = client.conversations_history(channel=id).data["messages"]
        members = client.conversations_members(channel=id)["members"]
        members.remove(bot_id)

        new_messages = [extract(m, members) for m in messages if float(m["ts"]) > last]
        updates += new_messages

    updates.sort(reverse=True)
    next_last = last if not updates else updates[0][0]
    return (next_last, updates)

print(upload_conversations(0))
