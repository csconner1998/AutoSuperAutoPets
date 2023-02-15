import pyautogui
import generateToken
import socket
import os
import emoji
import threading
import cv2
import numpy as np
from PIL import ImageGrab
import time

# globals
server = os.getenv('server')
port = os.getenv('port')
nickname = os.getenv('nickname')
token = generateToken.getAccessToken()
channel = os.getenv('channel')
twitchChat = {}
authorList = []
needInput = False


def stopThread():
    global stopped
    stopped = True

def isValidMove(moveStr):
    if moveStr == "sell" or moveStr == "freeze" or moveStr == "roll" or moveStr == "end" or moveStr == "play" or moveStr == "pet" or moveStr == "turtle" or moveStr == "golden" or moveStr == "puppy" or moveStr == "star" or moveStr == "weekly" or moveStr == "back":
        return True
    #split movestring into two parts
    elif len(moveStr.split(" ")) == 2:
        #check if first part is a number
        if moveStr.split(" ")[0].isdigit() and int(moveStr.split(" ")[0]) > 0 and int(moveStr.split(" ")[0]) < 13:
            #check if second part is a number
            if (moveStr.split(" ")[1].isdigit() and int(moveStr.split(" ")[1]) > 0 and int(moveStr.split(" ")[1]) < 13) or moveStr.split(" ")[1] == "freeze" or moveStr.split(" ")[1] == "sell":
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def getMove(moveStr):
    if moveStr == "roll":
        return (13,0)
    elif moveStr == "end":
        return (14,0)
    elif len(moveStr.split(" ")) == 2:
        if moveStr.split(" ")[1] == "freeze":
            return (int(moveStr.split(" ")[0]), 15)
        elif moveStr.split(" ")[1] == "sell":
            return (int(moveStr.split(" ")[0]), 15)
        return (int(moveStr.split(" ")[0]), int(moveStr.split(" ")[1]))
    else:
        return moveStr

def thread_function():
    global stopped, twitchChat, authorList
    sock = socket.socket()
    sock.connect((server, int(port)))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))
    while True and not stopped:
        resp = sock.recv(2048).decode('utf-8')
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            chatMsg = resp.split("l :")
            if len(chatMsg) > 1:
                clensedChatMsg = emoji.demojize(
                    chatMsg[1].rstrip("\n\r")).lower()
                author = resp.split("!")[0][1:]
                if needInput and author not in authorList and isValidMove(clensedChatMsg):
                    twitchInput = getMove(clensedChatMsg)
                    print(f"Got input from twitch: {twitchInput}")
                    if twitchInput not in twitchChat:
                        twitchChat[twitchInput] = 1
                    else:
                        twitchChat[twitchInput] += 1
                    print(twitchChat)

# Checks if image is in the screen


def check_if_image_on_screen(image_path, threshold=0.8):
    # Load the image to search for
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Capture the screen
    screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Perform template matching to search for the image
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)

    # Get the coordinates of the matching area
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        return True
    else:
        return False


