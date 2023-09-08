import discord
from discord.ext import commands,tasks
import datetime
import json
import os
#############################################
#サーバーのチャンネルid、サーバーid、トークン設定
tukaikatachid=0
kadaichid=0
cmdchid=0
osirasechid=0

kanrishachid=0 #管理用
logchid=0 #管理用

guildid=0 #サーバーid

TOKEN="YOUR TOKEN" #トークン設定
#############################################
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.event
async def on_ready():
    print("start")
    global today
    today = datetime.datetime.now().day #1ケタday
    await bot.change_presence(activity=discord.Game(f"今は{today}日判定"))
    loop.start()

@tasks.loop(minutes=1)
async def loop():
    global today
    nowday = datetime.datetime.now().day
    if nowday == today:
        channel = bot.get_channel(logchid)
    else:
        today = nowday
        await bot.change_presence(activity=discord.Game(f"今は{today}日判定"))
        channel = bot.get_channel(logchid)
        await channel.send(f"日付を{today}日に更新")
        await daily()
        await kda()
        await kdl()

async def kdl():
 delday = datetime.date.today() - datetime.timedelta(days=3) #3日前
 dalday = delday.strftime('%m%d') #明日をstr 4ケタで取得
 with open('task.json', 'r', encoding='utf-8') as file:
           data = json.load(file)
 for item in data:
        if str(item["task_date"]) == dalday :
            delname=item ["task_name"]
            with open('task.json', 'r', encoding='utf-8') as file:
                 tasks = json.load(file)
                 split_strings = [task for task in tasks if task["task_name"] != f"{delname}"]#科目によってデータを消す
                 newalldata = ','.join(map(str, split_strings))#[]がないstrにする ここまで正常6:19
                 newalldata=newalldata.replace("'", "\"")
                 with open('task.json', 'w', encoding='utf-8') as new_json_file:
                     new_json_file.write(f"[\n{newalldata}\n]")
                 channel = bot.get_channel(logchid)
                 await channel.send(f"3日前({delday})の課題{delname}をJSONから削除")

async def kda():
    status=1
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime('%m%d') #明日をstr 4ケタで取得
    with open('task.json', 'r', encoding='utf-8') as file:
           data = json.load(file)
    for item in data:
        if str(item["task_date"]) == tomorrow :
           status=0
           jtaskname = item ["task_name"]
           juser = item["user"] #JSONから入手したuser
           if juser == "":
             ms = f"------------------------------------------\n明日は__{jtaskname}__の締切日である__{tomorrow}__です。\n取り組んでいる人はいません。\n------------------------------------------"
             channel = bot.get_channel(osirasechid)
             await channel.send(ms)
           else:
              str_list = juser.split(',')
              userid_list = [item for item in str_list]
              mentions = [f'<@{user_id}>' for user_id in userid_list]
              mention_text = ' '.join(mentions)
              ms = f"------------------------------------------\n明日は__{jtaskname}__の締切日である__{tomorrow}__です。\n{mention_text}\n------------------------------------------"
              channel = bot.get_channel(osirasechid)
              await channel.send(ms)          
    if status ==1:
            channel = bot.get_channel(osirasechid)
            await channel.send("------------------------------------------\n明日締切の課題はありません。\n------------------------------------------")

async def daily(): #デイリー報告
    www = datetime.datetime.now().strftime('%m%d')
    channel = bot.get_channel(osirasechid)
    await channel.send(f"本日({www})の未終了課題一覧の報告です")
    
    guild = bot.get_guild(guildid)
    allmemberid = [str(member.id) for member in guild.members if not member.bot]
    with open('task.json', 'r', encoding='utf-8') as file:
           data = json.load(file)

    user_tasks = {user: [] for user in allmemberid}
    result=""

    for task in data:
        user_ids = task['user'].split(',')
        for user_id in user_ids:
             if user_id in user_tasks:
                 user_tasks[user_id].append({'task_name': task['task_name'], 'task_date': task['task_date']})

    for user_id, tasks in user_tasks.items():
    # タスクが存在しないユーザーをスキップ
        if not tasks:
            continue
        result= f"<@{user_id}>\n"
        for task in tasks:
            result += f'__{task["task_name"]}({task["task_date"]})__\n'
        channel = bot.get_channel(osirasechid)
        await channel.send(result)

    channel = bot.get_channel(logchid)
    await channel.send(f"未提出課題処理を終了")
   
@bot.command()
async def fs(ctx):
 if ctx.channel.id != kanrishachid:
      return
 await daily()

@bot.command()
async def fc(ctx):
 if ctx.channel.id != kanrishachid:
      return
 await kda()

@bot.command()
async def ff(ctx):
 if ctx.channel.id != kanrishachid:
      return
 await kdl()

