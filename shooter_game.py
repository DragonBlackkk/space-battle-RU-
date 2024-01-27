#Создай собственный Шутер!

from pygame import *
from random import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


    
class Player(GameSprite):
    def update(self):
        keys =key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_witdh - 80:
            self.rect.x += self.speed
        

    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
          

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            self.rect.x = randint(80,win_witdh-80)
            self.rect.y = 0
            lost = lost +1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        

#|||||||||||||||||||Настройка экрана|||||||||||||||||||||||||||||||||||||||#                  
image_bag = "galaxy.jpg"                                                   #
win_witdh = 700                                                            #
win_hight = 500                                                            #
window = display.set_mode((win_witdh, win_hight))                          #
display.set_caption('Space chaos')                                         #
background = transform.scale(image.load(image_bag),(win_witdh,win_hight))
winbackg = transform.scale(image.load('win.jpg'),(win_witdh,win_hight))
losebackg = transform.scale(image.load('lose.jpg'),(win_witdh,win_hight))  #
#|||||||||||||||||||Создание Фоновой музыки||||||||||||||||||||||||||||||||#
mixer.init()                                                               #
mixer.music.load("spaceost.mp3")                                              #
mixer.music.play()
#mixer.music.load("fire.ogg")
firesound = mixer.Sound('fire.ogg')                                                         #
#|||||||||||||||||||Cоздаём спрайты||||||||||||||||||||||||||||||||||||||||#
x = 50
y = 500
image_hero = 'rocket.png'                                                  #
ship = Player(image_hero, 5, win_hight - 100, 80, 100, 10)                 #
image_enemy = 'ufo.png'
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(image_enemy, randint(80,win_witdh-80),-40,80,50, randint(1,3))
    monsters.add(monster)
bullets = sprite.Group() 

#|||||||||||||||||||Задаём основные базы|||||||||||||||||||||||||||||||||||#
finish = False                                       #
run = True
finish = False                                           #
clock = time.Clock()                                 #
lost = 0                                             #
score = 0
maxlost = 3                                            # 
font.init()
font1 = font.Font(None,36)    
#|||||||||||||||||||Игровой цикл|||||||||||||||||||||#                                    
while run:                                           #
    for e in event.get():                            #
        if e.type == QUIT:                           #
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                firesound.play() 
                ship.fire()
    if not finish:                                                 
        window.blit(background, (0,0))
        text_win = font1.render('Счет: '+str(score),1,(255,255,255))                   #
        window.blit(text_win,(10,20))
        text_lost = font1.render('Пропущено: '+str(lost),1,(255,255,255))     
        window.blit(text_lost,(10,50))
        ship.update()
        monsters.update()
        bullets.update()                                 #
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        colides = sprite.groupcollide(monsters,bullets, True, True)
        for c in colides:
            score += 1
            monster = Enemy(image_enemy, randint(80,win_witdh-80),-40,80,50, randint(1,3))
            monsters.add(monster)    
        if score > 10:
            finish = True
            window.blit(winbackg,(0,0))
        if sprite.spritecollide(ship,monsters,False ) or lost > maxlost:
            finish = True
            window.blit(losebackg,(0,0))
        display.update()                                 
                               
    clock.tick(60)                                   #
#||||||||||||||||||||||||||||||||||||||||||||||||||||#
                                           