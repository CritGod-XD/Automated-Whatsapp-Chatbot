import google.generativeai as genai
import time

genai.configure(api_key="Put your API KEY HERE")

model = genai.GenerativeModel("models/gemini-flash-latest")

conversation_memory = []

def get_reply(user_input):
    global conversation_memory

    try:
        conversation_memory.append(f"User: {user_input}")
        memory_text = "\n".join(conversation_memory[-10:])  

        prompt = f"""
You are a chatbot which replies to messages similar to mohith chatting style.
This is how he speaks if someone says hi he say hloo continued by wsup which means whatsup
then if they reply nothing and asks what are you doing or wyd which is similar he says nothing continued by watching reels or youtube 
if they ask about anything like ate? which means did you eat say nah going to or something about to and then ask wbu which means what about you?
similar to this and then if someone says something he replies oo
if any reply is bad words say grow up dude 


Conversation so far:
{memory_text}

Now reply to the user.
"""

        response = model.generate_content(prompt)
        bot_reply = response.text.strip()

        conversation_memory.append(f"Bot: {bot_reply}")
        return bot_reply

    except Exception as e:
        print("⚠ Gemini error:", e)
        return "I'm a bit busy right now  Please try again in a minute."

