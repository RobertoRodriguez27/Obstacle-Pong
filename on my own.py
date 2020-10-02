import pygame
import random

pygame.init()

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Tito's First")
player_sprites = pygame.sprite.Group()
ball_sprite = pygame.sprite.Group()
boundaries_sprites = pygame.sprite.Group()
background = pygame.image.load("pong mega dome.png")

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, play_x, play_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 70))
        self.image.fill([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (700 // 2, 500 // 2)
        self.rect.x = play_x
        self.rect.y = play_y
        self.width = 15
        self.height = 70
        self.vel = 20
        self.up = False
        self.down = False
        self.point = 0
        self.hitBox = (self.rect.x, self.rect.y, self.width, self.height)

    def update(self, win):
        if not (self.up and self.down):
            pygame.draw.rect(win, (0, 0, 0), (self.rect.x, self.rect.y, self.width, self.height))
        elif self.up:
            self.rect.y += self.vel
            pygame.draw.rect(win, (0, 0, 0), (self.rect.x, self.rect.y, self.width, self.height))
        else:
            self.rect.y -= self.vel
            pygame.draw.rect(win, (0, 0, 0), (self.rect.x, self.rect.y, self.width, self.height))
        self.hitBox = (self.rect.x, self.rect.y, self.width, self.height)  # update hitBox with movement
        pygame.draw.rect(win, (255, 0, 0), self.hitBox, 2)  # hitBox visual


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (700 // 2, 500 // 2)
        self.dx = random.choice([-10, 10])
        self.dy = random.choice([-15, -10, 10, 15])

    def update(self, win):
        self.rect.x += self.dx
        self.rect.y += self.dy
        pygame.draw.rect(win, [0, 0, 0], (self.rect.x, self.rect.y, 25, 25))
        # constraints
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > 500:
            self.dy *= -1

        collide = pygame.sprite.spritecollideany(ball, player_sprites)  # collision for ball and player
        collide2 = pygame.sprite.spritecollideany(ball, boundaries_sprites)  # collision for ball
        if collide:  # here, player collides with ball to return it back
            if collide == player1:
                self.rect.x -= self.dx
                self.dx *= -1
                self.dx += random.choice([0, 1])
            if collide == player2:
                self.rect.x -= self.dx
                self.dx *= -1
                self.dx += random.choice([0, 1])
        if collide2:  # obstacle collides with ball, returning it back
            self.rect.x -= self.dx
            self.dx *= -1
            self.dx += random.choice([0, 1])

            # this is to avoid y's speed from slowing down
            if self.dy == 0:
                self.dy += random.choice([-1, 1])
            if self.dy <= 0:
                self.dy += -random.choice([-1, 0, 1])
            if self.dy >= 0:
                self.dy += random.choice([-1, 1])


# In charge of generating obstacles.
# takes in a sprite as a parameter to generate a new
# obstacle sprite to later add to boundary_sprites group
class Obstacles(pygame.sprite.Sprite):
    # Obstacle "constructor"
    # obst_x: obstacle's starting x position
    # obst_y: obstacle's starting y position
    # obst_speed: obstacle's moving speed
    def __init__(self, obst_x, obst_y, obst_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 50))
        self.color = (0, 85, 102)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = obst_x
        self.rect.y = obst_y
        self.speed = obst_speed
        self.width, self.height = 15, 50

    # updates positions for obstacles and redraws obstacles in
    # new positions
    # win: game window that game is held on
    def update(self, win):
        self.rect.y += self.speed
        pygame.draw.rect(win, self.color, (self.rect.x, self.rect.y, self.width, self.height))


# redraws the game window by calling object's
# update window. Helps in de-cluttering mainloop
def redrawGameWindow():
    window.blit(background, (0, 0))
    text = font.render("Player 1: " + str(player1.point), 1, (0, 0, 0))
    text2 = font.render("Player 2: " + str(player2.point), 1, (0, 0, 0))
    window.blit(text, (10, 10))
    window.blit(text2, (550, 10))
    player1.update(window)
    player2.update(window)

    for ob in obstacles:  # loops through all objects in obstacles list
        ob.update(window)

    ball.update(window)
    pygame.display.update()


# method in charge of movement of players
# player: gets a specified player instance
# up_key: key that moves player up depending on player instance
# down_key: key that moves player down depending on player instance
def movement(player, up_key, down_key):
    keys = pygame.key.get_pressed()  # makes list of all pressed keys from key board

    if keys[up_key] and player.rect.y > 20:  # If up button and top of player below 20 px
        player.rect.y -= player.vel  # update the players position
        player.up = True
        player.down = False
    elif keys[down_key] and player.rect.y + player.height < 500 - 20:  # moving player down
        player.rect.y += player.vel
        player.up = False
        player.down = True
    else:  # player is not moving
        player.up = False
        player.down = False


# gets an x, y, and random speed
# pos: chooses the corresponding position
# return: tuple with x, y, anf random speed
def generate_pos(pos):
    speed_pos = [10, 100, 50, 20, 35, 100, 50]
    pos_x, pos_y = 0, 0
    if pos == "topL":
        pos_y = 0
        pos_x = 200
    elif pos == "topC":
        pos_y = 0
        pos_x = 350
    elif pos == "topR":
        pos_y = 0
        pos_x = 600
    elif pos == "botL":
        pos_y = 400
        pos_x = 100
    elif pos == "botC":
        pos_y = 400
        pos_x = 350
    elif pos == "botR":
        pos_y = 400
        pos_x = 600
    return pos_x, pos_y, random.choice(speed_pos)


def point():
    if ball.rect.x < 0:
        player2.point += 1
        ball.rect.center = (700 // 2, 500 // 2)
    if ball.rect.x > 700:
        player1.point += 1
        ball.rect.center = (700 // 2, 500 // 2)
    if player1.point - player2.point > 5:
        player1.height = 50
    if player2.point - player1.point > 5:
        player2.height = 50


# mainloop
font = pygame.font.SysFont("comicsans", 30)
player1 = Player(10, 200)  # makes player1 object at x, y coordinates
player2 = Player(675, 200)  # does same as above but with player2
player_sprites.add(player1)  # sprite group that contains both players
player_sprites.add(player2)
ball = Ball()  # makes ball object
ball_sprite.add(ball)  # adds ball to ball sprite group
obstacles = []  # holds instances of Obstacle and used for looping through generated Obstacles
loop = 0  # helps keep track of generated Obstacles
run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():  # grabs events from pygame. Keeps track if program closed
        if event.type == pygame.QUIT:
            run = False

    # loops and generates new block obstacles that change
    if loop > 0:
        loop += 1
    if loop > 3:
        loop = 0

    for obstacle in obstacles:
        boundaries_sprites.add(obstacle)
        hit = pygame.sprite.spritecollideany(ball, boundaries_sprites)
        if hit:
            ball.update(window)
        if obstacle.rect.y - obstacle.height > 500:
            obstacles.remove(obstacle)

    if loop == 0:
        if len(obstacles) < 10:
            start = ["topL", "topC", "topR", "botL", "botC", "botR"]
            x, y, speed = generate_pos(random.choice(start))
            obstacles.append(Obstacles(x, y, speed))
        loop = 1

    point()
    movement(player1, pygame.K_w, pygame.K_s)  # helper method to declutter mainloop
    movement(player2, pygame.K_UP, pygame.K_DOWN)  # and reduce repeated code

    redrawGameWindow()  # update game window by redrawing sprites to keep movement updated

pygame.quit()
