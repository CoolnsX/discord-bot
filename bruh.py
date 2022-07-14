import discord, requests, re, random, base64

waifu = discord.Client()

def anime_link(ani,ep=0,t=""):
    ids = re.findall(r'\?id=([^&]+)',requests.get(ani,headers={'user-agent':'uwu'}).text)
    id1 = ids[ep-1]
    ep = len(ids) if ep == 0 else ep
    title = ani.split('/')[-1].replace('-',' ')+f" episode {ep}" if not t else t 
    id1 = base64.b64encode(f"{id1}LTXs3GrU8we9O{base64.b64encode(id1.encode()).decode()}".encode()).decode()
    url = base64.b64decode(requests.get(f"https://animixplay.to/api/live{id1}",headers={'user-agent':'uwu'},allow_redirects=False).headers['Location'].split("#")[1]).decode()
    return [f"mpv '{url}' --force-media-title='{title}'",title,url]


@waifu.event
async def on_ready():
    print("You let me Inside as {0.user} UWU".format(waifu))

@waifu.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    usermsg = str(message.content)

    if message.author == waifu:
        return
    
    bot_sfw = "972595831142248518"
    bot_nsfw = "972572560564822107"
    if message.channel.id == f"{bot_sfw}" or message.channel.id == f"{bot_nsfw}":
        if usermsg.lower() == "!hello":
            await message.channel.send(f"Hello {username}")
            return
        if usermsg.lower() == "!ping":
            await message.channel.send(f"boing boing {username} UWU")
            return
        elif usermsg.lower() == "!status":
            data = requests.get("https://raw.githubusercontent.com/CoolnsX/ani-cli-status/main/results").text
            await message.channel.send(f"Here uwu Go\n{data}")
            return
        elif usermsg.lower() == "!info":
            await message.channel.send("```\nGive Orders:\n!status > gives ani-cli providers status..\n!info > this help menu\n!hello > just greetings.. cause I don't have necessary holes for you\n!anime > gives random anime link (animixplay)\n!anime anime_name > gives query anime link (animixplay)\n!hentai > gives the random hentai video url(works only in #bots-nsfw channel)\n!doujin > gives random nhentai link(works only in #bots-nsfw channel)\n!doujin @username > give dare to mentioned username\n\n\t<-- This girl is shaped by ani-cli discord members with ❤️. Take care of her wisely.. -->```")
            return
        elif usermsg.lower().split(" ")[0] == '!anime':
            if (usermsg.lower().split(" ")[1:]):
                query = usermsg.lower().partition('!anime ')[2]
                ep=int(query.split(",")[1]) if ',' in query else 0
                query=query.split(",")[0].replace(" ",'-')
                anime = re.findall(r'"/category/([^"]*)"',requests.get(f"https://gogoanime.lu//search.html?keyword={query}",headers={'user-agent':'uwu'}).text)[0]
                link = anime_link(f"https://animixplay.to/v1/{anime}",ep=ep)
                await message.channel.send(f"\n```sh\n{link[0]}```",embed=discord.Embed(title=link[1],url=link[2],description="Direct Video Link for watching on any platform"))
                return
            else:
                anime = requests.get("https://animixplay.to/random",headers={'user-agent':'uwu'},allow_redirects=False).headers['Location']
                await message.channel.send(f"Here uwu Go \nhttps://animixplay.to{anime}")
                return

    if usermsg.lower().split(" ")[0] == "!doujin":
        if message.channel.name != "bots-nsfw":
            await message.channel.send(f"Umm.. Master doesn't allow me to post here, come to #bots-nsfw channel {username}")
            return
        else:
            if (usermsg.lower().split(" ")[1:]):
                await message.channel.send(f"{username} dared you to read this {usermsg.lower().partition('!doujin ')[2]}\n https://nhentai.net/g/{random.randrange(400000)}/")
            else:
                await message.channel.send(f"I dare you to read this {username}\n https://nhentai.net/g/{random.randrange(400000)}/")
            return

    if ("animixplay.to" in usermsg.lower()) and (message.channel.name == "animixplay-rss-feed"):
        link = anime_link(re.search(r']\((.+?)\)',usermsg).group(1),t=re.search(r'\[(.+?)\]',usermsg).group(1).split('**')[1])
        await message.channel.send(f"\n```sh\n{link[0]}```",embed=discord.Embed(title=link[1],url=link[2],description="Direct Video Link for watching on any platform"))
        return

    if usermsg.lower() == "!hentai":
        if message.channel.id != f"{bot_nsfw}":
            await message.channel.send(f"Umm.. Master doesn't allow me to post here, come to <#{bot_nsfw}> channel {username}")
            return
        else:
            lol = re.findall(r'id="post-hot-(.*?)"',requests.get("https://hentaimama.io/").text)
            random.shuffle(lol)
            video_url = re.search(r'file: "(.*?)"',requests.get(re.search(r'src="(.*?)"',requests.post("https://hentaimama.io/wp-admin/admin-ajax.php",data={"action":"get_player_contents","a":lol[0]},params={"X-Requested-With":"XMLHttpRequest"}).text.replace("\\","")).group(1)).text).group(1)
            await message.channel.send(f"Here uwu go {message.author.mention}\n{video_url}")
            return
  
    if usermsg.lower() == "!anywhere" and message.channel.id != f"{bot_sfw}" :
        await message.channel.send(f"Umm.. My master doesn't allow me to post here, Please come to <#{bot_sfw}> or <#{bot_nsfw}> channel, {username}")
        return

waifu.run(<your_token_in_quotes>)
