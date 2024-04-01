import math

import pygame as pygame
from pygame import Vector2, Color, mixer

width = 700
height = 700

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
screen.fill((53, 53, 88), (0, 0, width, height))
pygame.draw.circle(screen, (255,0,0), (width/2, height/2), width/2, 5)
mixer.init()
sound = mixer.Sound("jump.wav")

class Ball:
    def __init__(self):
        self.position = Vector2(width/2, height/2)
        self.color = (0,0,0)
        self.gravity = Vector2(0,0.32)
        self.velocity = Vector2(-7,-7)
        self.prevPos = Vector2(self.position.x,self.position.y)
        self.radius = 30

    def update(self):
        self.prevPos = Vector2(self.position.x,self.position.y)

        # movement
        self.velocity += self.gravity
        self.position += self.velocity

        dirToCenter = Vector2(self.position.x - width/2,self.position.y - height/2)
        if self.isCollide():
            pygame.mixer.Sound.play(sound)
            self.radius += 1
            self.position = Vector2(self.prevPos.x,self.prevPos.y)
            v = math.sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y)
            angleToCollisionPoint = math.atan2(-dirToCenter.y,dirToCenter.x)
            oldAngle = math.atan2(-self.velocity.y,self.velocity.x)
            newAngle = 2 * angleToCollisionPoint - oldAngle
            self.velocity = Vector2(-v * math.cos(newAngle),v * math.sin(newAngle))

    def isCollide(self):
        if self.distance(self.position.x,self.position.y,width/2,height/2) > width/2 - self.radius:
            return True
        return False

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)

    def draw(self):
        pygame.draw.circle(screen,self.color,(self.position.x,self.position.y),self.radius)

ball = Ball()
color = Color(211,12,211)
h = color.hsla[0]
s = color.hsla[1]
l = color.hsla[2]
colorDir = 1

while True:
    clock.tick(60 )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    ball.update()
    pygame.draw.circle(screen, (255, 0, 0), (width / 2, height / 2), width / 2, 5)

    color.hsla = (h, s, l, 1)
    h += 1 * colorDir
    if h >= 360:
        colorDir = -1
    elif h <= 0:
        colorDir = 1

    pygame.draw.circle(screen,
                       (color.r, color.g, color.b),
                       (ball.position.x, ball.position.y),
                       ball.radius + 2)

    ball.draw()

    pygame.display.flip()
