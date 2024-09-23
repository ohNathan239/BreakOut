import pygame
import random
pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

class Player(pygame.Rect):

    def __init__(self, x, y):
        super().__init__(x, y, 250, 25)   # arbitrary values TODO tweak
        self.vx = 0

    def draw(self):
        pygame.draw.rect(screen, 'orange', self, 0) # fill
        pygame.draw.rect(screen, 'black', self, 1) # outline

    def update(self):
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

class Ball(pygame.Rect):

    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(0, 2) * random.choice([1, -1])
        self.vy = 4#random.randint(3, 4) # TODO tweak?

    def draw(self):
        pygame.draw.ellipse(screen, 'white', self, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 and self.vx < 0:
            self.vx *= -1
        elif self.x + self.w > screen.get_width() and self.vx > 0:
            self.vx *= -1
        if self.y < 0 and self.vy < 0:
            self.vy *= -1
        elif self.y  > screen.get_height():
            self. y = screen.get_height()//2

player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
ball = Ball(screen.get_width()/2 - 10, screen.get_height()/2 +20, 20)

class Brick(pygame.Rect):

    WIDTH = 80
    HEIGHT = 40

    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y
    #     self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255),)

    def __init__(self, x, y):
        super().__init__(x, y, Brick.WIDTH, Brick.HEIGHT)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self):
        pygame.draw.rect(screen, self.color, self, 0, border_radius= 6) #fill
        pygame.draw.rect(screen, 'grey', self, 2, border_radius= 6) #outline

    # def update(self):

bricks = []
for x in range(0, screen.get_width(), Brick.WIDTH):
    for y in range(100, 400, Brick.HEIGHT):
        bricks.append(Brick(x,y))

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += -6
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += 6
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += 6
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += -6
    # Do logical updates here.
    player.update()
    ball.update()
    if ball.colliderect(player):
        ball.vy *= -1
        ball.y = player.y - ball.width # perhaps sideways collision would look better?
        if (ball.x + ball.w/2) - (player.x + player.w/2) < 25:
            diff = (ball.x + ball.w/2) - (player.x + player.w/2)
        else:
            diff = (ball.x + ball.w / 2) - (player.x + player.w / 2)
        if (diff//5 < 25):
            ball.vx += diff // 5

    for b in bricks:
        if ball.colliderect(b):
            bricks.remove(b)
            ball.vy*=-1
            ball.vx*=-1




    screen.fill('grey')  # Fill the display with a solid color
    # Render the graphics here.
    player.draw()
    ball.draw()
    for b in bricks:
        b.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)