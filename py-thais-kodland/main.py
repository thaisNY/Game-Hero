import pgzrun
import random

#tela incial
WIDTH = 1000
HEIGHT = 700
TITLE = "Hero Adventure"


class Game:
    def __init__(self):
        self.state = "menu"  # estados menu, play, won
        self.music_on = True

    def button_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            if not music.is_playing("background_music"):
                music.play("background_music")
        else:
            music.stop()

    def set_state(self, new_state):
        self.state = new_state

        if self.music_on and not music.is_playing("background_music"):
            music.play("background_music")
        elif not self.music_on:
            music.stop()

game = Game()

# Hero classe
class Player:
    def __init__(self):
        self.sprite = Actor("hero_idle", pos=(400, 500))
        self.speed = 4
        self.jump_speed = -10
        self.gravity = 0.5
        self.dy = 0
        self.jumping = False
        self.lives = 3

    def move(self):
        self.dy += self.gravity
        self.sprite.y += self.dy

        if self.sprite.y >= 500: 
            self.sprite.y = 500
            self.dy = 0
            self.jumping = False

        for block in [block_1, block_2, block_3, block_4, block_5]:
            if self.sprite.colliderect(block) and self.dy > 0:  
                self.sprite.y = block.top
                self.dy = 0
                self.jumping = False

        if keyboard.left:
            self.sprite.x -= self.speed
            self.sprite.image = "hero_move"
        elif keyboard.right:
            self.sprite.x += self.speed
            self.sprite.image = "hero_move"
        else:
            self.sprite.image = "hero_idle"

        self.sprite.x = max(0, min(WIDTH, self.sprite.x))

    def jump(self):
        if not self.jumping:
            self.dy = self.jump_speed
            self.jumping = True

    def reset_position(self):
        self.sprite.pos = (400, 500) #pos inical

player = Player()

# Blocos
block_1 = Rect((500, 400), (200, 20))
block_2 = Rect((300, 300), (200, 20))
block_3 = Rect((500, 220), (400, 20))
block_4 = Rect((0, 100), (800, 20))
block_5 = Rect((500, 100), (200, 20))

# Castelo
castle = Actor("castle_idle", pos=(30, 60))

# Enemy classe
class Enemy:
    def __init__(self, pos, frames):
        self.sprite = Actor(frames[0], pos=pos)
        self.frames = frames
        self.frame_index = 0
        self.frame_speed = 0.1
        self.timer = 0
        self.speed = 2

    def update_position(self):
        self.sprite.x += self.speed
        if self.sprite.x <= 0 or self.sprite.x >= WIDTH:
            self.speed *= -1

    def animate(self):
        self.timer += self.frame_speed
        if self.timer >= 1:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.sprite.image = self.frames[self.frame_index]
            self.timer = 0

enemy = Enemy((400, 380), ["ghost_1", "ghost_2", "ghost_3", "ghost_4"])

# Bat classe
class Bat:
    def __init__(self, pos, frames):
        self.sprite = Actor(frames[0], pos=pos)
        self.frames = frames
        self.frame_index = 0
        self.frame_speed = 0.1
        self.timer = 0
        self.direction = 1

    def update_position(self):
        self.sprite.y += self.direction * 2
        if self.sprite.y <= 150 or self.sprite.y >= 200:  
            self.direction *= -1

    def animate(self):
        self.timer += self.frame_speed
        if self.timer >= 1:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.sprite.image = self.frames[self.frame_index]
            self.timer = 0

bat = Bat((600, 180), ["bat_1", "bat_2", "bat_3"])

# Funcoes
def draw():
    screen.clear()
    if game.state == "menu":
        draw_menu()
    elif game.state == "play":
        draw_game()
    elif game.state == "won":
        draw_won()

def draw_menu():
    screen.draw.text("Hero Adventure", center=(WIDTH / 2, HEIGHT / 4), fontsize=50, color="white")
    draw_button("Start Game", (WIDTH / 2, HEIGHT / 2 - 50))
    draw_button(f"Music: {'ON' if game.music_on else 'OFF'}", (WIDTH / 2, HEIGHT / 2))
    draw_button("Quit", (WIDTH / 2, HEIGHT / 2 + 50))

def draw_button(text, pos):
    button = Rect(pos[0] - 100, pos[1] - 20, 200, 40)
    screen.draw.filled_rect(button, "gray")
    screen.draw.text(text, center=pos, fontsize=30, color="white")

def draw_game():
    screen.draw.text(f"Lives: {player.lives}", topright=(WIDTH - 10, 10), fontsize=30, color="white")
    player.sprite.draw()
    screen.draw.filled_rect(block_1, "gray")
    screen.draw.filled_rect(block_2, "gray")
    screen.draw.filled_rect(block_3, "gray")
    screen.draw.filled_rect(block_4, "gray")
    screen.draw.filled_rect(block_5, "gray")
    enemy.sprite.draw()
    castle.draw()
    bat.sprite.draw()

def draw_won():
    screen.draw.text("YOU WON", center=(WIDTH / 2, HEIGHT / 2), fontsize=100, color="white")

def on_mouse_down(pos):
    if game.state == "menu":
        if button_click(pos, (WIDTH / 2, HEIGHT / 2 - 50)):
            game.set_state("play")
        elif button_click(pos, (WIDTH / 2, HEIGHT / 2)):
            game.button_music()
        elif button_click(pos, (WIDTH / 2, HEIGHT / 2 + 50)):
            quit_game()

def button_click(pos, button_center):
    button = Rect(button_center[0] - 100, button_center[1] - 20, 200, 40)
    return button.collidepoint(pos)

def quit_game():
    import sys
    sys.exit()

def update():
    if game.state == "play":
        player.move()
        enemy.update_position()
        enemy.animate()
        bat.update_position()
        bat.animate()
        check_collision()

def on_key_down(key):
    if game.state == "play" and key == keys.SPACE:
        player.jump()

def check_collision():
    if player.sprite.colliderect(enemy.sprite) or player.sprite.colliderect(bat.sprite):
        player.lives -= 1
        player.reset_position()
        if player.lives <= 0:
            game.set_state("menu")
            player.lives = 3
    if player.sprite.colliderect(castle):
        game.set_state("won")

pgzrun.go()
