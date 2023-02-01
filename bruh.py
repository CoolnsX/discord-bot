import discord , requests, re, subprocess, os
from discord import app_commands

anime_url = "https://allanime.site"
hentai_url = "https://hentaimama.io"

def hentai_link(x):
    return re.search(r'file: "(.*?)"',requests.get(re.search(r'src="(.*?)"',requests.post(f"{hentai_url}/wp-admin/admin-ajax.php",data={"action":"get_player_contents","a":x},params={"X-Requested-With":"XMLHttpRequest"}).text.replace("\\",""))[1]).text)[1]


waifu = discord.Client(intents=discord.Intents.all())

tree = app_commands.CommandTree(waifu)

@waifu.event
async def on_ready():
        await waifu.wait_until_ready()
        await tree.sync()
        print(f"You let me Inside as {waifu.user} UWU")

@waifu.event
async def on_message(ctx):
        if ctx.author == waifu.user:
                return
        try:
                if ctx.channel.is_nsfw():
                        num = re.findall(r'(\d+)',ctx.content)[0]
                        if (len(num) > 4 and len(num) < 7):
                                await ctx.channel.send(f'{ctx.author.mention}\nhttps://nhentai.net/g/{num}/')
                                return
        except:
                pass

@tree.command(name='ping', description= 'latency to reach my heart')
async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f'Boing Boing UwU! (took {round(waifu.latency*1000)} ms)')

@tree.command(name='megamind', description= 'megamind with text')
async def megamind(interaction : discord.Interaction,text:str = 'No bitches??'):
        await interaction.response.defer()
        subprocess.run(args=['convert', '-pointsize', '45', '-fill', 'white', '-annotate','+20+50',text,'-font','Roboto-regular','https://raw.githubusercontent.com/CoolnsX/discord-bot/main/mmind.png','/tmp/out.jpg'])
        await interaction.followup.send(file=discord.File('/tmp/out.jpg'))

@tree.command(name='anime', description= 'ask me anime,will give you link')
async def anime(interaction : discord.Interaction,anime:str,episode:int = -1):
        await interaction.response.defer()
        try:
                result = re.findall(
                    r'_id":"([^"]*)","name":"([^"]*)".*sub":{"episodeString":"([^"]*)"',
                    requests.get('{}/allanimeapi?variables=%7B%22search%22%3A%7B%22allowAdult%22%3Atrue%2C%22allowUnknown%22%3Atrue%2C%22query%22%3A%22{}%22%7D%2C%22limit%22%3A40%2C%22page%22%3A1%2C%22translationType%22%3A%22sub%22%2C%22countryOrigin%22%3A%22ALL%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%229c7a8bc1e095a34f2972699e8105f7aaf9082c6e1ccd56eab99c2f1a971152c6%22%7D%7D'.format(anime_url,anime.replace(' ','%20')),headers={'user-agent':'uwu'}).text.replace('Show','\n')
                )[0]
                #episode number
                ep = result[2] if(episode == -1) else str(episode)
                #title
                title = result[1] + " Episode " + ep
                clock_id = re.findall(
                    r'clock\?id=([^"]*)".*sourceName"',
                    requests.get(f'{anime_url}/watch/{result[0]}/episode-{ep}-sub',headers={"user-agent":"uwu"}).text.replace('\\','').replace('type','\n')
                )[-1]

                video_url = re.findall('link":"([^"]*)"',requests.get(f'https://blog.allanime.pro/apivtwo/clock.json?id={clock_id}',headers={"user-agent":"uwu"}).text)[0]
                if video_url:
                    await interaction.followup.send(
                        f"\n```sh\nmpv '{video_url}' --force-media-title='{title}'```",
                        embed=discord.Embed(title=title,url=video_url,description="Direct Video Link for watching on any platform")
                    )
                    return
                await interaction.followup.send("No video url",ephemeral=True)
        except:
                await interaction.followup.send("Error",ephemeral=True)

@tree.command(name='hentai', description= 'ask me hentai,will give you link')
async def hentai(interaction,hentai:str,episode:int = 0):
        if not interaction.channel.is_nsfw():
                await interaction.response.send_message("I only send in nsfw enabled channels",ephemeral=True)
                return

        await interaction.response.defer()
        try:
                result = re.search(r'\s<a.*/tvshows/([^"]*)/',requests.get("{}/?s={}".format(hentai_url,hentai.replace(' ','-'))).text)[1]
                ep_list = re.findall(r'\s<a.*hentaimama.io/episodes/([^"]*)/">',requests.get(f"{hentai_url}/tvshows/{result}/").text)[::-1]
                video_url = hentai_link(re.search(r"\?p=([^']*)",requests.get(f"{hentai_url}/episodes/{ep_list[episode-1]}/").text)[1])
                await interaction.followup.send(f"Here uwu go",embed=discord.Embed(title=ep_list[episode-1].replace("-"," ").title(),url=video_url,description="Have Fun"))
        except:
                await interaction.followup.send('Error',ephemeral=True)

waifu.run(os.getenv("WAIFU"))
