import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import subprocess
import math
import shutil


def text_to_image(text, output_path='output.png', font_size=80, image_size=(1000, 400),
                  color_shadow_rgb=(128, 128, 128),      # gray shadow
                  color_highlight_rgb=(211, 211, 211),   # light gray highlight
                  color_main_rgb=(0, 0, 0),              # black main text
                  line_spacing=6):         
    # Create a transparent image (RGBA)
    
    print(image_size)
    
    #colors = [color_main_rgb, color_shadow_rgb, color_highlight_rgb]

    #ic = inverse_average_color(colors) # inverse_color
    ic = [ 0, 0, 0]
    
    image = Image.new('RGBA', tuple(map(int, image_size)), (ic[0], ic[1], ic[2], 0))    
    draw = ImageDraw.Draw(image)
    
    DISTANCE = 2

    # Load italic font
    try:
        font = ImageFont.truetype("ariali.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Split into lines
    lines = text.split('\\n')
    print("utilities")
    print(lines)

    # Measure height of one line
    _, _, _, line_height = draw.textbbox((0, 0), "Ag", font=font)
    total_height = len(lines) * line_height + (len(lines) - 1) * line_spacing
    
    # Start drawing vertically centered
    y = (image_size[1] - total_height) // 2

    for line in lines:
        # Measure this line
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (image_size[0] - line_width) // 2

        # Draw shadows and main text
        draw.text((x - DISTANCE, y - DISTANCE), line, fill=color_shadow_rgb + (255,), font=font)
        draw.text((x + DISTANCE, y + DISTANCE), line, fill=color_highlight_rgb + (255,), font=font)
        draw.text((x, y), line, fill=color_main_rgb + (255,), font=font)

        y += line_height + line_spacing

    # Save and show
    image.save(output_path, "PNG")
    #image.show()


def generate_images(phrases, output_folder='phrases_images', font_path="ariali.ttf",
                    font_size=80, image_size=(1000, 400),
                    color_shadow_rgb=(128, 128, 128),      # gray shadow
                    color_highlight_rgb=(211, 211, 211),   # light gray highlight
                    color_main_rgb=(0, 0, 0),              # black main text
                    line_spacing=6):    

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    INITIAL_COUNT = 15

    # Generate an image for each phrase
    for idx, phrase in enumerate(phrases):
        filename = f"frame_{idx+1:04d}.png"
        output_path = os.path.join(output_folder, filename)
        text_to_image(phrase, output_path, font_size, image_size, color_shadow_rgb, color_highlight_rgb, color_main_rgb, line_spacing)



def inverse_average_color(colors):
    if not colors:
        raise ValueError("Color list is empty.")

    # Average each RGB channel
    avg_r = sum(c[0] for c in colors) // len(colors)
    avg_g = sum(c[1] for c in colors) // len(colors)
    avg_b = sum(c[2] for c in colors) // len(colors)

    # Invert the average color
    inv_r = 255 - avg_r
    inv_g = 255 - avg_g
    inv_b = 255 - avg_b

    return (inv_r, inv_g, inv_b)
    

def create_video_from_frames(command):

    # Run the command and wait for it to finish
    subprocess.run(command, check=True)  


def deleteFolder(output_dir):
    # Check if folder exists before deleting
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Deleted folder: {output_dir}")
    else:
        print(f"Folder not found: {output_dir}")
    
    
def createVideoAndDeleteFolder(output_dir, frame_idx, frame_rate=60):
    command = [
        'ffmpeg',
        '-framerate', f"{frame_rate}",
        '-i', f"{output_dir}//frame_%04d.png",
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        f"{output_dir}_{frame_idx:04d}.mp4"
    ]

    create_video_from_frames(command)
    deleteFolder(output_dir)
