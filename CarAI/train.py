import sys
import math
import pygame
import neat
from pathlib import Path
import os
from random import randint
import time
import matplotlib.pyplot as plt
import pickle

def translate_point(point, angle, distance):
    radians = math.radians(angle)
    return int(point[0] + distance * math.cos(radians)),\
        int(point[1] + distance * math.sin(radians))

class Car:
    def __init__(self):
        self.corners = []
        self.edge_points = []
        self.edge_distances = []
        self.travelled_distance = 0
        self.angle = 0
        self.Spawn = Spawn
        self.last = Spawn
        self.car = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'car{}.png'.format(randint(1,9)))))
        self.car = pygame.transform.scale(self.car, CAR_SIZE)
        self.crashed = False
        self.update_sensor_data()

    def display_car(self):
        rotated_car = pygame.transform.rotate(self.car, self.angle)
        rect = rotated_car.get_rect(center=self.Spawn)
        SCREEN.blit(rotated_car, rect.topleft)

    def crash_check(self):
        for corner in self.corners:
            if TRACK.get_at(corner) in Border:
                return True
        return False

    def update_sensor_data(self):
        angles = [360 - self.angle, 90 - self.angle, 180 - self.angle]
        angles = [math.radians(i) for i in angles]
        edge_points = []
        edge_distances = []
        for angle in angles:
            distance = 0
            edge_x, edge_y = self.Spawn
            while TRACK_COPY.get_at((edge_x, edge_y)) not in Border:
                edge_x = int(self.Spawn[0] + distance * math.cos(angle))
                edge_y = int(self.Spawn[1] + distance * math.sin(angle))
                distance += 1
            edge_points.append((edge_x, edge_y))
            edge_distances.append(distance)
        self.edge_points = edge_points
        self.edge_distances = edge_distances


    def display_edge_points(self):
        
        for point in self.edge_points:
           
            # if self.last[1]!=self.Spawn[1]:
            #     if self.last[1]<self.Spawn[1]:
            #         pygame.draw.line(SCREEN, (67, 153, 162, 255), (self.Spawn[0]+40,self.Spawn[1]-70), (self.Spawn[0]-40,self.Spawn[1]-70),width=5)
            #     if self.last[1]>self.Spawn[1]:
            #         pygame.draw.line(SCREEN, (67, 153, 162, 255), (self.Spawn[0]-40,self.Spawn[1]+70), (self.Spawn[0]+40,self.Spawn[1]+70),width=5)
            # if self.last[0]!=self.Spawn[0]:
            #     if self.last[0]<self.Spawn[0]:
            #         pygame.draw.line(SCREEN,(67, 153, 162, 255), (self.Spawn[0]-70,self.Spawn[1]-40), (self.Spawn[0]-70,self.Spawn[1]+40),width=5)
            #     if self.last[0]>self.Spawn[0]:
            #         pygame.draw.line(SCREEN, (67, 153, 162, 255), (self.Spawn[0]+70,self.Spawn[1]+40), (self.Spawn[0]+70,self.Spawn[1]-40),width=5)
            # self.last = self.Spawn
            
            pygame.draw.line(SCREEN, (255,0,255), self.Spawn, point)
            pygame.draw.circle(SCREEN, (255,0,255), point, 5)

    def update_position(self):
        self.Spawn = translate_point(
            self.Spawn, 90 - self.angle, Speed)
        self.travelled_distance += Speed
        dist = math.sqrt(CAR_SIZE[0]**2 + CAR_SIZE[1]**2)/2
        corners = []
        corners.append(translate_point(
            self.Spawn, 60 - self.angle, dist))
        corners.append(translate_point(
            self.Spawn, 120 - self.angle, dist))
        corners.append(translate_point(
            self.Spawn, 240 - self.angle, dist))
        corners.append(translate_point(
            self.Spawn, 300 - self.angle, dist))
        self.corners = corners


