import os
from PIL import Image, ImageDraw, ImageFont
from utilities import *


phrases = [
    "Fenomenal"
    
]
#"""
color_main_rgb=(39, 215, 207)
color_main2_rgb=(27, 56, 57)
color_shadow_rgb=(39, 107, 215)
color_highlight_rgb=(39, 107, 215)
#"""


"""
color_main_rgb=(215, 124, 40)
color_main2_rgb=(103, 68, 36)
color_shadow_rgb=(134, 38, 89)
#color_highlight_rgb=(39, 107, 215)
#"""

generate_images(
    phrases = phrases,
    output_folder='phrases_images',
    color_shadow_rgb=color_shadow_rgb,        # shadow
    color_highlight_rgb = color_shadow_rgb,   # highlight
    color_main_rgb = color_main_rgb           # main text
)

generate_images(
    phrases = phrases,
    output_folder='phrases_images2',
    color_shadow_rgb=color_shadow_rgb,        # shadow
    color_highlight_rgb = color_shadow_rgb,   # highlight
    color_main_rgb = color_main2_rgb          # main text
)