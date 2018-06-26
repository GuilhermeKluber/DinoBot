from scanner import Scanner
from network import Network,Load_Network
from time import sleep
from pynput import keyboard as Pkeyboard
import pyautogui
import csv
import cv2
import numpy as np
import random
import copy
import pyautogui
import keyboard
import time

class Generation:
    def __init__(self):
        self.__genomes = [Network() for i in range(12)]
        self.__best_genomes = []
        #self.net = Load_Network()

    def execute(self,lx,ly,rx,ry,epoch):
        scanner = Scanner(lx,ly,rx,ry)
        show_fitness = []
        pyautogui.keyDown('ctrl')
        pyautogui.press('r')
        pyautogui.keyUp('ctrl')
        last=0;
        for genome in self.__genomes:
            scanner.reset()
            sleep(1)
            game_over=False
            keyboard.press("space")
            keyboard.release("space")
            while True:
                if not game_over:
                    obs,game_over = scanner.find_next_obstacle(game_over)
                    #print("Dist e {} , Largura {} Altura {} Speed e {}".format(int(100*(1-((260-obs['distance'])/(260)))),obs['length']/100,obs['height']/100,obs['speed']/10))
                    #inputs = [1-((260-obs['distance'])/(260)) ,obs['length']/100,obs['height']/100, obs['speed'] / 10,obs['moviment']]
                    inputs = [1-((260-obs['distance'])/(260)) ,obs['length']/100, obs['speed'] / 10]
                    #self.inputwriter.writerow([inputs[0],inputs[1],inputs[2],inputs[3]])
                    #self.outputwriter.writerow([inputs[4]])
                    output = genome.forward(np.array(inputs, dtype=float))
                    if output != last:
                        start = time.time()
                        last = output
                    elif time.time() - start > 10:
                        game_over = True
                        print("Game Over!!!")
                    #output = self.net.predict(inputs)
                    #print(output)
                    self.play(output,obs['height']/100)
                else:
                    break
            genome.fitness = scanner.get_fitness()
            show_fitness.append(genome.fitness)
        image = pyautogui.screenshot(region=(lx,ly, rx-lx+160, ry-ly))
        image = np.array(image)
        cv2.imwrite("./scores/Score_{}.jpg".format(epoch),image)
        print("Fitness desta geracao [{}]".format(show_fitness))

    def play(self,output, altura):
        if output[0] > 0.55 and altura < 0.3:
            #pyautogui.keyUp('down')
            #pyautogui.press('space')
            keyboard.release("down")
            keyboard.press("space")
            #time.sleep(0.1)
        elif output[0] > 0.55 and altura > 0.3:
            #pyautogui.keyDown('down')
            keyboard.release("space")
            keyboard.press("down")
        else:
            keyboard.release("space")
            keyboard.release("down")
            #pyautogui.keyUp('down')

    def keep_best_genomes(self):
        self.__genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.__genomes = self.__genomes[:4]
        self.__best_genomes = self.__genomes[:]

    def mutations(self):
        while len(self.__genomes) < 10:
            genome1 = random.choice(self.__best_genomes)
            genome2 = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(self.cross_over(genome1, genome2)))
        while len(self.__genomes) < 12:
            genome = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(genome))

    def cross_over(self, genome1, genome2):
        new_genome = copy.deepcopy(genome1)
        other_genome = copy.deepcopy(genome2)
        cut_location = int(len(new_genome.W1) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W1[i], other_genome.W1[i] = other_genome.W1[i], new_genome.W1[i]
        cut_location = int(len(new_genome.W2) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W2[i], other_genome.W2[i] = other_genome.W2[i], new_genome.W2[i]
        return new_genome

    def __mutate_weights(self, weights):
        if random.uniform(0, 1) < 0.2:
            return weights * (random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
        else:
            return 0

    def mutate(self, genome):
        new_genome = copy.deepcopy(genome)
        new_genome.W1 += self.__mutate_weights(new_genome.W1)
        new_genome.W2 += self.__mutate_weights(new_genome.W2)
        return new_genome
