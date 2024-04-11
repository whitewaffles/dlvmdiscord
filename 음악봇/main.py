import nextcord
from nextcord.ext import commands
import asyncio
import youtube_dl
import asyncio
import yt_dlp as youtube_dl
import random
from datetime import datetime
import os


now = datetime.now()


bot = commands.Bot(command_prefix=commands.when_mentioned_or(",") and "," , intents=nextcord.Intents.all())
                #  command_prefix 란 시작할 명령어             ⬆이것과  ⬆이것은 같게 해야함

Stime = f"{str(now.hour)}시 {str(now.minute)}분 {str(now.second)}초"







#인사 명령어
@bot.command(name="안녕") # 명령
async def 인사(ctx):
    await ctx.send(f'{ctx.author.name}님 안녕하세요!')  # 답변

@bot.command(name="랜덤") # 명령
async def 랜덤(ctx):
    ran = random.randint(0,3)  # 랜덤으로 보낼 답변의 갯수 4개라면 (0,3) 9개라면 (0,8)  [파이썬의 숫자는 0부터 시작]
    if ran == 0:  # 1번 랜덤
        r = "A♥️"   # 답변
    if ran == 1:  # 2번 랜덤
        r = "A♦️"   # 답변
    if ran == 2:
        r = "A♣"
    if ran == 3:
        r = "A♠️"
    await ctx.channel.send(r)  # 변수 r의 값을 보냄

@bot.command(name="반응") # 명령
async def 인사(ctx):
    msg = await ctx.send(f'반응이다')  # 답변
    await msg.add_reaction("🧑🏿")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == 1: #봇이면 패스
        return None
    # 이모지가 "🧑🏿" 이고 해당 메시지의 이모지인 경우에만 반응
    if str(reaction.emoji) == "🧑🏿" and reaction.message.content == '반응이다':
        await reaction.message.channel.send(f'{user.name}님이 이모지를 누르셨습니다!')


@bot.command(name="임베드")  # 명령
async def embed(ctx):
    embed = nextcord.Embed(
        title='제목',           # 제목과 설명은 임베드에 1개만 추가가 가능합니다
        description='설명',
        color=nextcord.Color(0xD3851F)  # 색상 코드
    )
    embed.add_field(name='필드 제목', value='필드 값', inline=False) # 필드

    embed.set_footer(text='푸터') # 임베드 1개에 1개만 작성 가능
    
    await ctx.send(embed=embed)


@bot.slash_command(name="화이프유튜브", description="화이프 유튜브 구취 렛츠고")
async def slash(ctx:nextcord.Interaction):
    await ctx.send("화이프 유튜브 구독 취소!")


allowed_user_id = '786487900291596328'   # 내 아이디 넣기


@bot.slash_command(name = '문의', description = '봇을 통해 문의를 할 수 있습니다')  # 문의 명령어
async def slash2(interaction: nextcord.Interaction, 문의내용: str):  # 옵션
    embed = nextcord.Embed(title="📑 봇 문의 📑", description="ㅤ", color=0x4000FF)  # 문의 보낸 후 결과 임베드
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1225105723239956530/1226394327677272104/sever.png?ex=66249bb9&is=661226b9&hm=e398ad389e9db6b2ed6cb4995d7874ae2a3bc7a489a728d42ba4429ab62d9cfb&")  # 배너 URL
    embed.add_field(name="봇 문의가 접수되었습니다", value="ㅤ", inline=False)
    embed.add_field(name="문의 내용", value="```{}```".format(문의내용), inline=False)  # 문의 내용
    embed.add_field(name="ㅤ", value="**▣ 문의 내용에 대한 답장은 관리자가 확인 후\n24시간 내에 답장이 오니 기다려 주시면 감사하겠습니다.**", inline=False) 
    embed.add_field(name="ㅤ", value=f"- 보낸이 : **{interaction.user.mention}**\n- ID: **{interaction.user.id}**\n- 신청시각 : **{Stime}**", inline=False)  # 보낸이 이름
    embed.set_footer(text=f"- {interaction.guild.name}에서 알림")#, icon_url= interaction.message.user.avatar_url)
    await interaction.response.send_message(embed=embed , ephemeral=True)
    users = await bot.fetch_user(allowed_user_id)   # 문의 온 문의 내용을 DM으로 받을 사람의 ID
    await users.send(embed = nextcord.Embed(title=f"{interaction.user.name}에게 문의가 왔습니다.",description=f"유저 아이디 : ```{interaction.user.id}```\n문의 내용 : ```{문의내용}```", color=0xFA58F4))




