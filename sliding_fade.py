from utilities import *


def slide_transition_with_fade(set1_dir, set2_dir, output_dir, steps=20, easing="linear"):
    
    file_names = sorted(os.listdir(set1_dir))

    frame_idx = 0
    for name in file_names:
        os.makedirs(output_dir, exist_ok=True)
        
        img2 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img1 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")

        width, height = img1.size

        i2 = 0
        for i in range(steps):
            slide_width = int((i + 1) / steps * width)
            # Fade in/out effect
            fade_progress = Easing.apply(easing, (i + 1) / steps)
            fade_alpha = int(255 * fade_progress)

            # Crop the sliding portion
            img1_crop = img1.crop((0, 0, slide_width, height))

            # Apply fade to alpha channel
            r, g, b, a = img1_crop.split()
            a = a.point(lambda px: min(px, fade_alpha))
            img1_fade = Image.merge('RGBA', (r, g, b, a))

            # Paste fade crop over base image
            frame = img2.copy()
            frame.paste(img1_fade, (0, 0), img1_fade)

            frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            frame.save(frame_path)
            i2 = i2+1

            
        bonus = int(steps/25)
        frame = img1.copy()
        for i in range(bonus):
            # Save frame
            frame_path = os.path.join(output_dir, f"frame_{i2:04d}.png")
            frame.save(frame_path)
            i2=i2+1
            
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
