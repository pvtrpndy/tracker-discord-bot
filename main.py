import os
from discord.ext import commands 
import json
from amazon import tracker
import discord
from screenshot import screen



client = commands.Bot(command_prefix = '-', help_command=None)

@client.event 
async def on_ready():
  print('ready')


@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = "Help",
    color=discord.Color.blue()
  )
  s = "**-track <amazon.in link> <alert price (optional)>**: Tracks the price of the product. Alert price is the current price by default \n **-list**: Lists all your trackings \n **-delete <item index>**: Deletes a product from tracking list \n **-current <item index>**- Tells the current price of the product\n"
  embed.add_field(name = "Amazon tracking", value = s, inline = False)
  embed.set_footer(text = 'The prices od amazon trackings are updated every 2 hours')
  await ctx.send(embed = embed)


@client.command()
async def track(ctx, *args):
  id = ctx.author.id
  with open("data/"+'usual.json', 'r') as f:
    trackData = json.load(f)   
  filename = str(id)+".json"
  if 1==1:
    url = args[0]
    try:
      alert = float(args[1])
    except:
      alert = -1.0  
    try:
      with open("data/"+filename, 'r') as f:
        trackData = json.load(f) 
    except:
      with open("data/"+'allusers.json', 'r') as f:
        li = json.load(f)
      li["ids"].append(str(id))
      with open("data/"+'allusers.json', 'w') as f:
        json.dump(li,f,indent = 4)
      with open("data/"+filename, 'w') as f:
        json.dump(trackData,f)
    
    if "flipkart" in url:
      await ctx.send('`browsing through flipkart...`')
      trackData["items"].append(tracker(url, alert))
    elif "amazon" in url:
      await ctx.send('`browsing through amazon...`')
      trackData["items"].append(ftracker(url, alert))
    with open(filename, 'w') as f:
      json.dump(trackData,f, indent = 2)
      
    await ctx.send('`added successfully`')
          
  else:
    await ctx.send('error')


@client.command()
async def list(ctx):
  id = ctx.author.id
  filename = str(id)+".json"
  data = {}
  try:
    with open("data/"+filename, 'r') as f:
      data = json.load(f)
  except:
    await ctx.send('No data stored for '+str(ctx.author))
  s = ""
  embed = discord.Embed(
    title = "Tracking for "+str(ctx.author)+":",
    color=discord.Color.blue()
  )
  i = 1

  for item in data["items"]:
    s ="["+item["name"]+"]("+ item["url"] +") `₹"+ str(item["current"])+"`"
    embed.add_field(name = str(i), value = s, inline=False)
    s = ""        
    i+=1
      
  embed.set_footer(text = 'To delete an item, **-delete <item no.>**')
  print(s)
  await ctx.send(embed= embed)

  
@client.command()
async def delete(ctx, *args):
  id = ctx.author.id
  filename = str(id)+".json"
  i = int(args[0])-1
  try:
    with open("data/"+filename, 'r') as f:
      data = json.load(f)
    (data["items"]).pop(i)
    with open("data/"+filename, 'w') as f:
      json.dump(data,f, indent= 2)
    await ctx.send("`deleted successfully`")
  except:
    await ctx.send('`error`')

@client.command()
async def current(ctx, *args):
  id = ctx.author.id
  new_data = {}
  filename = str(id)+".json"
  try:
    with open("data/"+filename, 'r') as f:
      data = json.load(f)
    await ctx.send("`Browsing through amazon`")
    new_data = tracker(((data["items"])[int(args[0])-1])["url"], ((data["items"])[int(args[0])-1])["alert"])
    await ctx.send("Value of `"+new_data["name"] + "` is `₹"+ str(new_data["current"])+ "`")
    ((data["items"])[int(args[0])-1])["current"] = new_data["current"]
    with open("data/"+filename, "w") as f:
      json.dump(data, f, indent =2)
  except:
    await ctx.send('`error`')

@client.command()
async def update(ctx): 
  print('working')
  channelid = 0 #provides the updates in the channel with this id
  channel = client.get_channel(channelid)
  with open("data/"+'allusers.json', 'r') as f:
    li = json.load(f)
  i = 0
  data = {

  }
  for user in li["ids"]:
    with open("data/"+user+".json", "r") as f:
      item = json.load(f)
    for product in item["items"]:
      new_data = {}
      new_data = ftracker(product["url"], product["alert"])
      product["current"] = new_data["current"]
      product["alert"] = new_data["current"]
      if(new_data["is_Sale"]):
        await channel.send('<@!'+user+'> '+ 'The product `'+str(new_data["name"])+'` is on discount.\n Old price: `₹'+ str(new_data["alert"])+'`\n Current price: `₹'+ str(new_data["current"])+'`')
        item["items"].pop(i)
        
        data= {
          "name": new_data["name"],
          "current": new_data["current"],
          "alert": new_data["current"],
          "url": new_data["url"],
          "is_sale": False
        }
        item["items"].append(data)
        with open("data/"+user+".json", "w") as f:
          json.dump(item, f, indent = 4)
      i+=1


@client.command()
async def ss(ctx, *args):
  try:
    url = args[0]
    await ctx.send('`Browsing...`' )
    screen(url)
    await ctx.send('`Taking screenshot...`')
    with open('ss.png','rb') as f:
      pic = discord.File(f)
      await ctx.send(file = pic)
  except:
    await ctx.send('`error`')





      
my_secret = os.environ['token']
client.run(my_secret)