@bot.slash_command(name = '답변', description = '봇을 통해 문의에 답변을 할 수 있습니다') #답변하기
async def slash2(interaction: nextcord.Interaction, 아이디: str, 답변: str):   # 옵션
    if str(interaction.user.id) == allowed_user_id:   # allowed_user_id에 적힌 유저만 사용 가능
        
        embed = nextcord.Embed(title="📑 봇 답변 📑", description="ㅤ", color=0x4000FF)   # 답변 임베드
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1225105723239956530/1226394327677272104/sever.png?ex=66249bb9&is=661226b9&hm=e398ad389e9db6b2ed6cb4995d7874ae2a3bc7a489a728d42ba4429ab62d9cfb&")  # 배너 URL
        embed.add_field(name="문의에 대한 답변 내용", value=f"```{답변}```".format(답변) , inline=False)   

        await interaction.response.send_message(embed = nextcord.Embed(title="봇 답변 로그",description=f"{Stime}에 {아이디}님께 ```{답변}```라고 답변을 했습니다.", color = 0xFFBF00))
        #await interaction.response.send_message(f"✅")  # 보내졌을시 나오는 확인 이모티콘
        user = await bot.fetch_user("{}".format(아이디))
        await user.send(embed=embed)
    else:
        
        embed=nextcord.Embed(title="사용 불가", description=f"```{interaction.user.mention}님은 관리자 권한이 없기 때문에 사용이 불가합니다.```", color=0xFF0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1225105723239956530/1226394327677272104/sever.png?ex=66249bb9&is=661226b9&hm=e398ad389e9db6b2ed6cb4995d7874ae2a3bc7a489a728d42ba4429ab62d9cfb&")  # 배너 URL
        embed.set_footer(text=f"- {Stime}")
        await interaction.response.send_message(embed=embed)


@bot.command(name="도움말음악")  # 명령
async def embed(ctx):
    embed = nextcord.Embed(
        title='📃ㅣ음악 도움말',           # 제목과 설명은 임베드에 1개만 추가가 가능합니다
        description='ㅤ',
        color=nextcord.Color(0xF3F781)  # 색상 코드
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1225105723239956530/1226394327677272104/sever.png?ex=66249bb9&is=661226b9&hm=e398ad389e9db6b2ed6cb4995d7874ae2a3bc7a489a728d42ba4429ab62d9cfb&")
    embed.add_field(name='- 입장', value='봇이 음성체널에 입장합니다.', inline=False) # 필드
    embed.add_field(name='- 퇴장', value='봇이 음성체널에서 퇴장합니다.', inline=False)
    embed.add_field(name='- 노래 (url)', value='봇이 (url)에 있는 동영상을 재생합니다.', inline=False)
    embed.add_field(name='- 삭제', value='재생중인 노래를 삭제합니다.', inline=False)
    embed.add_field(name='- 중지', value='재생중인 노래를 정지합니다.', inline=False)
    embed.add_field(name='- 재생', value='정지가 된 노래를 재생합니다.', inline=False)
    embed.add_field(name='- 볼륨', value='노래의 볼륨을 설정합니다. (0%~100%)', inline=False)
    embed.set_footer(text='- made  white_waffle') # 임베드 1개에 1개만 작성 가능
    
    await ctx.send(embed=embed)



# ---------------------------------------음악--------------------------------------- #
 
@bot.command(aliases=['입장'])
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
        print("음성 채널 정보: {0.author.voice}".format(ctx))
        print("음성 채널 이름: {0.author.voice.channel}".format(ctx))
    else:
        embed = nextcord.Embed(title='음성 채널에 유저가 존재하지 않습니다.',  color=nextcord.Color(0xFF0000))
        await ctx.send(embed=embed)
 
@bot.command(aliases=['퇴장'])
async def out(ctx):
    try:
        await ctx.voice_client.disconnect()
    except AttributeError as not_found_channel:
        embed = nextcord.Embed(title='봇이 존재하는 채널을 찾지 못하였습니다.',  color=nextcord.Color(0xFF0000))
        await ctx.send(embed=embed)




youtube_dl.utils.bug_reports_message = lambda: ''



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# youtube 음악과 로컬 음악의 재생을 구별하기 위한 클래스 작성.
class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# 음악 재생 클래스. 커맨드 포함.
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(aliases=['노래'])
    async def play(self, ctx, *, url):


        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'플레이어 에러 : {e}') if e else None)
        embed = nextcord.Embed(title=f'현재 재생중인 음악 : {player.title}',  color=nextcord.Color(0xF3F781))
        await ctx.send(embed=embed)


    @commands.command(aliases=['볼륨'])
    async def volume(self, ctx, volume: int):


        if ctx.voice_client is None:
            embed = nextcord.Embed(title="음성 채널에 연결되지 않았습니다.",  color=nextcord.Color(0xFF0000))
            return await ctx.send(embed=embed)

        ctx.voice_client.source.volume = volume / 100
        embed = nextcord.Embed(title=f"볼륨을 {volume}%으로 변경되었습니다.",  color=nextcord.Color(0x0040FF))
        await ctx.send(embed=embed)

    @commands.command(aliases=['삭제'])
    async def stop(self, ctx):


        await ctx.voice_client.disconnect()

    @commands.command(aliases=['중지'])
    async def pause(self, ctx):


        if ctx.voice_client.is_paused() or not ctx.voice_client.is_playing():
            embed = nextcord.Embed(title="음악이 이미 일시 정지 중이거나 재생 중이지 않습니다.",  color=nextcord.Color(0xFF0000))
            await ctx.send(embed=embed)


        ctx.voice_client.pause()

    @commands.command(aliases=['재생'])
    async def resume(self, ctx):


        if ctx.voice_client.is_playing() or not ctx.voice_client.is_paused():
            embed = nextcord.Embed(title="음악이 이미 재생 중이거나 재생할 음악이 존재하지 않습니다.",  color=nextcord.Color(0xFF0000))
            await ctx.send(embed=embed)

        ctx.voice_client.resume()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                embed = nextcord.Embed(title="음성 채널에 연결되어 있지 않습니다.",  color=nextcord.Color(0xFF0000))
                await ctx.send(embed=embed)
                raise commands.CommandError("작성자가 음성 채널에 연결되지 않았습니다.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


# ---------------------------------------음악--------------------------------------- #
 
 
intents = nextcord.Intents.default()
intents.message_content = True





bot.add_cog(Music(bot))
access_token = os.environ['BOT_TOKEN']

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(access_token)

bot.run(access_token) #토큰