def run(genomes, config):
    global GENERATION,lines,fps,TRACK,TRACK_COPY,Spawn
    GENERATION += 1
    models = []
    cars = []

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        models.append(net)
        genome.fitness = 0
        cars.append(Car())
    starttime = time.time()
    lasttime = starttime
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_l]:
            if lines:
                lines = False
            else:
                lines = True
        if keys_pressed[pygame.K_x]:
            if fps <120:
                fps+=1
        if keys_pressed[pygame.K_z]:
            if fps >5:
                fps-=1
        if keys_pressed[pygame.K_1]:
            TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track1.png'))).convert_alpha()
            TRACK = pygame.transform.scale(TRACK,(900,900))
            TRACK_COPY = TRACK.copy()
            Spawn = 70, 800
        if keys_pressed[pygame.K_2]:
            TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track2.png'))).convert_alpha()
            TRACK = pygame.transform.scale(TRACK,(900,900))
            TRACK_COPY = TRACK.copy()
            Spawn = 820, 300
        # if keys_pressed[pygame.K_3]:
        #     TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track3.jpg'))).convert_alpha()
        #     TRACK = pygame.transform.scale(TRACK,(850,850))
        #     TRACK_COPY = TRACK.copy()
        #     Spawn = 70, 200
                
        running_cars = 0

        SCREEN.blit(TRACK,(0,0))

        for i, car in enumerate(cars):
            if not car.crashed:
                running_cars += 1
                output = models[i].activate(car.edge_distances)
                choice = output.index(max(output))
                if choice == 0:
                    car.angle += Turn
                elif choice == 1:
                    car.angle -= Turn
                car.update_position()
                car.display_car()
                car.crashed = car.crash_check()
                car.update_sensor_data()
                genomes[i][1].fitness += car.travelled_distance
                if lines:
                    car.display_edge_points()
                

        if running_cars == 0:
            G_Data.append(GENERATION)
            T_Data.append(laptime)
            plt.plot(G_Data,T_Data)
            plt.draw()
            return
        laptime = round((time.time() - lasttime)*(fps/24), 2)
        msg = "Generation: {}, Cars: {}, Time alive {}".format(GENERATION, running_cars,laptime)
        text = FONT.render(msg, 1, (255,255,255))
        SCREEN.blit(text, (200, -7))
        sp = "Speed: {}".format(fps)
        text2 = FONT.render(sp, 1, (255,255,255))
        SCREEN.blit(text2, (400, 860))
        pygame.display.update()
        CLOCK.tick(fps)
        
def save_ai(filename,net):
    with open(str(os.fspath(Path(__file__).resolve().parent / filename)), "wb") as f:
        pickle.dump(net, f)
        f.close()

def load_ai(filename):
    with open(str(os.fspath(Path(__file__).resolve().parent / filename)), "rb") as f:
        genome = pickle.load(f)
        f.close()
    return genome


# if __name__ == "__main__":
pygame.init()
pygame.display.set_caption("Self Driving Car")
WIN = 900, 900
SCREEN = pygame.display.set_mode(WIN)

Spawn = 70, 800
Speed = 10
Turn = 27

CAR_SIZE = 25,50
Border = [(67, 153, 162, 255),(154, 239, 254, 255),(136, 219, 91, 255),(67, 153, 162, 255),(23, 57, 170, 255)]
TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track1.png'))).convert_alpha()
TRACK = pygame.transform.scale(TRACK,(900,900))
TRACK_COPY = TRACK.copy()
FONT = pygame.font.SysFont("Grand9K Pixel", 30)
plt.style.use("dark_background")
plt.ion()
plt.title("AI Evolution")
plt.xlabel("Generation")
plt.ylabel("Time Alive")

CLOCK = pygame.time.Clock()
GENERATION = 0

lines = True
fps = 24

G_Data =[]
T_Data = []
neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                str(os.fspath(Path(__file__).resolve().parent / "config.txt")))

population = neat.Population(neat_config)

population = load_ai("best.pickle")
# population.add_reporter(neat.StdOutReporter(True))
# stats = neat.StatisticsReporter()
# population.add_reporter(stats)

population.run(run, 100)
save_ai("best.pickle",population)
