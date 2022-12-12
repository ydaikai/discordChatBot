import requests
import os

# Discord Botのクライアントを作成する
client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

# OpenAIのAPIキーを設定する
API_KEY = os.environ["OPENAI_TOKEN"]

# OpenAIのAPIを呼び出すためのエンドポイントを設定する
API_ENDPOINT = "https://api.openai.com/v1/completions"

# Discord Botの動作を定義する
@client.command(name="chat", aliases=["/chat"])  # nameとaliasesを指定する
async def chat(ctx, *, query: str):
  
  # OpenAIのAPIを呼び出し、モデルから返された応答を取得する
  response = requests.post(
    API_ENDPOINT,
    headers={
      "Content-Type": "application/json",
      "Authorization": f"Bearer {API_KEY}"
    },
    json={
      "prompt": query,
      "model": "text-davinci-003",
      "temperature": 0.6,
      "max_tokens": 512
    }
  )
  # 応答をDiscord上で表示する
  await ctx.send(response.json()["choices"][0]["text"])

# Discord Botのトークンを設定して、Botを起動する
client.run(os.environ["DISCORD_TOKEN"])

# @メンションされたときの処理を定義する
@client.event
async def on_message(message):
  try:
    # Botが@メンションされているかどうかを判定する
    if message.is_mentioned(client.user):
      # Botが@メンションされたときの処理を実行する
      response = requests.post(
        API_ENDPOINT,
        headers={
          "Content-Type": "application/json",
          "Authorization": f"Bearer {API_KEY}"
        },
        json={
          "prompt": message.content,
          "model": "text-davinci-003",
          "temperature": 0.6,
          "max_tokens": 512
        }
      )
      # 応答をDiscord上で表示する
      await message.channel.send(response.json()["choices"][0]["text"])
  except Exception as e:
    print(e)