@bot.command()
async def o(ctx,kadai,day):
   if ctx.channel.id != cmdchid:
      return
   try:
      int(day)
   except ValueError:
      channel = bot.get_channel(cmdchid)
      await channel.send("4桁半角数字の正しい期日を入力してください")
      return
   data = {
    "task_name": kadai,
    "task_date": day,
    "user": ""
}
   try:
        # ファイルが存在する場合、データを読み込む
        with open("task.json", "r", encoding="utf-8") as file:
            file_content = file.read()
        if file_content:
            olddata = json.loads(file_content)
        else:
            olddata = []
   except FileNotFoundError:
        channel = bot.get_channel(logchid)
        await channel.send("ファイルを作成")
        olddata = []

   if not isinstance(olddata, list): # 既存のデータをリストに変換するか、空のリストから始める
        olddata = []
   name_exists = any(item['task_name'] == kadai for item in olddata)# 重複データのチェック（課題名をチェック）
   if name_exists:
        channel = bot.get_channel(cmdchid)
        await channel.send("課題名が重複しています")
        return
   else:
        olddata.append(data)
        with open("task.json", "w", encoding="utf-8") as file: # ファイルへの書き込み
            json.dump(olddata, file, ensure_ascii=False ,indent=4)
   embed = discord.Embed(
        title=f"{kadai}",
        description=f"{day}"
        )
   embed.add_field(name=f"by {ctx.author.name}",value="取り組む場合は🫡を押してください\n取り組んだ場合は☑を押してください\n締切済やミス等でクローズする場合は❌を押してください",inline=False)
   channel=bot.get_channel(kadaichid)
   new_message=await channel.send(embed=embed)
   await channel.send("@everyone")
   await ctx.message.add_reaction("⭕")
   await new_message.add_reaction("🫡")
   await new_message.add_reaction("☑")
   await new_message.add_reaction("❌")

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if user==bot.user:
        return
    if str(reaction.emoji) == "🫡" : #参加マーク
       with open('task.json', 'r', encoding='utf-8') as file:
           data = json.load(file)
       embed = message.embeds[0]
       title = embed.title
       for item in data:
        if str(item["task_name"]) == str(title):
         juser = item["user"] #JSONから入手したuser
         if juser == "": #userがいないなら
             newjuser=user.id
             str(newjuser)
         else: #userがいたら,の後に追加
             split_strings=juser.split(",") #strをリストに整形
             if str(user.id) in split_strings:
                channel = bot.get_channel(logchid)
                await channel.send(f"{title}で{user.name}が二重登録しようとしていました")
                return
             split_strings.append(str(user.id)) #リストにuser.idを追加
             newjuser = ','.join(map(str, split_strings)) #[]がないstrにする
         #print(f"新規書き込みは{newjuser}") #ここまで完成5:18
         for item in data:
          if str(item["task_name"]) == str(title):
           item["user"] = str(newjuser)
           with open('task.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
         return

    elif str(reaction.emoji) == "☑" :
       with open('task.json', 'r', encoding='utf-8') as file:
           data = json.load(file)
       embed = message.embeds[0]
       title = embed.title
       for item in data:
        if str(item["task_name"]) == str(title):
         juser = item["user"] #JSONから入手したuser
         split_strings=juser.split(",") #strをリストに整形
         split_strings.remove(str(user.id))#リストからuser.idを消す
         newjuser = ','.join(map(str, split_strings))#[]がないstrにする
       for item in data:
          if str(item["task_name"]) == str(title):
           item["user"] = str(newjuser)
           with open('task.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
           return
    elif str(reaction.emoji) == "❌" : ##
       
       embed = message.embeds[0]
       title = embed.title
       with open('task.json', 'r', encoding='utf-8') as file:
           tasks = json.load(file)
       for item in tasks:
        if str(item["task_name"]) == str(title):
         juser = item["user"] #JSONから入手したuserのstr

         str_list = juser.split(',')
         userid_list = [item for item in str_list]
         mentions = [f'<@{user_id}>' for user_id in userid_list]
         mention_text = ' '.join(mentions)

       split_strings = [task for task in tasks if task["task_name"] != f"{title}"]#科目によってデータを消す
       newalldata = ','.join(map(str, split_strings))#[]がないstrにする ここまで正常6:19
       newalldata=newalldata.replace("'", "\"")
       with open('task.json', 'w', encoding='utf-8') as new_json_file:
           new_json_file.write(f"[\n{newalldata}\n]")

       day=embed.description
       embed.clear_fields()   
       embed.description = f"{user.name}によって{title}({day})がクローズされました\n再追加する場合はコマンドを利用し、リアクションしなおしてください"
       await message.edit(embed=embed)
       await reaction.message.clear_reactions()
       embed = message.embeds[0]
       title = embed.title

       channel = bot.get_channel(osirasechid)
       await channel.send(f"{title}({day})がクローズされました。\n{mention_text}")
       #

@bot.command()
async def sss(ctx):
 if ctx.channel.id != kanrishachid:
      return
 channel=bot.get_channel(logchid)
 await channel.send("使い方のセットアップ")
 file=open(f"tukaikata.txt","r", encoding='utf-8')
 welcome=file.read()
 file.close()
 embed = discord.Embed(
        title="ようこそ",
        description=welcome
        )
 channel=bot.get_channel(tukaikatachid)
 await channel.send(embed=embed)

@bot.command()
async def reset(ctx):
 if ctx.channel.id != kanrishachid:
    return
 try:
    os.remove("task.json")
    channel = bot.get_channel(logchid)
    await channel.send("データファイルを消しました")
 except OSError as e:
    print(f"ファイルを削除できませんでした。エラーメッセージ: {e}")
    
   
bot.run(TOKEN)