import sys
import pygame
import os
filepath = os.path.dirname(__file__)
enpic = os.path.join(filepath, 'enemy.png')
deadpic = os.path.join(filepath, 'dead.png')
laspic = os.path.join('laser.png')
sspic = os.path.join('ship.png')
els = os.path.join('enemylaser.png')
screen = pygame.display.set_mode((800, 600))
x = os.path.join("OVERSCREEN.png")
OVERSCREEN = pygame.image.load(x)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
y = os.path.join("GGSCREEN.png")
GGSCREEN = pygame.image.load(y)


class Bunker:
    WIDTH = 100
    HEIGHT = 30
    HP = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, background):
        pygame.draw.rect(background, COLOR_GREEN, pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT))
        pygame.display.flip()


class Enemy:
    SPEED = 50
    WIDTH = 50
    HEIGHT = 50
    RC = 0
    en = pygame.image.load(enpic)
    dead = pygame.image.load(deadpic)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, background):
        if SpaceInvaders.lost == 0:
            background.blit(self.en, (self.x, self.y))
            pygame.display.flip()


class Enemylaser:
    ELAS = pygame.image.load(els)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, background):
        background.blit(self.ELAS, (self.x, self.y, 4, 8))
        self.y += 20
        if self.y > 800:
            SpaceInvaders.elasers.remove(self)
        pygame.display.flip()
    def checkHit(self, enemy):
        laser_rect = pygame.Rect(self.x, self.y, 4, 8)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.WIDTH, enemy.HEIGHT)

        return laser_rect.colliderect(enemy_rect)

class Laser:
    LAS = pygame.image.load(laspic)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, background):
        background.blit(self.LAS, (self.x, self.y, 4, 8))
        self.y -= 20
        if self.y < 0:
            SpaceInvaders.lasers.remove(self)
        pygame.display.flip()

    def checkHit(self, enemy):
        laser_rect = pygame.Rect(self.x, self.y, 4, 8)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.WIDTH, enemy.HEIGHT)

        return laser_rect.colliderect(enemy_rect)



class Player:
    SPEED = 5
    WIDTH = 50
    HEIGHT = 48
    HP = 100000

    SS = pygame.image.load(sspic)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_right(self):
        self.x += self.SPEED

        if self.x + self.WIDTH > SpaceInvaders.WIDTH:
            self.x -= self.SPEED

    def move_left(self):
        self.x -= self.SPEED

        if self.x < 0:
            self.x = 0

    def render(self, background):
        background.blit(self.SS, (self.x, self.y))
        pygame.display.flip()






