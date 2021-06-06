import discord
import os
import requests
import asyncio
from json import loads

twitch_Client_ID = 'f1o23oh5jcoo6rcha25bs2v6nt3z7e'
twitch_Client_secret = 'mtm6xp8b20dma9fg7r1t94po2m4688'


discord_channelID = 825065746245615668
discord_bot_state = '방송 알리미'
twitchID = 'nrmtzv'
ment = '아아 마이크 테스트 마이크 테스트'


client = discord.Client()

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")

    # 디스코드 봇 상태 설정
    game = discord.Game(discord_bot_state)
    await client.change_presence(status=discord.Status.online, activity=game)

    # 채팅 채널 설정
    channel = client.get_channel(discord_channelID)

    # 트위치 api 2차인증
    oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twitch_Client_ID + "&client_secret=" + twitch_Client_secret + "&grant_type=client_credentials")
    access_token = loads(oauth_key.text)["access_token"]
    token_type = 'Bearer '
    authorization = token_type + access_token
    print(authorization)

    check = False     #여기 오류를 수정합니다

    while True:
        print("ready on Notification")

        # 트위치 api에게 방송 정보 요청
        headers = {'client-id': twitch_Client_ID, 'Authorization': authorization}
        response_channel = requests.get('https://api.twitch.tv/helix/streams?user_login=' + twitchID, headers=headers)
        print(response_channel.text)
        # 라이브 상태 체크
        try:
            # 방송 정보에서 'data'에서 'type' 값이 live 이고 체크상태가 false 이면 방송 알림(오프라인이면 방송정보가 공백으로 옴)
            if loads(response_channel.text)['data'][0]['type'] == 'live' and check == False:
                await channel.send(ment +'\n https://www.twitch.tv/' + twitchID)
                print("Online")
                check = True

        except:
            print("Offline")
            check = False

        await asyncio.sleep(30)

client.run(os.environ['token'])