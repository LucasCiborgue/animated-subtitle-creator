from utilities import *

def slide_transition(set1_dir, set2_dir, output_dir, steps=20, easing = "linear"):
    file_names = sorted(os.listdir(set1_dir))

    frame_idx = 0
    for name in file_names:
        os.makedirs(output_dir, exist_ok=True)
        
        img2 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img1 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")

        width, height = img1.size

        for i in range(steps):
            # Calculate width of img1 to show
            # Sliding mask width
            slide_progress = Easing.apply(easing, (i + 1) / steps)
            slide_width = int(slide_progress * width)


            # Crop left portion of img1 and paste over img2
            img1_crop = img1.crop((0, 0, slide_width, height))
            frame = img2.copy()
            frame.paste(img1_crop, (0, 0), img1_crop)  # use alpha as mask

            frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            frame.save(frame_path)
        
        
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
           