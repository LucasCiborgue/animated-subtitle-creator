from utilities import *


def gradient_transition(set1_dir, set2_dir, output_dir, steps=30,easing="linear"):
    file_names = sorted(os.listdir(set1_dir))

    frame_idx = 0
    for name in file_names:
        os.makedirs(output_dir, exist_ok=True)
        img2 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img1 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")

        width, height = img1.size
        i2 = 0
        for i in range(steps):
            progress = Easing.apply(easing, (i + 2) / steps)
            

            # Create horizontal gradient alpha mask
            gradient = np.zeros((height, width), dtype=np.uint8)
            for x in range(width):            
                alpha = int(255 * ((x/width)-(1 - progress)))
                if alpha < 0:
                    alpha = 0
                    
                if alpha==255:
                    print(alpha)
                
                gradient[:, x] = alpha
                
                #gradient = np.fliplr(gradient)  # Flip left-to-right
            
            # Invert the gradient array
            #gradient = 255 - gradient

            # Create the inverted alpha mask
            alpha_mask = Image.fromarray(gradient, mode='L')            

            # Composite the result
            blended = Image.composite(img1, img2, alpha_mask)
            

            # Save frame
            frame_path = os.path.join(output_dir, f"frame_{i2:04d}.png")
            blended.save(frame_path)
            i2 += 1
        
        bonus = int(steps/10)
        for i in range(bonus):           
            
            # Save frame
            frame_path = os.path.join(output_dir, f"frame_{i2:04d}.png")
            img1.save(frame_path)
            i2 += 1        
        
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
        