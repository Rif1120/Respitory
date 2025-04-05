#Create your own shooter

from pygame import *
from random import randint
from time import time as timer
class GameSprites(sprite.Sprite):
    def __init__(self, player_image,player_x, player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprites):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0

class Enemy(GameSprites):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >  win_height:
            self.rect.x  = randint(80,win_width-80)
            self.rect.y = 0
            self.speed = randint(1,2)
            lost +=1

class Enemy2(GameSprites):
    def update(self):
        global lost
        self.rect.y += self.speed
        self.rect.x += randint(-10,10)
        if self.rect.y >  win_height:
            self.rect.x  = randint(80,win_width-80)
            self.rect.y = 0
            self.speed = randint(1,1)
            lost +=1

class Enemy3(GameSprites):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >  win_height:
            self.rect.x  = randint(80,win_width-80)
            self.rect.y = 0
            self.speed = randint(1,2)

class Bullet(GameSprites):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width,win_height))

from pygame import *

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
kick = mixer.Sound("fire.ogg")

init()
font.init
fontgame= font.Font(None,80)
win = fontgame.render('YOU WIN!', True, (180, 0, 0))
lose = fontgame.render('YOU LOSE!', True, (255, 255, 255))
font2 = font.Font(None, 36)
restarttext = fontgame.render ('Game restart!', True, (180,0,0))
restart=False

win_width = 700
win_height = 500

#create game window
win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("Shooter game")

#set scene background
background  = transform.scale(image.load('galaxy.jpg'), (700, 500))
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_enemy2 = "ufo2.png"
img_bullet = "bullet.png"
img_asteroids = 'asteroid.png'

score = 0
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        

player1 = Player(img_hero,5,win_height -100,80,100,10)

monsters = sprite.Group()
monsters2 = sprite.Group()
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width-80), 40, 80, 90, randint(1,2))
    monsters.add(monster)
    monster2 = Enemy2(img_enemy2, randint(80, win_width-80), 40, 80, 90, randint(1,3))
    monsters2.add(monster)
    asteroid = Enemy3(img_asteroids, randint(80, win_width-80), 40, 80, 90, randint(1,1))
    asteroids.add(asteroid)

bullets = sprite.Group()


#handle "click on the "Close the window"" event 
run = True
clock = time.Clock()
FPS = 60
score = 0
finish = False
goal = 10
max_lost = 3
win = fontgame.render('YOU WIN!', True, (255, 255, 255))
lose = fontgame.render('YOU LOSE!', True, (180, 0, 0))


rel_time = False
num_fire = 0
max_fire = 5
finish = False

life = 3
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < max_fire and rel_time == False:
                    num_fire +=1
                    kick.play()
                    player1.fire()

                if num_fire >= max_fire and rel_time == False:
                    last_time = timer()
                    rel_time = True

            if e.key == K_RETURN:
                restart = True

    if not finish:


        window.blit(background,(0,0))
        player1.update()
        player1.reset()
        asteroids.update()
        asteroids.draw(window)
        monsters.update()
        monsters.draw(window)
        monsters2.update()
        monsters2.draw(window)
        bullets.update()
        bullets.draw(window)


        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1.5:
                reload = fontgame.render('Wait... reload...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
                

        collides = sprite.groupcollide(asteroids,bullets, False, True)

        collides = sprite.groupcollide(monsters,bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40,80,50, randint(1,2))
            monsters.add(monster)

        collides = sprite.groupcollide(monsters2,bullets, True, True)
        for collide in collides:
            score += 1
            monster2 = Enemy(img_enemy2, randint(80, win_width-80), -40,80,50, randint(1,3))
            monsters2.add(monster2)

        if sprite.spritecollide(player1, monsters, True):
            life += -1

        if sprite.spritecollide(player1, monsters2, True):
            life += -1

        if sprite.spritecollide(player1, asteroids, True):
            life += -1

        if score >= goal:
            finish = True
            window.blit(win,(200,200))          
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))  
            
        if life == 3:
            life_color = (0,150,0)            
        if life == 2:
            life_color = (150,150,0)            
        if life == 1:
            life_color = (150,0,0)            
        text_life = fontgame.render(str(life),1,life_color)
        window.blit(text_life,(650,10)) 
        text = font2.render("Socre: "+str(score),1, (255,255,255))
        window.blit(text,(10,20))

        text = font2.render("Missed: "+str(lost),1, (255,255,255))
        window.blit(text,(10,50))
        display.update()
    elif restart:
        finish = False
        restart = False
        score = 0
        lost = 0
        life = 3
        rel_time = False
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()            
        for m in monsters2:
            m.kill()   
        player = Player(img_hero,5,win_height-100,80,100,10)                             
        for i in range(1, 3):
            monster = Enemy(img_enemy, randint(80, win_width-80), -40,80,50, randint(1,2))
            monsters.add(monster)
        for i in range(1, 3):
            monster2 = Enemy2(img_enemy2, randint(80, win_width-80), -40,80,50, randint(1,3))
            monsters2.add(monster2)
        for i in range(1, 3):
            asteroid = Enemy3(img_enemy2, randint(80, win_width-80), -40,80,50, randint(1,3))
            asteroids.add(asteroid)        
        window.blit(background,(0,0))
        window.blit(restarttext,(200,200))
        display.update()
        time.delay(1000)
        
    display.update()
    clock.tick(FPS)

    time.delay(50)

#clock.tick(FPS)