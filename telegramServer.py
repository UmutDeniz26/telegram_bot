token=""

# -*- coding: utf-8 -*-
import pyautogui as pag
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time,os,cv2
import functions as opr
import attributes as atr
os.system('cls')
print("Remote Bot has started!")

songIndex=1
indexOrder=[0]

#Command Functions
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"""Commands:
    /help
    
    /open [parameter]
    Parameter list: [ primeVideo, ogubs, youtube, github, chatgpt]
    
    /startSong, /nextSong,
    /shutDownComputer, /resetComputer, /altf4,
    /chatGPTlocal, /takePhoto""")
    print("Command requested: Help")

async def altf4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pag.hotkey('alt','f4')
    print("Command requested: altf4")
    await update.message.reply_text(f'Task completed successfully: ALT+F4')
    
async def shutDownComputer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    opr.executeCmd("shutdown /s")
    await update.message.reply_text(f'Task completed successfully: shutDownComputer')

async def resetComputer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    opr.executeCmd("shutdown /r")
    await update.message.reply_text(f'Task completed successfully: resetComputer')

async def chatGPTlocal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        opr.executeCmd("start OpenAI.exe.lnk")
        print("Command requested: chatGPTlocal")
        await update.message.reply_text(f'Task completed successfully: chatGPTlocal')
    except:
        print("ERROR -> chatGPTlocal")

async def takePhoto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        [result,image,screenshot]=opr.takePhotoAndScreenShot()
        screenshot.save('assets/temp/screenshot.jpg')
        cv2.imwrite('assets/temp/webcam.jpg', image)
        if result:
            await update.message.reply_photo('./assets/temp/screenshot.jpg',caption="Ekran Görüntüsü")
            await update.message.reply_photo('./assets/temp/webcam.jpg',caption="Kamera Görüntüsü")
            print("Command requested: takePhoto")
        else:
            await update.message.reply_text(f"ERROR -> takePhoto")
    except:
        print("ERROR -> takePhoto")

async def startSong(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        opr.openSong(indexOrder[0])
        print("Command requested: startSong")
        await update.message.reply_text(f'Task completed successfully: startSong')
    except:
        print("ERROR -> startSong")

async def nextSong(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global songIndex,indexOrder
        opr.nextSong(indexOrder[songIndex])
        songIndex+=1
        nextSongName=atr.songUris[indexOrder[songIndex]]['name']
        print("Command requested: nextSong, next song is{}".format(nextSongName))
        await update.message.reply_text(
            "Task completed successfully: nextSong (Next song: {} )"
            .format(nextSongName))
    except:
        print("ERROR -> nextSong")
async def open(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        parameter= str(opr.getParamsFromMessage(update.message.text)[0]).lower()
        isParameterNotFound=True
        for element in atr.paramLinks:
            if element['parameter']==parameter:
                isParameterNotFound=False
                opr.executeCmd('start {}'.format(element['link']))
                print("Command requested: open {}".format(element["parameter"]))
                await update.message.reply_text('Task completed successfully: Open ( {} )'
                .format(element["parameter"]))
                break
        
        if isParameterNotFound:
            await update.message.reply_text(f'Unrecognized parameter')
            print("Command requested: open ( Unrecognized Parameter )")
    except:
        print("ERROR -> open")

#Telegram Side
app = ApplicationBuilder().token(token).build()
functions=[
    startSong,nextSong,altf4,shutDownComputer
    ,help,chatGPTlocal,takePhoto,open,resetComputer
    ]

#Commands definations
for function in functions:
    app.add_handler(CommandHandler(function.__name__,function))
app.run_polling()