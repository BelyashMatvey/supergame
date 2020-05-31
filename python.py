import pygame
import random
import time
import sys


WIDTH = 600
HEIGHT = 400
FPS = 60

open('output.txt', 'w').close()
f=open("output.txt","r+")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 150, 100)


pygame.init()
pygame.mixer.init()
sounds=[]
sounds.append(pygame.mixer.Sound('expl3.wav'))
sounds.append(pygame.mixer.Sound('expl6.wav'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
bullets = pygame.sprite.Group()
mobs=pygame.sprite.Group()
cels=pygame.sprite.Group()


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x =-30
        self.rect.y = 100

    def update(self):
        if self.rect.x >= WIDTH + 30:
            self.rect.x = 0 -30
        else:
            self.rect.x += 2


class Cel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x =-17
        self.rect.y = 137

    def update(self):
        if self.rect.x >= WIDTH + 30:
            self.rect.x = 0 -30
        else:
            self.rect.x += 2
        return


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = HEIGHT // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(Cel):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.a=self.rect.y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 20:
            self.kill()
        if self.rect.y==140:
            if self.rect.x>c.rect.x:
                f.write(str(abs(self.rect.x-c.rect.x)))
                f.write(" +")
                f.write("\n")
            else:
                f.write(str(abs(self.rect.x - c.rect.x)))
                f.write(" -")
                f.write("\n")


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
all_sprites.add(player)
c=Cel()
b=Bullet(player.rect.centerx,player.rect.top)
cels.add(c)
all_sprites.add(c)
m = Mob()
mobs.add(m)
all_sprites.add(m)


running = True
while running:


    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    hits1=pygame.sprite.groupcollide(cels,bullets,True,True)
    for hit in hits1:
        c.kill()
        m.kill()
        c = Cel()
        m=Mob()
        kil = f.readlines()
        kil = kil[:-1]
        f.write("0")
        f.write("\n")
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        sounds[1].play()
        sounds[1].play()
        all_sprites.add(m)
        mobs.add(m)
        all_sprites.add(c)
        cels.add(c)
    all_sprites.update()
    pygame.display.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        c.kill()
        c=Cel()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        sounds[0].play()
        all_sprites.add(m)
        all_sprites.add(c)
        cels.add(c)
        mobs.add(m)
    screen.fill(BLACK)
    all_sprites.draw(screen)
f.close()