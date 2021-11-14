from pygame import *
from random import randint
from time import time as timer

font.init()
font = font.SysFont("Arial", 36)

score = 0
lost = 0
goal = 30
life = 30
max_lost = 30 

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 1855:
            self.rect.x += self.speed
    def fire(self):
       bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,15, 20, 50)
       bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 1050:
            self.rect.y += 2
        
        else:
            
            self.rect.y = -80
            self.rect.x = randint(40, 1920)
            lost = lost + 1

class Asteroid_cl(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 1050:
            self.rect.y += 2
        
        else:
            
            self.rect.y = -80
            self.rect.x = randint(40, 1920)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            

player = Player("rocket.png", 960, 900, 100, 150, 15)

monsters = sprite.Group()
for i in range(1, 15):
    monster = Enemy("ufo.png", randint(40, 1880), randint(-150, -40), 100, 80, 8)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 10):
    asteroid = Asteroid_cl("asteroid.png", randint(40, 1880), randint(-100, -25), 100, 100, 8)
    asteroids.add(asteroid)

bullets = sprite.Group()


window = display.set_mode((1920,1050))
display.set_caption("Ship vs UFO")
background = transform.scale(image.load("galaxy.jpg"), (1920,1050))

clock = time.Clock()
FPS = 60
game = True
finish = False

num_fire = 0
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                   num_fire = num_fire + 1
                   player.fire()
                   

                if num_fire  >= 10 and rel_time == False :
                    last_time = timer() 
                    rel_time = True 

    if not finish:


        window.blit(background,(0,0))

        text = font.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 100))

        text_lose = font.render("Пропущено: " + str(lost), 1 ,(255,255,255))
        window.blit(text_lose, (10, 50))

        text_life = font.render("Жизнь: " + str(life), 1 ,(255, 255, 255))
        window.blit(text_life, (10, 150)) 

        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font.render("Reload",1,(150,0,0))
                window.blit(reload,(960,525))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(40, 1880), randint(-150, -40), 100, 80, 8)
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            lose = transform.scale(image.load("game-over.jpg"), (1920,1050))
            window.blit(lose, (0,0))

        if score >= goal:
            finish = True
            win = transform.scale(image.load("thumb.jpg"), (1920,1050))
            window.blit(win, (0,0))

        display.update()
        
    clock.tick(FPS)
