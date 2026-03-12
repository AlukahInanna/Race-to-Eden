

import pygame


class StatusBar:

    def __init__(self,x,y,width,height,color):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color
        self.display_value = 1.0

    def draw(self,screen,current,max_value):

        target = current/max_value

        # smooth animation
        self.display_value += (target - self.display_value)*0.1

        pygame.draw.rect(screen,(40,40,40),
                         (self.x,self.y,self.width,self.height))

        pygame.draw.rect(screen,self.color,
                         (self.x,self.y,
                          self.width*self.display_value,self.height))


hp_bar = StatusBar(20,20,200,20,(255,60,60))
st_bar = StatusBar(20,50,200,20,(60,255,60))
mp_bar = StatusBar(20,80,200,20,(60,60,255))

__all__ = ["StatusBar", "hp_bar", "st_bar", "mp_bar"]

