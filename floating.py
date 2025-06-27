from utilities import *

def float_animation(input_folder, placeholder, output_dir, steps=60, canvas_size=(800, 300), amplitude=10):
    os.makedirs(output_dir, exist_ok=True)
    file_names = sorted(os.listdir(input_folder))

    frame_idx = 0
    for file in file_names:
        os.makedirs(output_dir, exist_ok=True)
        subtitle_img = Image.open(os.path.join(input_folder, file)).convert("RGBA")
        text_width, text_height = subtitle_img.size
        canvas_width, canvas_height = canvas_size

        for i in range(steps):
            offset_y = int(amplitude * math.sin(2 * math.pi * i / steps))

            # Create transparent canvas
            frame = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

            # Center + float vertically
            pos = ((canvas_width - text_width) // 2, (canvas_height - text_height) // 2 + offset_y)
            frame.paste(subtitle_img, pos, subtitle_img)

            # Save frame
            frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
            frame.save(frame_path)
            
        createVideoAndDeleteFolder(output_dir, frame_idx,steps)
            
        frame_idx += 1
    
    deleteFolder(input_folder)
    deleteFolder(placeholder)
