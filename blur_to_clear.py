from utilities import *


def blur_to_clear(set1_dir, set2_dir, output_dir, steps=30, max_blur=8, max_scale=1.5):
    file_names = sorted(os.listdir(set1_dir))
    frame_idx = 0

    for name in file_names:
        os.makedirs(output_dir, exist_ok=True)
        
        img1 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img2 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")
        width, height = img1.size

        for i in range(steps):
            progress = i / (steps - 1)

            # --- IMAGE 1: blur, shrink, fade out
            blur_amount = max_blur * (1 - progress)
            scale1 = max_scale - (max_scale - 1) * progress
            alpha1 = int(255 * (1 - progress))

            img1_blur = img1.filter(ImageFilter.GaussianBlur(radius=blur_amount))
            img1_scaled = img1_blur.resize(
                (int(width * scale1), int(height * scale1)), Image.LANCZOS
            )
            img1_alpha = img1_scaled.copy()
            img1_alpha.putalpha(alpha1)

            # --- IMAGE 2: fade in
            scale2 = 1 + 0.1 * (1 - progress)  # small entrance scale effect
            alpha2 = int(255 * progress)
            img2_scaled = img2.resize(
                (int(width * scale2), int(height * scale2)), Image.LANCZOS
            )
            img2_alpha = img2_scaled.copy()
            img2_alpha.putalpha(alpha2)

            # --- Canvas and positioning
            canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            img1_pos = (
                (width - img1_alpha.width) // 2,
                (height - img1_alpha.height) // 2,
            )
            img2_pos = (
                (width - img2_alpha.width) // 2,
                (height - img2_alpha.height) // 2,
            )

            canvas.paste(img1_alpha, img1_pos, img1_alpha)
            canvas.paste(img2_alpha, img2_pos, img2_alpha)

            canvas.save(os.path.join(output_dir, f"frame_{i:04d}.png"))
        
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
