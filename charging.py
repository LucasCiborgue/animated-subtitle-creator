from utilities import *

def blend_images(set1_dir, set2_dir, output_dir, steps=10,easing="linear"):
    os.makedirs(output_dir, exist_ok=True)
    file_names = sorted(os.listdir(set1_dir))

    frame_idx = 0
    for name in file_names:
        
        os.makedirs(output_dir, exist_ok=True)
        
        img1 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img2 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")

        for i in range(steps):
            alpha = i / (steps - 1)
            alpha = Easing.apply(easing, alpha)
            
            blended = Image.blend(img1, img2, alpha)
            
            frame_name = os.path.join(output_dir, f"frame_{i:04d}.png")
            #blended.save(os.path.join(output_dir, frame_name))
            blended.save(frame_name)
            
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
