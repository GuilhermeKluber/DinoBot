from datetime import datetime
import numpy as np
import cv2
import os
import webbrowser
import time
import pyautogui

def compare(img,col):
    im = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    diff=im
    diff[im != col[0]] = 0
    diff[im == col[0]] = 255
    diff = diff.astype(np.uint8)
    return diff

def get_location():
    url = "http://google.com"
    webbrowser.open(url)

    time.sleep(3)
    # pyautogui.keyDown('win')
    # pyautogui.press('left')
    # pyautogui.keyUp('win')
    # pyautogui.click(x=100, y=600)
    # image size is 47x50
    try:
        lx, ly, w, h = pyautogui.locateOnScreen("./images/t_rex.png")
    except:
        print("Game Not Found")
        raise Exception("Game not found!")
    ly += h
    pyautogui.press("space")
    time.sleep(2)
    try:
        t_rex, _, w, h = pyautogui.locateOnScreen("./images/t_rex_head.png")
    except:
        print("Game Not Found")
        raise Exception("Game not found!")
    t_rex += w
    time.sleep(8)
    try:
        rx, ry, w, h = pyautogui.locateOnScreen("./images/hi.png")
    except:
        print("Game Not Found")
        raise Exception("Game not found!")
    ly, ry = ry, ly
    # left, top, right, bottom, t_rex
    return lx,ly,rx,ry

def screenshot(x, y, w, h):
    url = "http://google.com"
    webbrowser.open(url)
    time.sleep(3)

    return img

def obstacle(distance, length, speed, time,height):
    return { 'distance': distance, 'length': length, 'speed': speed, 'time': time,'height':height }

class Scanner:
    def __init__(self,lx,ly,rx,ry):
        self.dino_start = (0, 0)
        self.dino_end = (0, 0)
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False
        self.inte=0
        self.hist_color_dino = np.zeros(10)
        self.lx,self.ly,self.rx,self.ry = lx,ly,rx,ry

    def find_next_obstacle(self,game_over):
        dist,game_over,length,height = self.__next_obstacle_dist(game_over)
        if dist < 50 and not self.__change_fitness:
            self.__current_fitness += 1
            self.__change_fitness = True
        elif dist > 50:
            self.__change_fitness = False
        time = datetime.now()
        delta_dist = 0
        speed = 0
        if self.last_obstacle:
            delta_dist = self.last_obstacle['distance'] - dist
            speed = (delta_dist / ((time - self.last_obstacle['time']).microseconds)) * 10000
        self.last_obstacle = obstacle(dist, length, speed, time,height)
        return self.last_obstacle,game_over

    def __next_obstacle_dist(self,game_over):
        s = 0
        length = 0
        height=0
        image = pyautogui.screenshot(region=(self.lx,self.ly, self.rx-self.lx+160, self.ry-self.ly-10))
        size = image.size
        DinoColor = image.getpixel((size[0]-40,15))
        if self.inte == 0:
            self.hist_color_dino[0]=DinoColor[0]
            self.inte+=1
        elif self.inte == self.hist_color_dino.size:
            self.inte=0
            self.hist_color_dino[0]=DinoColor[0]
        else:
            self.hist_color_dino[self.inte]=DinoColor[0]
            self.inte+=1
        self.hist_color_dino.sort()
        aux=0
        aux2=0
        DinoColor = [0,0,0]
        DinoColor_aux = [0,0,0]
        for j in range(1,self.hist_color_dino.size):
            if self.hist_color_dino[j] == self.hist_color_dino[j-1]:
                DinoColor[0]=self.hist_color_dino[j-1]
                DinoColor[1]=self.hist_color_dino[j-1]
                DinoColor[2]=self.hist_color_dino[j-1]
                aux+=1
            elif aux >= aux2:
                DinoColor_aux[0]=self.hist_color_dino[j-1]
                DinoColor_aux[1]=self.hist_color_dino[j-1]
                DinoColor_aux[2]=self.hist_color_dino[j-1]
                aux2=aux
                aux=0
        if aux2 > aux:
            DinoColor=DinoColor_aux
        image = pyautogui.screenshot(region=(self.lx,self.ly, self.rx-self.lx, self.ry-self.ly-10))
        image = np.array(image)
        th = compare(image,DinoColor)
        x_aux=1000000
        count=0
        opa, contours, _= cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 1:
            for c in contours:
                x,y,w,h = cv2.boundingRect(c)
                if cv2.contourArea(c)>900 and cv2.contourArea(c)<1000:
                    if (x > size[0]/2-30) and (y < size[1]-10):
                        game_over=True
                        print("Game Over")
                        return 1000000,game_over,0, 0

                if cv2.contourArea(c)>120 and cv2.contourArea(c)<450:
                    if x == size[0]:
                        count+=1
                    if (x-x_aux) < 30 :
                        count+=1
                    if x < x_aux and x >70:
                        length=w
                        x_aux=x
                        height=size[1]-y
                        count+=1
            if x_aux > 70 and x_aux < size[0]:
                return (x_aux-70), game_over, length*count, height

        return 10000000,game_over,0, 0

    def reset(self):
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def get_fitness(self):
        return self.__current_fitness
