#Create your own shooter
import pygame as pyg
import random as rand

res = width,height = 700,500

pyg.init()
pyg.font.init()

window = pyg.display.set_mode(res)
pyg.display.set_caption("Space Shooters")

point = 0
miss = 0
maxpoint = 50
maxmiss = 3

pyg.mixer.music.load("space.ogg")
pyg.mixer.music.play()


class GameSprite(pyg.sprite.Sprite):
    def __init__(self,playerImage,speed,coordinates,dimension=(65,65)):
        super().__init__()
        self.image = pyg.transform.scale(
            pyg.image.load(playerImage),dimension
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
class Player(GameSprite):
    def move(self):
        keys = pyg.key.get_pressed()
        if keys[pyg.K_LEFT] and self.rect.x >= self.speed:
            self.rect.x -= self.speed
        if keys[pyg.K_RIGHT] and self.rect.x <= width-self.speed:
            self.rect.x += self.speed
        window.blit(self.image,(self.rect.x,self.rect.y))
    def shoot(self):
        bullet = Bullet("bullet.png",16,(self.rect.x+20,self.rect.y),(10,20))
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y >= height:
            self.rect.x,self.rect.y = rand.randint(1,9)*width//10,10
            self.speed = rand.randint(1,3)
            miss += 1
class Bullet(GameSprite):
    def update(self):
        global point
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            self.kill()


font = pyg.font.Font(None,30)
lose = pyg.font.Font(None,90).render("You Lose",1,(255,0,0))
win = pyg.font.Font(None,90).render("You Win",1,(0,255,0))
restart = font.render("Click R To Restart",1,(255,255,255))


background = pyg.transform.scale(
    pyg.image.load("galaxy.jpg"),res
)
player = Player("rocket.png",7,(200,380),(50,100))
enemies = pyg.sprite.Group()
for i in range(1,6):
    enemy = Enemy("ufo.png",rand.randint(1,2),(rand.randint(1,9)*width//10,10),(70,35))
    enemies.add(enemy)

bullets = pyg.sprite.Group()

def reset():
    global point,miss,rerun,enemies
    point = 0
    miss = 0
    rerun = False
    for enemy in enemies:
        enemy.kill()
    for bullet in bullets:
        bullet.kill()
    for i in range(1,6):
        enemy = Enemy("ufo.png",rand.randint(1,2),(rand.randint(1,9)*width//10,10),(70,35))
        enemies.add(enemy)


rerun = False
fps = pyg.time.Clock()
frame = 30
while True:
    for e in pyg.event.get():
        if e.type == pyg.QUIT:
            pyg.quit()
            quit()
        if e.type == pyg.KEYDOWN:
            if e.key == pyg.K_SPACE and rerun == False:
                player.shoot()
                shootSound = pyg.mixer.Sound("fire.ogg")
                shootSound.play()
            if e.key == pyg.K_r and rerun == True:
                reset()
    
    window.blit(background,(0,0))

    if pyg.sprite.spritecollide(player,enemies,False) or miss >= 3:
        window.blit(lose,(230,200))
        window.blit(restart,(260,290))
        rerun = True
    elif point >= 50:
        window.blit(win,(230,200))
        window.blit(restart,(260,290))
        rerun = True
    else:
        enemies.draw(window)
        enemies.update()
        player.move()
        bullets.draw(window )
        bullets.update()

        hitCount = font.render("Hit: "+str(point),1,(255,255,255))
        loseCount = font.render("Miss: "+str(miss),1,(255,255,255))
        window.blit(hitCount,(10,10))
        window.blit(loseCount,(10,50))


        collide = pyg.sprite.groupcollide(enemies,bullets,True,True)
        for shot in collide:
            enemy = Enemy("ufo.png",rand.randint(1,2),(rand.randint(1,9)*width//10,10),(70,35))
            enemies.add(enemy)
        for i in collide:
            point += 1
    
    pyg.display.update()
    fps.tick(frame)