from utilities import *


def counter_shake(set1_dir, set2_dir, output_dir, steps=20,easing = "linear", shake_range=12,speed_multiplier=2):
    os.makedirs(output_dir, exist_ok=True)
    file_names = sorted(os.listdir(set1_dir))
    frame_idx = 0

    for name in file_names:
        os.makedirs(output_dir, exist_ok=True)
        
        img1 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img2 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")
        width, height = img1.size

        for i in range(steps):
            # Increase frequency using speed_multiplier
            # Shaky motion angle (oscillating faster with easing)
            oscillation = Easing.apply(easing, i / steps)
            angle = oscillation * 2 * np.pi * speed_multiplier

            # Faster shaking motion
            offset_x = int(np.sin(angle) * shake_range)
            offset_y = int(np.cos(angle) * shake_range)

            canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))

            # Shake in opposite directions
            pos1 = (
                (width - img1.width) // 2 + offset_x,
                (height - img1.height) // 2 - offset_y
            )
            pos2 = (
                (width - img2.width) // 2 - offset_x,
                (height - img2.height) // 2 + offset_y
            )

            canvas.paste(img1, pos1, img1)
            canvas.paste(img2, pos2, img2)

            canvas.save(os.path.join(output_dir, f"frame_{i:04d}.png"))
        
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
