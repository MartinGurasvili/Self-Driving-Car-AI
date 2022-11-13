import sys
import math
import pygame
import neat
from pathlib import Path
import os
from random import randint
import time
import joblib

resett = True

    
ploss = False
def translate_point(point, angle, distance):
    radians = math.radians(angle)
    return int(point[0] + distance * math.cos(radians)),\
        int(point[1] + distance * math.sin(radians))
        
def rotate_image(win,image,top_left,angle):
        rotated_image = pygame.transform.rotate(image,angle)
        new_rect = rotated_image.get_rect(center =top_left)
        win.blit(rotated_image,new_rect.topleft)

def changeploss():
    global ploss
    ploss = True
class PlayerCar:
    
    def __init__(self,max_vel):
        self.img = CARp
        self.max_vel = max_vel
        self.vel = 0
        self.angle = 180
        self.x,self.y = Spawn
        self.acc = 0.3
        
    def draw(self,win):
        rotate_image(win,self.img,(self.x,self.y ),self.angle)
        if TRACK.get_at((int(self.x), int(self.y))) in Border:
            self.x,self.y = Spawn
            self.angle = 180
            self.vel = 0
            text =FONT.render("You Lost", 1, (255,255,255))
            SCREEN.blit(text, (200, 400))
            
            CARp = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "car{}.png".format(randint(1,9)))))
            CARp = pygame.transform.rotate(CARp,180)
            CARp = pygame.transform.scale(CARp,(CAR_SIZE[0]-3,CAR_SIZE[1]-6))
            self.img = CARp
            pygame.display.update()
            time.sleep(2)
            changeploss()
        

    def forward(self):
        self.vel = min(self.vel + self.acc,self.max_vel)
        
        self.move()
        
    
        
    def move(self):
        self.img = CARp
        radians = math.radians(self.angle)
        
        vert = math.cos(radians) * self.vel
        horz = math.sin(radians) * self.vel
        
        self.y -= vert
        self.x -= horz
    def momentum(self):
        self.vel = max(self.vel - self.acc / 2,0)
        
        self.move()
        

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
        angles = [360 - self.angle, 90 - self.angle, 180 - self.angle,45 - self.angle, 135- self.angle,70 - self.angle, 110- self.angle]
        angles = [math.radians(i) for i in angles]
        
        edge_points = []
        edge_distances = []
        for angle in angles:
            distance = 0
            edge_x, edge_y = self.Spawn
            try:
                while TRACK_COPY.get_at((edge_x, edge_y)) not in Border :
                    distance += 1
                    edge_x = int(self.Spawn[0] + distance * math.cos(angle))
                    edge_y = int(self.Spawn[1] + distance * math.sin(angle))
            except:
                f=0
            edge_points.append((edge_x, edge_y))
            edge_distances.append(distance)
        self.edge_points = edge_points
        self.edge_distances = edge_distances


    def display_edge_points(self):
        
        for point in self.edge_points:
            
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
    global GENERATION,lines,fps,TRACK,TRACK_COPY,Spawn,resett,countdown
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
        
        if keys_pressed[pygame.K_1]:
            TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track1.png'))).convert_alpha()
            TRACK = pygame.transform.scale(TRACK,(900,900))
            TRACK_COPY = TRACK.copy()
            Spawn = 70, 800
            resett = True
        if keys_pressed[pygame.K_2]:
            TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track2.png'))).convert_alpha()
            TRACK = pygame.transform.scale(TRACK,(900,900))
            TRACK_COPY = TRACK.copy()
            Spawn = 820, 300
            resett = True
        if keys_pressed[pygame.K_3]:
            TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track3.png'))).convert_alpha()
            TRACK = pygame.transform.scale(TRACK,(900,900))
            TRACK_COPY = TRACK.copy()
            Spawn = 190, 600
            resett = True
        if keys_pressed[pygame.K_4]:
            TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track4.png'))).convert_alpha()
            TRACK = pygame.transform.scale(TRACK,(900,900))
            TRACK_COPY = TRACK.copy()
            Spawn = 230, 350
            resett = True
        moved = False
        if keys_pressed[pygame.K_w]:
            moved = True
            pcar.forward()
        if keys_pressed[pygame.K_a]:
            pcar.angle += 5
        if keys_pressed[pygame.K_d]:
            pcar.angle -= 5 
             
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
            if ploss:
                car.Spawn = Spawn
                car.crashed = True
                
        pcar.draw(SCREEN)
        
        if running_cars == 0:
            G_Data.append(GENERATION)
            T_Data.append(laptime)
            
            return
        laptime = round((time.time() - lasttime)*(fps/24), 2)
        if resett == True:
            fps = 1
            text = FONT.render(str(countdown), 1, (255,0,0))
            SCREEN.blit(text, (400, 400))
            countdown -=1
        if countdown == 0:
            resett = False
            fps = 24
            countdown = 3
        if not moved:
            pcar.momentum()   
        pygame.display.update()
        CLOCK.tick(fps)
        


def load_ai(filename):
    return  joblib.load((os.fspath(Path(__file__).resolve().parent / filename)))


# if __name__ == "__main__":
pygame.init()
pygame.display.set_caption("YOU VS AI")
WIN = 900, 900
SCREEN = pygame.display.set_mode(WIN)
countdown = 3

Spawn = 190, 600
Speed = 10
Turn = 28

CAR_SIZE = 25,50
Border = [(67, 153, 162, 255),(66, 154, 162, 255),(37, 156, 163, 255),(120, 220, 82, 255),(76, 155, 162, 255),(136, 242, 255, 255),(65, 152, 162, 255),(154, 239, 254, 255),(136, 219, 91, 255),(137, 219, 92, 255),(67, 153, 162, 255),(23, 57, 170, 255)]
TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track3.png'))).convert_alpha()
TRACK = pygame.transform.scale(TRACK,(900,900))
TRACK_COPY = TRACK.copy()
FONT = pygame.font.SysFont("Grand9K Pixel", 100)

CARp = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "car{}.png".format(randint(1,9)))))
CARp = pygame.transform.rotate(CARp,180)
CARp = pygame.transform.scale(CARp,(CAR_SIZE[0]-3,CAR_SIZE[1]-6))

rot = 0
pcar = PlayerCar(Speed)
CLOCK = pygame.time.Clock()
GENERATION = 0

lines = False
fps = 30

G_Data =[]
T_Data = []


# population = load_ai(str(os.fspath(Path(__file__).resolve().parent / "best.pickle")))
population = load_ai("best.pkl")
while True:
    ploss = False
    population.run(run, 1)
    if ploss == False:
        text = FONT.render("You Won", 1, (255,255,255))
        SCREEN.blit(text, (200, 400))
        CARp = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "car{}.png".format(randint(1,9)))))
        CARp = pygame.transform.rotate(CARp,180)
        CARp = pygame.transform.scale(CARp,(CAR_SIZE[0]-3,CAR_SIZE[1]-6))
        pygame.display.update()
        time.sleep(2)
        pcar.x = Spawn[0]
        pcar.y = Spawn[1]
        
    
    

