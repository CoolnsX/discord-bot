import discord, requests, re, random, base64

waifu = discord.Client()

ban_words = {'java','microsoft','windows','c#','javascript','whine', 'whi_ne', 'whitespace_negative', 'whi-nyan', 'whi~nyaan!', 'whi whi'}
abusive_words = {'fuck','fk','wtf','shit','nigga','mf','mfs','bitch','ur mom','bad','cringe'}
good_words = {'moe bot','kawai bot','good bot'}

def anime_link(ani,ep=0,t=""):
    ids = re.findall(r'\?id=([^&]+)',requests.get(ani,headers={'user-agent':'uwu'}).text)
    id1 = ids[ep-1]
    ep = len(ids) if ep == 0 else ep
    title = ani.split('/')[-2].replace('-',' ')+f" episode {ep}" if not t else t 
    id1 = base64.b64encode(f"{id1}LTXs3GrU8we9O{base64.b64encode(id1.encode()).decode()}".encode()).decode()
    url = base64.b64decode(requests.get(f"https://animixplay.to/api/live{id1}",headers={'user-agent':'uwu'},allow_redirects=False).headers['Location'].split("#")[1]).decode()
    return [f"mpv '{url}' --force-media-title='{title.title()}'",title.title(),url]

def hentai_link(x):
    return re.search(r'file: "(.*?)"',requests.get(re.search(r'src="(.*?)"',requests.post("https://hentaimama.io/wp-admin/admin-ajax.php",data={"action":"get_player_contents","a":x},params={"X-Requested-With":"XMLHttpRequest"}).text.replace("\\",""))[1]).text)[1]

@waifu.event
async def on_ready():
    print("You let me Inside as {0.user} UWU".format(waifu))

@waifu.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    usermsg = str(message.content)

    if message.author == waifu:
        return

    if message.channel.name == "bot-sfw" or message.channel.name == "bots-nsfw":
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
                link = anime_link(f"https://animixplay.to/v1/{anime}/",ep=ep)
                await message.channel.send(f"\n```sh\n{link[0]}```",embed=discord.Embed(title=link[1],url=link[2],description="Direct Video Link for watching on any platform"))
                return
            else:
                anime = requests.get("https://animixplay.to/random",headers={'user-agent':'uwu'},allow_redirects=False).headers['Location']
                await message.channel.send(f"Here uwu Go \nhttps://animixplay.to{anime}")
                return

    if usermsg.lower().split(" ")[0] == '!banword':
        if usermsg.lower().split(" ")[1] == 'list':
            await message.channel.send(f"Here uwu Go \n{ban_words}")
            return
        elif usermsg.lower().split(" ")[1] == 'add':
            ban_words.update(usermsg.lower().split(' ')[2:])
            await message.channel.send(f"Done {username}")
            return
        elif usermsg.lower().split(" ")[1] == 'rm':
            ban_words.difference_update(usermsg.lower().split(' ')[2:])
            await message.channel.send(f"Done {username}")
            return

    if usermsg.lower().split(" ")[0] == '!abuse':
        if usermsg.lower().split(" ")[1] == 'list':
            await message.channel.send(f"Here uwu Go \n{abusive_words}")
            return
        elif usermsg.lower().split(" ")[1] == 'add':
            abusive_words.update(usermsg.lower().split(' ')[2:])
            await message.channel.send(f"Done {username}")
            return
        elif usermsg.lower().split(" ")[1] == 'rm':
            abusive_words.difference_update(usermsg.lower().split(' ')[2:])
            await message.channel.send(f"Done {username}")
            return

    if usermsg.lower().split(" ")[0] == '!good':
        if usermsg.lower().split(" ")[1] == 'list':
            await message.channel.send(f"Here uwu Go \n{good_words}")
            return
        elif usermsg.lower().split(" ")[1] == 'add':
            good_words.update(usermsg.lower().split(' ')[2:])
            await message.channel.send(f"Done {username}")
            return
        elif usermsg.lower().split(" ")[1] == 'rm':
            good_words.difference_update(usermsg.lower().split(' ')[2:])
            await message.channel.send(f"Done {username}")
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
        animix = re.search(r']\((.+?)\)',usermsg)[1]
        link = anime_link(animix,ep=int(animix.split('/')[-1].split('ep')[1]))
        await message.channel.send(f"\n```sh\n{link[0]}```",embed=discord.Embed(title=link[1],url=link[2],description="Direct Video Link for watching on any platform"))
        return

    if usermsg.lower().split(" ")[0] == "!hentai":
        if message.channel.name != "bots-nsfw":
            await message.channel.send(f"Umm.. Master doesn't allow me to post here, come to #bots-nsfw channel {username}")
            return
        elif (usermsg.lower().split(" ")[1:]):
            hen_query = usermsg.lower().partition('!hentai ')[2]
            hen_ep=int(hen_query.split(",")[1]) if ',' in hen_query else 0
            hen_query=hen_query.split(",")[0].replace(" ",'-')
            hentai = re.search(r'\s<a.*/tvshows/([^"]*)/',requests.get(f"https://hentaimama.io/?s={hen_query}").text)[1]
            ep_list = re.findall(r'\s<a.*hentaimama.io/episodes/([^"]*)/">',requests.get(f"https://hentaimama.io/tvshows/{hentai}/").text)[::-1]
            video_url = hentai_link(re.search(r"\?p=([^']*)",requests.get(f"https://hentaimama.io/episodes/{ep_list[hen_ep-1]}/").text)[1])
            await message.channel.send(f"Here uwu go {message.author.mention}",embed=discord.Embed(title=ep_list[hen_ep-1].replace("-"," ").title(),url=video_url,description="Have Fun"))
        else:
            lol = re.findall(r'id="post-hot-(.*?)"',requests.get("https://hentaimama.io/").text)
            random.shuffle(lol)
            video_url = hentai_link(lol[0])
            await message.channel.send(f"Here uwu go {message.author.mention}\n{video_url}")
            return
  
    if abusive_words.intersection(set(usermsg.lower().split())) and ban_words.intersection(set(usermsg.lower().split())):
        await message.channel.send("https://raw.githubusercontent.com/CoolnsX/discord-bot/main/smug.jpg")
        return
    elif ban_words.intersection(set(usermsg.lower().split())):
        await message.channel.send("https://raw.githubusercontent.com/CoolnsX/discord-bot/main/sad.png")
        return
    elif abusive_words.intersection(set(usermsg.lower().split())):
        await message.channel.send("https://raw.githubusercontent.com/CoolnsX/discord-bot/main/cringe.jpg")
        return
    elif good_words.intersection(set(usermsg.lower().split())):
        await message.channel.send("https://raw.githubusercontent.com/CoolnsX/discord-bot/main/smug.jpg")
        return

    if usermsg.lower() == "!anywhere" and message.channel.name != "bot-sfw" :
        await message.channel.send(f"Umm.. My master doesn't allow me to post here, Please come to #bot-sfw or #bots-nsfw channel {username}")
        return

waifu.run(<your_token>)
