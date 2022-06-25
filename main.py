# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv()
import os
POST_CHANNEL_ID = int(os.getenv('POST_CHANNEL_ID'))
OBSERVE_CHANNEL_ID = int(os.getenv('OBSERVE_CHANNEL_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')

import discord
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# チャンネル入退室時の通知処理
@client.event
async def on_voice_state_update(member, before, after):
    # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
    if before.channel != after.channel:
        # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
        botRoom = client.get_channel(POST_CHANNEL_ID)

        # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）
        announceChannelIds = [OBSERVE_CHANNEL_ID]

        # 監視対象チャンネルのオブジェクトを取得
        if before.channel != None and before.channel.id == OBSERVE_CHANNEL_ID:
            observe_channel = before.channel
        elif after.channel != None and after.channel.id == OBSERVE_CHANNEL_ID:
            observe_channel = after.channel
        else:
            return

        members = []
        members_ids = list(observe_channel.voice_states.keys())
        for member_id in members_ids:
            member = observe_channel.guild.get_member(member_id)
            if member.nick != None:
                members.append(member.nick)
            else:
                members.append(member.name)

        if len(members_ids) == 0:
            await botRoom.send('現在、誰も参加していません。')
            return

        underline_members = list(map(lambda name: "__" + name + "__", members))
        await botRoom.send(f'{"   ".join(underline_members)}  が参加しています。')

# Botのトークンを指定（デベロッパーサイトで確認可能）
client.run(BOT_TOKEN)

