import pygame
import random
import math
import numpy as np
from numpy import linalg as LA

# Entrada do usuário para o número de bolas
num_balls = int(input("Digite o número de bolas: "))

# Definindo as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definindo as dimensões da tela
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 650

#Coeficiente de restituição	
cr=1

# Definindo a classe da bola
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(10, 60) #Define o tamanho das bolas
        self.color = color
        self.speed_x = random.randint(-1, 1)
        self.speed_y = random.randint(-1, 1)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_collision(self, other_balls):
        for ball in other_balls:
            if ball != self:
              distance = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
          
              if distance < self.radius + ball.radius:
              
                fatorDeMudanca = 0.5*(distance - self.radius - ball.radius)    
                self.x -= fatorDeMudanca * (self.x - ball.x)/distance    
                self.y -= fatorDeMudanca * (self.y - ball.y)/distance    
                ball.x += fatorDeMudanca * (self.x - ball.x)/distance   
                ball.y += fatorDeMudanca * (self.y - ball.y)/distance
                  
                vetornormal=np.array([ball.x-self.x,ball.y-self.y])
                normanormal=LA.norm(vetornormal)
                vetorunitarionormal=np.divide(vetornormal,normanormal)
                vetorunitariotangencial=np.array([-vetorunitarionormal[1],vetorunitarionormal[0]])
                velocidade1=np.array([self.speed_x,self.speed_y])
                velocidade2=np.array([ball.speed_x,ball.speed_y])

                v1normal=np.dot(vetorunitarionormal,velocidade1)
                v2normal=np.dot(vetorunitarionormal,velocidade2)
                v1tangencial=np.dot(vetorunitariotangencial,velocidade1)
                v2tangencial=np.dot(vetorunitariotangencial,velocidade2)

                        
                vcentromassa=np.divide(np.add(self.radius*v1normal,ball.radius*v2normal),self.radius+ball.radius)

                v1normal=np.subtract((1+cr)*vcentromassa,cr*v1normal)
                v2normal=np.subtract((1+cr)*vcentromassa,cr*v2normal)
  
                v1normal=np.dot(vetorunitarionormal,v1normal)
                v2normal=np.dot(vetorunitarionormal,v2normal)
                v1tangencial=np.dot(vetorunitariotangencial,v1tangencial)
                v2tangencial=np.dot(vetorunitariotangencial,v2tangencial)
  
                v1final=np.add(v1tangencial,v1normal)
                v2final=np.add(v2tangencial,v2normal)
                self.speed_x=v1final[0]
                ball.speed_x=v2final[0]
                self.speed_y=v1final[1]
                ball.speed_y=v2final[1]
                    
              

        if self.x + self.radius > SCREEN_WIDTH or self.x - self.radius < 0:
            self.speed_x = -cr*self.speed_x
        if self.y + self.radius > SCREEN_HEIGHT or self.y - self.radius < 0:
            self.speed_y = -cr*self.speed_y

# Inicialização do pygame
pygame.init()

# Inicialização da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bolas Colidindo")



# Lista de bolas
balls = []
for _ in range(num_balls):
    overlap = True
    while overlap:
        new_ball = Ball(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        overlap = False
        for ball in balls:
            distance = math.sqrt((new_ball.x - ball.x) ** 2 + (new_ball.y - ball.y) ** 2)
            if distance < new_ball.radius + ball.radius + 10:
                overlap = True
                break
    balls.append(new_ball)

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for ball in balls:
        ball.move()
        ball.check_collision(balls)
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(144)

pygame.quit()