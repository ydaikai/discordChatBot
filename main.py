import discord
import openai
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

from datetime import date
today = date.today()
cutoff = "2021-09-01"

# OpenAI APIのセットアップ
openai.api_key = os.environ["OPENAI_TOKEN"]

chats = [{"role": "system", "content": f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: {cutoff} Current date: {today}."}]

# チャットボットへのリクエスト送信関数
def send_request(prompt):
    # リクエストパラメータの設定
    # APIへのリクエスト送信
    chats.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=list(chats)
    )
    chats.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    # 返答を取得
    return response['choices'][0]['message']['content']

@client.event
async def on_ready():
    print(f'{client.user} がログインしました')

@client.event
async def on_message(message):
  
    # 自分自身へのメッセージには反応しないようにする
    if message.author == client.user:
        return
    if message.content == "clear":
        chats = [{"role": "system", "content": f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: {cutoff} Current date: {today}."}]
        await message.channel.send("Response history was cleared.")
        return

    # 発言に対して、OpenAIに問い合わせて返答を生成する
    response = send_request(message.content)
    
    # 返答をDiscordのチャンネルに送信する
    await message.channel.send(response)

client.run(os.environ["DISCORD_TOKEN"])