if __name__ == "__main__":
    x = threading.Thread(target=thread_function, args=())
    x.start()
    stopped = False
    toNumber = 0
    fromNumber = 0
    timer = 10
    while True:
        # Write timer to timer.txt
        with open("timer.txt", "w") as f:
            f.write("Timer: " + str(int(timer)))
            f.close()
        if check_if_image_on_screen("Arena Mode.png"):
            needInput = True
            print("Arena Mode is on screen")
            pyautogui.keyDown('insert')
            time.sleep(0.05)
            pyautogui.keyUp('insert')
            if timer != 0:
                timer -= 0.5
            else:
                # Check if play or pet has more votes
                if "play" in twitchChat and "pet" in twitchChat:
                    if twitchChat["play"] >= twitchChat["pet"]:
                        pyautogui.click(750, 400)
                    else:
                        pyautogui.click(1500, 250)
                elif "play" in twitchChat:
                    pyautogui.click(750, 400)
                elif "pet" in twitchChat:
                    pyautogui.click(1500, 250)
                timer = 10
                twitchChat = {}
                authorList = []
        elif check_if_image_on_screen("packs.png"):
            needInput = True
            print("Packs is on screen")
            pyautogui.keyDown('end')
            time.sleep(0.05)
            pyautogui.keyUp('end')
            if timer != 0:
                timer -= 0.5
            else:
                # checks the max votes between turtle, golden, puppy, star and weekly
                print(twitchChat)
                turtleVotes = 0
                goldenVotes = 0
                puppyVotes = 0
                starVotes = 0
                weeklyVotes = 0
                backVotes = 0
                max = 0
                winner = ""
                if "turtle" in twitchChat:
                    turtleVotes = twitchChat["turtle"]
                    if turtleVotes > max:
                        max = turtleVotes
                        winner = "turtle"
                if "golden" in twitchChat:
                    goldenVotes = twitchChat["golden"]
                    if goldenVotes > max:
                        max = goldenVotes
                        winner = "golden"
                if "puppy" in twitchChat:
                    puppyVotes = twitchChat["puppy"]
                    if puppyVotes > max:
                        max = puppyVotes
                        winner = "puppy"
                if "star" in twitchChat:
                    starVotes = twitchChat["star"]
                    if starVotes > max:
                        max = starVotes
                        winner = "star"
                if "weekly" in twitchChat:
                    weeklyVotes = twitchChat["weekly"]
                    if weeklyVotes > max:
                        max = weeklyVotes
                        winner = "weekly"
                if "back" in twitchChat:
                    backVotes = twitchChat["back"]
                    if backVotes > max:
                        max = backVotes
                        winner = "back"
                print(winner)
                if winner == "turtle":
                    pyautogui.click(180, 550)
                elif winner == "golden":
                    pyautogui.click(572, 550)
                elif winner == "star":
                    pyautogui.click(964, 550)
                elif winner == "puppy":
                    pyautogui.click(1356, 550)
                elif winner == "weekly":
                    pyautogui.click(1750, 550)
                elif winner == "back":
                    pyautogui.click(180, 1000)
                timer = 10
                twitchChat = {}
                authorList = []
        elif check_if_image_on_screen("Battle.png"):
            print("Battle is on screen")
            needInput = True
            pyautogui.keyDown('pageup')
            time.sleep(0.05)
            pyautogui.keyUp('pageup')
            if timer != 0:
                timer -= 0.5
            else:
                needInput = False
                max = 0
                fromNumber = 0
                toNumber = 0
                for key, value in twitchChat.items():
                    if len(key) != 2:
                        continue
                    if value > max:
                        max = value
                        fromNumber = key[0]
                        toNumber = key[1]
                print(f"From: {fromNumber} To: {toNumber}")
                if max == 0:
                    timer = 10
                    twitchChat = {}
                    authorList = []
                    continue
                if fromNumber == 13:
                    pyautogui.click(200, 1000)
                    time.sleep(0.2)
                elif fromNumber == 14:
                    pyautogui.click(1700, 1000)
                    time.sleep(0.2)
                else:
                    if fromNumber < 6:
                        pyautogui.click(540 + (fromNumber - 1) * 145, 400)
                        time.sleep(0.2)
                    elif fromNumber == 15:
                        pyautogui.click(1000, 1000)
                        time.sleep(0.2)
                    else:
                        pyautogui.click(540 + (fromNumber - 6) * 145, 700)
                        time.sleep(0.2)
                    if toNumber < 6:
                        pyautogui.click(540 + (toNumber - 1) * 145, 400)
                        time.sleep(0.2)
                    elif toNumber == 15:
                        pyautogui.click(1000, 1000)
                        time.sleep(0.2)
                    else:
                        pyautogui.click(540 + (toNumber - 6) * 145, 700)
                        time.sleep(0.2)
                pyautogui.click(1700, 700)
                timer = 10
                toNumber = 0
                fromNumber = 0
                twitchChat = {}
                authorList = []

                # if fromPicked and toDone:
                #     needInput = False
                #     if fromNumber == 13 or toNumber == 13:
                #         pyautogui.click(200, 1000)
                #         time.sleep(0.2)
                #     elif fromNumber == 14 or toNumber == 14:
                #         pyautogui.click(1700, 1000)
                #         time.sleep(0.2)
                #     else:
                #         if fromNumber < 6:
                #             pyautogui.click(540 + (fromNumber - 1) * 145, 400)
                #             time.sleep(0.2)
                #         elif fromNumber == 15:
                #             pyautogui.click(1000, 1000)
                #             time.sleep(0.2)
                #         else:
                #             pyautogui.click(540 + (fromNumber - 6) * 145, 700)
                #             time.sleep(0.2)
                #         if toNumber < 6:
                #             pyautogui.click(540 + (toNumber - 1) * 145, 400)
                #             time.sleep(0.2)
                #         elif toNumber == 15:
                #             pyautogui.click(1000, 1000)
                #             time.sleep(0.2)
                #         else:
                #             pyautogui.click(540 + (toNumber - 6) * 145, 700)
                #             time.sleep(0.2)
                #     pyautogui.click(1700, 700)
                #     fromPicked = False
                #     timer = 10
                #     toDone = False
                #     toNumber = 0
                #     fromNumber = 0
                # elif fromPicked:
                #     needInput = True
                #     # Get the most picked number
                #     max = 0
                #     for key, value in twitchChat.items():
                #         if not isinstance(key, int):
                #             continue
                #         if value > max:
                #             max = value
                #             toNumber = key
                #     if not max == 0:
                #         toDone = True
                #     else:
                #         timer = 10
                #     twitchChat = {}
                #     authorList = []
                # else:
                #     needInput = True
                #     # Get the most picked number
                #     max = 0
                #     for key, value in twitchChat.items():
                #         # if key isn't an instance of int, skip it
                #         if not isinstance(key, int):
                #             continue
                #         if value > max:
                #             max = value
                #             fromNumber = key
                #     if not max == 0:
                #         fromPicked = True
                #     if fromNumber == 13 or fromNumber == 14:
                #         fromPicked = True
                #         toDone = True
                #     else:
                #         timer = 10
                #     twitchChat = {}
                #     authorList = []
        elif check_if_image_on_screen("Pause.png"):
            needInput = False
            print("Pause is on screen")
            pyautogui.keyDown('home')
            time.sleep(0.05)
            pyautogui.keyUp('home')
            print("Battling")
        elif check_if_image_on_screen("endBattle.png") or check_if_image_on_screen("endBattle2.png"):
            needInput = False
            print("endBattle is on screen")
            pyautogui.click(1700, 700)
            time.sleep(3)
            pyautogui.click(1700, 700)
        elif check_if_image_on_screen("extraGold.png"):
            needInput = False
            print("extraGold is on screen")
            pyautogui.click(700, 700)
            pyautogui.click(1700, 700)
        elif check_if_image_on_screen("gainLife.png"):
            print("gainLife is on screen")
            pyautogui.click(1500, 150)
        else:
            print("Nothing is on screen")
            pyautogui.keyDown('home')
            time.sleep(0.05)
            pyautogui.keyUp('home')

        time.sleep(0.5)
