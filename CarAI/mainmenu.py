import pygame 
import sys 
from pathlib import Path
import os

pygame.init() 
pygame.display.set_caption("Self Driving Car")
res = (900,900) 

WIN = pygame.display.set_mode(res) 
   
color = (255,255,255) 
color_light = (170,170,170,50) 
  
color_dark = (150,150,150,50) 
  

width = WIN.get_width() 

height = WIN.get_height() 
  
smallfont = pygame.font.SysFont("Grand9K Pixel", 40) 
  
text = smallfont.render('Train Model' , True , color) 
text3 = smallfont.render('You VS AI' , True , color) 
text2 = smallfont.render('Test Drive' , True , color) 
  
while True: 
      
    for ev in pygame.event.get(): 
          
        if ev.type == pygame.QUIT: 
            pygame.quit() 
    
        if ev.type == pygame.MOUSEBUTTONDOWN: 

            if 300 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+60: 
                import train
            if 300 <= mouse[0] <= width/2+140 and height/2+100 <= mouse[1] <= height/2+160: 
                import test
            if 300 <= mouse[0] <= width/2+140 and height/2+200 <= mouse[1] <= height/2+260: 
                import race
                  
    bg = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'blur.jpg'))).convert_alpha()
    bg = pygame.transform.scale(bg,(900,900))
    WIN.blit(bg,(0,0))
    ico = pygame.image.load(str(os.fspath(Path(__file__).resolve().parent / 'icon.png'))).convert_alpha()
    ico = pygame.transform.scale(ico,(400,400))
    WIN.blit(ico,(260,50))
    mouse = pygame.mouse.get_pos() 
      
      
          
    if 300 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+60: 
        pygame.draw.rect(WIN,color_light,[width/2-140,height/2,300,60]) 
          
    else: 
        pygame.draw.rect(WIN,color_dark,[width/2-140,height/2,300,60]) 
        
    if 300 <= mouse[0] <= width/2+140 and height/2+100 <= mouse[1] <= height/2+160: 
        pygame.draw.rect(WIN,color_light,[width/2-140,height/2+100,300,60])
    else: 
        pygame.draw.rect(WIN,color_dark,[width/2-140,height/2+100,300,60])      
    
        
    if 300 <= mouse[0] <= width/2+140 and height/2+200 <= mouse[1] <= height/2+260: 
        pygame.draw.rect(WIN,color_light,[width/2-140,height/2+200,300,60]) 
          
    else: 
        pygame.draw.rect(WIN,color_dark,[width/2-140,height/2+200,300,60]) 
      
    WIN.blit(text , (width/2-110,height/2)) 
    WIN.blit(text2 , (width/2-110,height/2+100)) 
    WIN.blit(text3 , (width/2-100,height/2+200)) 

    pygame.display.update() 