import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Set up the fonts
font = pygame.font.SysFont("Garamond", 32)

# Set up the colors
GREEN = (77, 158, 158)
WHITE = (245, 245, 220)

# Set up the paddles and ball
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_WIDTH = 20
BALL_HEIGHT = 20

player1_score = 0
player2_score = 0

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.velocity = 0

    def draw(self, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

class Ball:
    def __init__(self):
        self.x = WIDTH/2 - BALL_WIDTH/2
        self.y = HEIGHT/2 - BALL_HEIGHT/2
        self.width = BALL_WIDTH
        self.height = BALL_HEIGHT
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.randint(-5, 5)

    def draw(self, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y < 0 or self.y > HEIGHT - self.height:
            self.velocity_y = -self.velocity_y

        if self.x < 0:
            self.reset(2)
        if self.x > WIDTH - self.width:
            self.reset(1)

    def reset(self, player):
        global player1_score, player2_score
        if player == 1:
            player1_score += 1
            self.velocity_x = -self.velocity_x
        elif player == 2:
            player2_score += 1
            self.velocity_x = -self.velocity_x
        self.x = WIDTH/2 - BALL_WIDTH/2
        self.y = HEIGHT/2 - BALL_HEIGHT/2
        self.velocity_y = random.randint(-5, 5)

# Set up the players and ball
player1 = Paddle(50, HEIGHT/2 - PADDLE_HEIGHT/2)
player2 = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT/2 - PADDLE_HEIGHT/2)
ball = Ball()

# Set up the game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.velocity = -5
            if event.key == pygame.K_s:
                player1.velocity = 5
            if event.key == pygame.K_UP:
                player2.velocity = -5
            if event.key == pygame.K_DOWN:
                player2.velocity = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1.velocity = 0
            if event.key == pygame.K_s:
                player1.velocity = 0
            if event.key == pygame.K_UP:
                player2.velocity = 0
            if event.key == pygame.K_DOWN:
                player2.velocity = 0

    # Clear the screen
    screen.fill(GREEN)

    # Draw the paddles and ball
    player1.draw(WHITE)
    player2.draw(WHITE)
    ball.draw(WHITE)

    # Move the paddles and ball
    player1.move()
    player2.move()
    ball.move()

    # Check for collisions between the ball and paddles
    if ball.x < player1.x + player1.width and \
       ball.x + ball.width > player1.x and \
       ball.y < player1.y + player1.height and \
       ball.y + ball.height > player1.y:
        ball.velocity_x = -ball.velocity_x

    if ball.x < player2.x + player2.width and \
       ball.x + ball.width > player2.x and \
       ball.y < player2.y + player2.height and \
       ball.y + ball.height > player2.y:
        ball.velocity_x = -ball.velocity_x

    # Check for player scores
    player1_text = font.render("Player 1: {}".format(player1_score), True, WHITE)
    player2_text = font.render("Player 2: {}".format(player2_score), True, WHITE)
    screen.blit(player1_text, (50, 50))
    screen.blit(player2_text, (WIDTH - player2_text.get_width() - 50, 50))

    if player1_score >= 10:
        game_over_text = font.render("Player 1 wins!", True, WHITE)
        screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))
        running = False

    if player2_score >= 10:
        game_over_text = font.render("Player 2 wins!", True, WHITE)
        screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))
        running = False

    # Update the screen
    pygame.display.flip()

    # Limit the framerate
    clock.tick(60)

# Quit Pygame
pygame.quit()