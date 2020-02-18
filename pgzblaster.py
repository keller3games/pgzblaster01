import random, time, sys
import pygame, pgzrun

WIDTH, HEIGHT = 500, 700


class Ship(Actor):
    def __init__(self):
        Actor.__init__(self, 'ship')
        self.bottom = HEIGHT
        self.centerx = WIDTH / 2
        self.vel = 6

    def update(self):
        if keyboard.left:
            self.x -= self.vel
        if keyboard.right:
            self.x += self.vel
        self.clamp_ip(0, 0, WIDTH, HEIGHT)

    def launch_rocket(self):
        rocket = Rocket(self.x, self.y-50)
        game.rockets.append(rocket)

    def hit(self):
        sounds.ship_hit.play()
        time.sleep(3)
        sys.exit()


class Rocket(Actor):
    def __init__(self, x, y):
        Actor.__init__(self, 'rocket')
        sounds.rocket_launch.play()
        self.alive = True
        self.x = x
        self.y = y
        self.vel = 10

    def update(self):
        self.y -= self.vel
        if(self.top < 0):
            self.alive = False
        for ufo in game.ufos:
            if self.colliderect(ufo):
                ufo.hit()
                self.alive = False
                return


class UFO(Actor):
    def __init__(self, x, y):
        Actor.__init__(self, 'ufo')
        self.alive = True
        self.x = x
        self.y = y
        self.x_vel = 2
        self.y_vel = 1
        self.bomb_rate = 0.007

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

        if self.left < 0 and self.x_vel < 0:
            self.x_vel *= -1
        if self.right > WIDTH and self.x_vel > 0:
            self.x_vel *= -1

        if self.top > HEIGHT:
            self.alive = False

        if decide(self.bomb_rate) and self.top > 0:
            self.drop_bomb()

        if self.colliderect(game.ship):
            game.ship.hit()

    def drop_bomb(self):
        game.bombs.append(Bomb(self.center))

    def hit(self):
        sounds.ufo_hit.play()
        self.alive = False


class Bomb(Actor):
    def __init__(self, center):
        Actor.__init__(self, 'bomb')
        sounds.bomb_drop.play()
        self.alive = True
        self.center = center
        self.vel = 5

    def update(self):
        self.y += self.vel
        if self.top > HEIGHT:
            self.alive = False
        if self.colliderect(game.ship):
            game.ship.hit()


class Game:
    def __init__(self):
        self.ship = Ship()
        self.rockets = []
        self.ufos = []
        self.bombs = []


def make_ufo_squadron(n_ufos):
    return [UFO(i*40, -i*40) for i in range(0, n_ufos)]


def decide(chance):
    return random.random() < chance


def on_key_down():
    if keyboard.space:
        game.ship.launch_rocket()


def update():
    for actor in game.rockets + game.bombs + game.ufos:
        actor.update()
    game.ship.update()

    game.rockets = [r for r in game.rockets if r.alive]
    game.ufos = [u for u in game.ufos if u.alive]
    game.bombs = [b for b in game.bombs if b.alive]

    if len(game.ufos) == 0:
        game.ufos = make_ufo_squadron(10)


def draw():
    screen.fill((255, 255, 255))

    for actor in game.rockets + game.bombs + game.ufos:
        actor.draw()
    game.ship.draw()


game = Game()
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 1024)
pgzrun.go()