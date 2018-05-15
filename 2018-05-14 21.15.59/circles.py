import os
import shutil

from datetime import datetime
from PIL import Image, ImageDraw
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Circle: 
    radius: float
    location: Tuple[float, float]

# Get the current time, use it as the directory we save everything in
SAVE_DIR = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
os.mkdir(SAVE_DIR)
shutil.copy(__file__, SAVE_DIR)  # Save a copy of this script so that we can recreate stuff

# The size of the image
IMAGE_SIZE = 100, 100
# Create a new image
CURRENT_IMAGE = Image.new('RGB', IMAGE_SIZE)
DRAW = ImageDraw.Draw(CURRENT_IMAGE)

# Missing: initial setup

# How many iterations?
MAX_ITERATIONS = 100
# The main loop, mess with the image for each iteration
for i in range(MAX_ITERATIONS):
    # Manipulate the image before saving it
    CURRENT_IMAGE.save(os.path.join(SAVE_DIR, "{}.png".format(i)))

    # Every so often print out something so we get a sense of progress
    if i % 10 == 0:
        print('Iteration {}'.format(i), flush=True)


def gifit(image_loc, gif_name, fps=12):
    """ Creates a GIF from all the pngs in the provide image_loc """
    import glob
    import moviepy.editor as mpy

    os.chdir(image_loc)
    file_list = glob.glob('*.png')
    list.sort(file_list, key=lambda x: int(x.split('.png')[0]))
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('{}.gif'.format(gif_name), fps=fps)


gifit(SAVE_DIR, 'final')