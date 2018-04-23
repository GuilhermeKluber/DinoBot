from scanner import Scanner
from network import Network
from time import sleep
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
        self.f = open('regGenome.csv', 'a+')
        self.csv_writer = csv.writer(self.f, delimiter=',')
        #self.csv_writer.writerow(['W1[0]','W1[1]','W1[2]','W1[3]','W1[4]','W2[0]','W2[1]','W2[2]','W2[3]','W1[4]' , 'Fitness'])
        self.f.flush()

    def execute(self,lx,ly,rx,ry,epoch):
        scanner = Scanner(lx,ly,rx,ry)
        show_fitness = [ ]
        pyautogui.keyDown('ctrl')
        pyautogui.press('r')
        pyautogui.keyUp('ctrl')
        for genome in self.__genomes:
            scanner.reset()
            sleep(1)
            game_over=False
            keyboard.press("space")
            keyboard.release("space")
            while True:
                if not game_over:
                    obs,game_over = scanner.find_next_obstacle(game_over)
                    #print("Dist e {} , Largura {} Altura {} Speed e {}".format(1-((260-obs['distance'])/(260)),obs['length']/100,obs['height']/100,obs['speed']/10))
                    inputs = [1-((260-obs['distance'])/(260)) ,obs['length']/100,obs['height']/100, obs['speed'] / 10]
                    #inputs = [1-((260-obs['distance'])/(260)) ,obs['height']/100, obs['speed'] / 10]
                    outputs = genome.forward(np.array(inputs, dtype=float))
                    #print(outputs[0])
                    if outputs[0] > 0.55:
                        pyautogui.keyUp('down')
                        pyautogui.press('space')
                    elif outputs[0] < 0.45:
                        pyautogui.keyDown('down')
                    else:
                        pyautogui.keyUp('down')
                else:
                    break
            genome.fitness = scanner.get_fitness()
            show_fitness.append(genome.fitness)
        print("Fitness desta geracao [{}]".format(show_fitness))

    def keep_best_genomes(self):
        self.__genomes.sort(key=lambda x: x.fitness, reverse=True)
        self.__genomes = self.__genomes[:4]
        self.csv_writer.writerow([self.__genomes[0].W1[0],self.__genomes[0].W1[1],self.__genomes[0].W1[2],self.__genomes[0].W1[2],
                        self.__genomes[0].W2[0],self.__genomes[0].W2[1],self.__genomes[0].W2[2],self.__genomes[0].W2[3],
                        self.__genomes[0].fitness])
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
