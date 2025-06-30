from utilities import *

def sliding_gradient_transition(set1_dir, set2_dir, output_dir, steps=30,easing="linear", gradient_width=100):
    file_names = sorted(os.listdir(set1_dir))

    frame_idx = 0
    for name in file_names:
        
        os.makedirs(output_dir, exist_ok=True)
        
        img1 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img2 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")
        width, height = img1.size

        for i in range(steps):
            # Mask clipping width
            slide_x = int(Easing.apply(easing, i / steps) * width)
            effective_width = min(slide_x, width)

            # Crop img2 to current slide width
            img2_crop = img2.crop((0, 0, effective_width, height))

            # Create alpha gradient mask for img2_crop
            gradient = np.ones((height, effective_width), dtype=np.uint8) * 255

            if gradient_width > 0 and effective_width > gradient_width:
                for x in range(gradient_width):
                    alpha = int(255 * (x / gradient_width))
                    gradient[:, -gradient_width + x] = alpha

            alpha_mask = Image.fromarray(gradient, mode='L')
            img2_fade = img2_crop.copy()
            img2_fade.putalpha(alpha_mask)

            # Paste over img1
            frame = img1.copy()
            frame.paste(img2_fade, (0, 0), img2_fade)

            frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            frame.save(frame_path)
        
        
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
        