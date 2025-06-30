from utilities import *


def grow_blur_swap(set1_dir, set2_dir, output_dir, steps=40, easing='linear', max_blur=8, max_scale=1.5):
    file_names = sorted(os.listdir(set1_dir))
    frame_idx = 0

    for name in file_names:
        os.makedirs(output_dir, exist_ok=True)
            
        img1 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img2 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")
        width, height = img1.size

        for i in range(steps):
            progress = i / (steps - 1)

            # Split animation at midpoint
            if progress <= 0.5:
                p = Easing.apply(easing, progress / 0.5)

                # img1 grows and blurs
                scale1 = 1 + (max_scale - 1) * p
                blur1 = max_blur * p
                alpha1 = 255

                # img2 is invisible
                scale2 = max_scale
                blur2 = max_blur
                alpha2 = 0

            else:
                p = Easing.apply(easing, (progress - 0.5) / 0.5)

                # img1 fades out
                scale1 = max_scale
                blur1 = max_blur
                alpha1 = int(255 * (1 - p))

                # img2 shrinks and becomes sharp/visible
                scale2 = max_scale - (max_scale - 1) * p
                blur2 = max_blur * (1 - p)
                alpha2 = int(255 * p)

            # Apply transformations
            img1_trans = img1.filter(ImageFilter.GaussianBlur(blur1)).resize(
                (int(width * scale1), int(height * scale1)), Image.LANCZOS)
            img2_trans = img2.filter(ImageFilter.GaussianBlur(blur2)).resize(
                (int(width * scale2), int(height * scale2)), Image.LANCZOS)

            img1_trans.putalpha(alpha1)
            img2_trans.putalpha(alpha2)

            # Composite on transparent canvas
            canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            pos1 = ((width - img1_trans.width) // 2, (height - img1_trans.height) // 2)
            pos2 = ((width - img2_trans.width) // 2, (height - img2_trans.height) // 2)
            canvas.paste(img1_trans, pos1, img1_trans)
            canvas.paste(img2_trans, pos2, img2_trans)

            # Save frame
            canvas.save(os.path.join(output_dir, f"frame_{i:04d}.png"))
        
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)

   