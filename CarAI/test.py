import pygame,math,os
from pathlib import Path
from random import randint

WIDTH,HEIGHT =900,900
SCALEW,SCALEH = 25,50
Border = [(67, 153, 162, 255),(66, 154, 162, 255),(37, 156, 163, 255),(76, 155, 162, 255),(136, 242, 255, 255),(65, 152, 162, 255),(154, 239, 254, 255),(136, 219, 91, 255),(137, 219, 92, 255),(67, 153, 162, 255),(23, 57, 170, 255)]
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Drive")

FPS = 30
CAR = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "car{}.png".format(randint(1,9)))))
CAR = pygame.transform.rotate(CAR,180)
CAR = pygame.transform.scale(CAR,(SCALEW,SCALEH))

bg = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "track1.png")))
bg = pygame.transform.rotate(bg,0)
bg = pygame.transform.scale(bg,(900,900))

def rotate_image(win,image,top_left,angle):
        rotated_image = pygame.transform.rotate(image,angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft= top_left).center)
        win.blit(rotated_image,new_rect.topleft)

class PlayerCar:
    
    def __init__(self,max_vel):
        self.img = CAR
        self.max_vel = max_vel
        self.vel = 0
        self.angle = 180
        self.x,self.y = (58,200)
        self.acc = 0.2
        
    def draw(self,win):
        rotate_image(win,self.img,(self.x,self.y ),self.angle)
        

    def forward(self):
        self.vel = min(self.vel + self.acc,self.max_vel)
        if bg.get_at((int(self.x), int(self.y))) in Border:
            self.vel = -(self.vel)
        self.move()
        
    
        
    def move(self):
        self.img = CAR
        radians = math.radians(self.angle)
        
        vert = math.cos(radians) * self.vel
        horz = math.sin(radians) * self.vel
        
        self.y -= vert
        self.x -= horz
    def momentum(self):
        self.vel = max(self.vel - self.acc / 2,0)
        
        self.move()
        


    
def draw_window(car):
    WIN.blit(bg, (0,0))
    
    car.draw(WIN)
    pygame.display.update()


line_start = None
car = PlayerCar(10)
clock = pygame.time.Clock()
rot = 0
run = True

while run:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
    
    draw_window(car)    
    
    keys_pressed = pygame.key.get_pressed()
    moved = False
    if keys_pressed[pygame.K_w]:
        moved = True
        car.forward()
    if keys_pressed[pygame.K_a]:
        car.angle += 5
    if keys_pressed[pygame.K_d]:
        car.angle -= 5
        
    if keys_pressed[pygame.K_1]:
        bg = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "track1.png")))
        bg = pygame.transform.rotate(bg,0)
        bg = pygame.transform.scale(bg,(900,900))
    if keys_pressed[pygame.K_2]:
        bg = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "track2.png")))
        bg = pygame.transform.rotate(bg,0)
        bg = pygame.transform.scale(bg,(900,900))
    if keys_pressed[pygame.K_3]:
        TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track3.png')))
        bg = pygame.transform.rotate(bg,0)
        TRACK = pygame.transform.scale(TRACK,(900,900))     
    if keys_pressed[pygame.K_4]:
        TRACK = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'track4.png')))
        bg = pygame.transform.rotate(bg,0)
        TRACK = pygame.transform.scale(TRACK,(900,900))
            
    if keys_pressed[pygame.K_r]:
        CAR = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / "car{}.png".format(randint(1,9)))))
        CAR = pygame.transform.rotate(CAR,180)
        CAR = pygame.transform.scale(CAR,(SCALEW,SCALEH))
        car.x,car.y = (58,200)
    
    if not moved:
            car.momentum()             
    
            
pygame.quit()


