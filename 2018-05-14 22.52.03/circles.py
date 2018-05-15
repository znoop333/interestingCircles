import os
import shutil
import subprocess
import math

from datetime import datetime
from PIL import Image, ImageDraw
from dataclasses import dataclass
from typing import Tuple, List
from random import randint, uniform, choice, random

COLORS = ['#F0CA4D',
          '#324d5c', 
          '#f2a336',
          '#BD9E20',
          '#0A1C28',
          '#EEE9D1',
          '#333741',
          '#F1EAD1',
          '#424142',
          '#BFB7A8',
          '#111826',
          '#F0EBEF',
          '#1477B2',
          '#0C3F60',
          '#12537E' ]

BLUES = [ '#060B23',
          '#162137',
          '#27374B',
          '#374D5F',
          '#486373',
          '#597987',
          '#698F9B',
          '#7AA5AF',
          '#8ABBC3',
          '#9BD1D7',
          '#ACE8EC',]

RED_ORANGES = [
    '#E36D60',
    '#DB6860',
    '#D46461',
    '#CD6062',
    '#C65C63',
    '#BF5864',
    '#B85364',
    '#B14F65',
    '#AA4B66',
    '#A34767',
    '#9C4368',
]


def random_color(): 
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def random_curve():
    return uniform(-20, 20)

def random_fill():
    return randint(0, len(COLORS)-1)

def random_grey():
    thing = randint(200, 210)
    return (thing, thing, thing)

def random_green():
    return (randint(0, 100), randint(150, 255), randint(0, 100))

def random_angle(): 
    return randint(180, 360)

def whites(num):
    return ["white" for _ in range(num)]

def random_blue():
    return choice(BLUES + RED_ORANGES+COLORS+whites(10))

@dataclass
class Circle: 
    radius: float
    location: Tuple[int, int]
    angle: int = 0
    fill = 0
    active: bool = True
    curve: int = 0
    oob_deactiavte = False
    history = []

    def __post_init__(self):
        self.angle = random_angle()
        self.curve = random_curve()
        self.fill = random_fill()

    @property
    def x(self):
        return self.location[0]

    @property
    def y(self):
        return self.location[1]

    def draw(self): 
        if not self.active:
            return
        #DRAW.ellipse((self.x - self.radius, 
                     #self.y - self.radius,
                     #self.x + self.radius,
                     #self.y + self.radius), fill=random_blue())
        self.history.append(((self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius), random_blue()))

    def really_draw(self): 
        print(len(self.history))
        if self.oob_deactiavte:
            return
        for thing in self.history:
            DRAW.ellipse(thing[0], fill=thing[1])
    
    def next_color(self):
        maybe_next = randint(0, len(COLORS)-1)
        # don't know if I care if we repeat ourselves...
        self.fill = maybe_next

    def maybe_deactivate(self):
        # If we are above 10% of the max we have a chance to deactivate
        if self.x > IMAGE_WIDTH*.9 or self.x < IMAGE_WIDTH * .1:
            if random() > .5:
                self.active = False
                self.oob_deactiavte = True
        if self.y > IMAGE_HEIGHT*.9 or self.y < IMAGE_HEIGHT * .1:
            if random() > .5:
                self.active = False
                self.oob_deactiavte = True


    def step(self):
        if not self.active:
            return
        step = self.radius/2
        rad_angle = math.radians(self.angle)
        self.location = (self.x + step*math.cos(rad_angle), 
                         self.y + step*math.sin(rad_angle))
        self.angle += self.curve
        self.next_color()

        # Maybe decrease radius
        if randint(0, 100) > 20:
            self.radius -= 1
        #Maybe change our rotation
        if randint(0, 100) > 79:
            self.curve = random_curve()

        self.maybe_deactivate()
        if self.x > IMAGE_WIDTH + self.radius or self.x < 0 - self.radius:
            self.active = False
        if self.y > IMAGE_HEIGHT + self.radius or self.y < 0 - self.radius:
            self.active = False
        if self.radius <= 0:
            self.active = False

# Get the current time, use it as the directory we save everything in
SAVE_DIR = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
os.mkdir(SAVE_DIR)
shutil.copy(__file__, SAVE_DIR)  # Save a copy of this script so that we can recreate stuff

# The size of the image
IMAGE_WIDTH = 5000
IMAGE_HEIGHT = 1000
# Create a new image
CURRENT_IMAGE = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color="black")
DRAW = ImageDraw.Draw(CURRENT_IMAGE)

# Missing: initial setup
circles = []
for _ in range(1):
    rad = randint(10, 30)
    x = randint(0, IMAGE_WIDTH)
    y = randint(0, IMAGE_HEIGHT)
    circles.append(Circle(rad, (x, y)))

# How many iterations?
MAX_ITERATIONS = 0
# The main loop, mess with the image for each iteration
for i in range(MAX_ITERATIONS):
    for circle in circles:
        circle.draw()
        circle.step()
    # Manipulate the image before saving it
    CURRENT_IMAGE.save(os.path.join(SAVE_DIR, "{}.png".format(i)))

    # Every so often print out something so we get a sense of progress
    if i % 10 == 0:
        print('Iteration {}'.format(i), flush=True)

for c in circles:
    while c.active:
        c.draw()
        c.step()
    c.really_draw()

CURRENT_IMAGE.show()
CURRENT_IMAGE.save(os.path.join(SAVE_DIR, "{}.png".format("final")))


def gifit(image_loc, gif_name, fps=12):
    """ Creates a GIF from all the pngs in the provide image_loc """
    import glob
    import moviepy.editor as mpy

    os.chdir(image_loc)
    file_list = glob.glob('*.png')
    list.sort(file_list, key=lambda x: int(x.split('.png')[0]))
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('{}.gif'.format(gif_name), fps=fps)


#gifit(SAVE_DIR, 'final')
#subprocess.run('start final.gif', shell=True)
