from utilities import *


def invertedBig(set1_dir, set2_dir, output_dir, steps=30):
    file_names = sorted(os.listdir(set1_dir))
    frame_idx = 0

    for name in file_names:
        os.makedirs(output_dir, exist_ok=True)
        img1 = Image.open(os.path.join(set1_dir, name)).convert("RGBA")
        img2 = Image.open(os.path.join(set2_dir, name)).convert("RGBA")
        width, height = img1.size

        for step in range(steps):
            progress = step / (steps - 1)

            # img1 shrinks and fades out
            scale1 = 1.0 - 0.3 * progress   # from 1.0 → 0.7
            alpha1 = 1.0 - progress         # from 1.0 → 0.0

            # img2 grows and fades in
            scale2 = 0.6 + 0.25 * progress  # from 0.6 → 0.85
            alpha2 = progress               # from 0.0 → 1.0

            # Create base transparent canvas
            canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))

            # --- Process img1 ---
            img1_scaled = img1.resize(
                (int(width * scale1), int(height * scale1)), resample=Image.LANCZOS
            )
            img1_alpha = ImageEnhance.Brightness(img1_scaled.split()[3]).enhance(alpha1)
            img1_scaled.putalpha(img1_alpha)
            pos1 = ((width - img1_scaled.width) // 2, (height - img1_scaled.height) // 2)
            canvas.paste(img1_scaled, pos1, img1_scaled)

            # --- Process img2 ---
            img2_scaled = img2.resize(
                (int(width * scale2), int(height * scale2)), resample=Image.LANCZOS
            )
            img2_alpha = ImageEnhance.Brightness(img2_scaled.split()[3]).enhance(alpha2)
            img2_scaled.putalpha(img2_alpha)
            pos2 = ((width - img2_scaled.width) // 2, (height - img2_scaled.height) // 2)
            canvas.paste(img2_scaled, pos2, img2_scaled)

            # Save frame
            canvas.save(os.path.join(output_dir, f"frame_{step:04d}.png"))
            
        createVideoAndDeleteFolder(output_dir, frame_idx)
            
        frame_idx += 1
    
    deleteFolder(set1_dir)
    deleteFolder(set2_dir)
