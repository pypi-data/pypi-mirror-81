import os
import keyboard
os.system("@echo off")
colordict = {"black":"0","gray":"8","blue":"1","L_blue":"9","green":"2","L_green":"A","aqua":"3","L_aqua":"B","red":"4","L_red":"C"}
def fs():
    keyboard.press_and_release('alt+enter')
def efs():
    keyboard.press_and_release('alt+enter')
def addline(txt):
    os.system("echo "+txt)
def clear():
    os.system("cls")
def color(colorfg,colorbg):
    try:
      colorfgcode=colordict[colorfg]
    except:
        quit("unknown color {} ):".format(colorfg))
    try:
        colorbgcode = colordict[colorbg]
    except:
        quit("unknown color {} ):".format(colorbg))
    os.system("color {}{}".format(colorbgcode,colorfgcode))

def fancyline(color1,color2,text):
    color(color1,color2)
    addline(text)
    color("white","black")
