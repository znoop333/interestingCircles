import os
import shutil
import subprocess
import math

from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageColor
#from dataclasses import dataclass
from typing import Tuple, List
from random import randint, uniform, choice, random, seed

# %%
seed(0)

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

GHOST_COLORS = []
for color in COLORS:
    c = ImageColor.getrgb(color)
    GHOST_COLORS.append((c[0], c[1], c[2], 128))

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

EARTH_WORM = [
'#CA6671',
'#C46771',
'#BF6972',
'#B96B73',
'#B46C74',
'#AE6E75',
'#A97076',
'#A37177',
'#9E7378',
'#987579',
'#93777A',
'#7E4047', 
'#80454C', 
'#824B51', 
'#845056', 
'#86565B', 
'#885B60', 
'#8A6165', 
'#8C666A', 
'#8E6C6F', 
'#907174', 
'#93777A', 
'#7E4047',
'#854950',
'#8D535A',
'#945D64',
'#9C676D',
'#A47177',
'#AB7B81',
'#B3858A',
'#BA8F94',
'#C2999E',
'#CAA3A8',
'#4B262A',
'#573236',
'#643F43',
'#714B4F',
'#7D585C',
'#8A6469',
'#977175',
'#A37D82',
'#B08A8E',
'#BD969B',
'#CAA3A8',
]

BLUE_WITH_A_TASTE_OF_YELLOW = BLUES + [ '#f48b00', '#c98a2d', 'black', 'white']

def random_color(): 
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def random_curve():
    return uniform(-10, 10)

def random_fill():
    return randint(0, len(COLORS)-1)

def random_grey():
    thing = randint(0, 255)
    return (thing, thing, thing)

def dark_grey():
    thing = randint(0, 100)
    return (thing, thing, thing)

def random_green():
    return (randint(0, 100), randint(150, 255), randint(0, 100))

def random_angle(): 
    return randint(180, 360)

def whites(num):
    return ["white" for _ in range(num)]

def random_blue():
    return choice(BLUES + RED_ORANGES+COLORS+whites(10))

def yellowish():
    base = randint(0,168)
    return (base + 87, base + 56, base)

SO_MANY_CHOICES = BLUES + RED_ORANGES + [random_grey() for _ in range(30)] + COLORS + [yellowish() for _ in range(10)]
R_N_B = BLUES + whites(100)
BG_COLOR = dark_grey()

#@dataclass
class Circle: 
    def __init__(self, r_, xy_):
        self.radius = r_
        self.location = xy_
        self.angle = 0
        self.fill = 0
        self.active= True
        self.curve = 0
        self.oob_deactiavte = False
        self.history = []
        self.opacity = 128

    def __post_init__(self):
        self.angle = random_angle()
        self.curve = random_curve()
        self.fill = random_fill()
        self.history = []

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
        self.history.append(((self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius), BG_COLOR, self.opacity))#choice(R_N_B)))

    def really_draw(self): 
        #if self.oob_deactiavte:
            #return
        out = choice(GHOST_COLORS)
        #out = (out[0], out[1], out[2], randint(0, 255))
        for thing in self.history:
            DRAW.ellipse(thing[0], fill=(out[0], out[1], out[2], thing[2]))

    def maybe_deactivate(self):
        # If we are above 10% of the max we have a chance to deactivate
        if self.x > IMAGE_WIDTH*.97 or self.x < IMAGE_WIDTH * .03:
            if random() > .9:
                self.active = False
                self.oob_deactiavte = True
        if self.y > IMAGE_HEIGHT*.9 or self.y < IMAGE_HEIGHT * .1:
            if random() > .9:
                self.active = False
                self.oob_deactiavte = True


    def step(self):
        if not self.active:
            return
        step = self.radius*1.25
        rad_angle = math.radians(self.angle)
        self.location = (self.x + step*math.cos(rad_angle), 
                         self.y + step*math.sin(rad_angle))
        self.angle += self.curve

        # Maybe decrease radius
        if randint(0, 100) > 99:
            self.radius -= 1
        if random() > .999:
            self.active = False
        #if randint(0, 100) > 99:
            #self.radius += 5
        #Maybe change our rotation
        if randint(0, 100) > 79:
            self.curve = random_curve()

        #self.maybe_deactivate()
        #if self.x + self.radius >= IMAGE_WIDTH  or self.x - self.radius <= 0:
        if self.x  >= IMAGE_WIDTH + self.radius*50 or self.x <= 0 - self.radius*50:
            self.active = False
            self.oob_deactiavte = True
        #if self.y + self.radius >= IMAGE_HEIGHT  or self.y - self.radius <= 0:
        if self.y  >= IMAGE_HEIGHT + self.radius*50 or self.y <= 0 - self.radius*50:
            self.active = False
            self.oob_deactiavte = True
        if self.radius <= 0:
            self.active = False
            
        # gradually change opacity over time
        self.opacity += 1
        if self.opacity > 255:
            self.opacity = 0
            

# Get the current time, use it as the directory we save everything in
SAVE_DIR = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
os.mkdir(SAVE_DIR)
#shutil.copy(__file__, SAVE_DIR)  # Save a copy of this script so that we can recreate stuff

# The size of the image
IMAGE_WIDTH = 6000
IMAGE_HEIGHT = 2000
# Create a new image
CURRENT_IMAGE = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
DRAW = ImageDraw.Draw(CURRENT_IMAGE, 'RGBA')

# Missing: initial setup
circles = []
NUM_CIRCS = 100#00
for i in range(NUM_CIRCS):
    #thang = (NUM_CIRCS - i) / NUM_CIRCS
    #rad = randint(int(50*thang), int(100*thang))
    rad = randint(5, 10)
    x = randint(2*rad, IMAGE_WIDTH-2*rad)
    y = randint(2*rad, IMAGE_HEIGHT-2*rad)
    #x = IMAGE_WIDTH/2
    #y = IMAGE_HEIGHT/2
    circles.append(Circle(rad, (x, y)))

for c in circles:
    while c.active:
        c.draw()
        c.step()
    c.really_draw()

CURRENT_IMAGE.save(os.path.join(SAVE_DIR, "{}.png".format("final")))
#CURRENT_IMAGE.show()