class SpaceInvaders():
    aliencounter = 40
    aliens = []
    FPS = 60
    WIDTH = 800
    HEIGHT = 600
    RC = 0
    lasers = []
    bunkers = []
    elasers = []
    MAX = 0
    MIN = 800
    score = 0
    highscore = 0
    lost = 0
    time = 0
    k = 0
    def __init__(self):

        self.ship = Player(375, 520)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = None
        for i in range(200, SpaceInvaders.WIDTH - 200, 50):
            for j in range(50, int(SpaceInvaders.HEIGHT / 2), 50):
                SpaceInvaders.aliens.append(Enemy(i, j))

    def start(self):

        self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.background = self.background.convert()
        self.background.fill(COLOR_BLACK)
        for i in range(100, self.WIDTH-100, 250):
            self.bunkers.append(Bunker(i, 460))
        self.screen.blit(self.background, (0, 0))

        pygame.display.flip()
        while True:
            self.time += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.lasers.append(Laser(self.ship.x + self.ship.WIDTH/2 , self.ship.y))
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a]:
                self.ship.move_left()
            if keys_pressed[pygame.K_d]:
                self.ship.move_right()
            for alien in self.aliens:
                MAX = 0
                for j in self.aliens:
                    if j.x == alien.x:
                        if j.y >= MAX:
                            MAX = j.y
                if alien.y == MAX:
                    if self.time % 60 ==0:
                        self.elasers.append(Enemylaser(alien.x + alien.WIDTH/2, alien.y))

            pygame.font.init()
            font = pygame.font.SysFont('Arial', 30)
            textsurface = font.render("Score: " + str(self.score), False, (255, 255, 255))
            screen.blit(textsurface, (10, 20))
            pygame.display.flip()
            pygame.font.init()
            font = pygame.font.SysFont('Arial', 30)
            textsurface = font.render("Highscore: " + str(self.highscore), False, (255, 255, 255))
            screen.blit(textsurface, (10, 50))
            pygame.display.flip()
            pygame.font.init()
            font = pygame.font.SysFont('Arial', 30)
            textsurface = font.render("Lives: " + str(self.ship.HP), False, (255, 255, 255))
            screen.blit(textsurface, (700, 20))
            pygame.display.flip()

            self.update()

            self.render()
            if(self.lost == 1):
                if self.k == 1:
                    screen.blit(OVERSCREEN, (0,0))
                    self.aliens.clear()
                    self.bunkers.clear()
                    self.ship = Player(1000, 1000)
                if self.k == 2:
                    screen.blit(GGSCREEN, (0,0))
                    self.aliens.clear()
                    self.bunkers.clear()
                    self.ship = Player(1000, 1000)
                if keys_pressed[pygame.K_SPACE]:
                    self.aliencounter = 40
                    self.aliens.clear()
                    self.FPS = 60
                    self.WIDTH = 800
                    self.HEIGHT = 600
                    self.RC = 0
                    self.lasers.clear()
                    self.bunkers.clear()
                    self.elasers.clear()
                    self.MAX = 0
                    self.MIN = 800
                    self.score = 0
                    self.lost = 0
                    self.__init__()
                    self.ship.HP = 3
                    self.start()

    def update(self):
        self.clock.tick(SpaceInvaders.FPS)
        for alien in self.aliens:
            for laser in self.lasers:
                if laser.checkHit(alien):
                        self.lasers.remove(laser)
                        SpaceInvaders.aliens.remove(alien)
                        self.aliencounter -= 1
                        self.score += 10
                        if self.score > self.highscore:
                            self.highscore = self.score

        for laser in self.lasers:
            for bunker in self.bunkers:
                if laser.checkHit(bunker):
                    SpaceInvaders.lasers.remove(laser)
                    bunker.HP -= 1
                    if bunker.HP == 0:
                        SpaceInvaders.bunkers.remove(bunker)
        for elaser in self.elasers:
            for bunker in self.bunkers:
                if elaser.checkHit(bunker):
                    SpaceInvaders.elasers.remove(elaser)
                    bunker.HP -= 1
                    if bunker.HP == 0:
                        SpaceInvaders.bunkers.remove(bunker)
        for elaser in self.elasers:
            if elaser.checkHit(self.ship):
                SpaceInvaders.elasers.remove(elaser)
                self.ship.HP -= 1


    def render(self):
        self.MIN = 800
        self.MAX = 0
        self.background.fill(COLOR_BLACK)
        self.ship.render(self.background)
        for alien in self.aliens:
            if alien.y >= 500:
                self.lost = 1
                self.k = 1
                break
        if self.ship.HP == 0:
            self.lost = 1
            self.k = 1
        if self.aliencounter == 0:
            self.lost = 1
            self.k = 2
        if self.aliens.__len__() != 0:
            for alien in self.aliens:
                if alien.x >= self.MAX:
                    self.MAX = alien.x
                if alien.x <= self.MIN:
                    self.MIN = alien.x

            if self.MAX + alien.SPEED > SpaceInvaders.WIDTH - alien.WIDTH and self.time % 60 == 0:
                self.RC += 1
                for alien in SpaceInvaders.aliens:
                    alien.y = alien.y + alien.HEIGHT


            if self.MIN <= 0 and self.time % 60 == 0:
                self.RC += 1
                for alien in SpaceInvaders.aliens:
                    alien.y = alien.y + alien.HEIGHT

            for alien in SpaceInvaders.aliens:
                if self.RC % 2 == 0 and self.time % 60 == 0:
                    alien.x += alien.SPEED
                if self.RC % 2 == 1 and self.time % 60 == 0:
                    alien.x -= alien.SPEED

        for alien in self.aliens:
            alien.render(self.background)
        for bunker in self.bunkers:
            bunker.render(self.background)
        for laser in self.lasers:
            laser.render(self.background)
        for elaser in self.elasers:
            elaser.render(self.background)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()



def main():
    # Initialize imported pygame modules
    pygame.init()

    # Set the window's caption
    pygame.display.set_caption("Space Invaders")

    # Create new game instance and start the game
    game = SpaceInvaders()
    game.start()


if __name__ == '__main__':
    main()