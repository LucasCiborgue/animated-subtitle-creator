import json
import tkinter as tk
from tkinter import scrolledtext, colorchooser
from utilities import *
from sliding_fade import slide_transition_with_fade
from sliding import slide_transition
from inverted_big import invertedBig
from charging import blend_images
from gradient import gradient_transition
from floating import float_animation
from sliding_gradient import sliding_gradient_transition


def subtitle(opt1, opt2, opt3, steps):
    #place holder
    return 0

class subtitleApp():


    def refresh_preset_menu(self):
        menu = self.preset_dropdown["menu"]
        menu.delete(0, "end")
        self.preset_files = [
            f[:-5] for f in os.listdir(self.PRESET_DIR)
            if f.endswith(".json")
        ]
        for name in self.preset_files:
            menu.add_command(label=name, command=lambda n=name: self.preset_selector_var.set(n))
        if self.preset_files:
            self.preset_selector_var.set(self.preset_files[0])

    def save_preset(self,preset_name):
        if not preset_name:
            print("[ERROR] Preset name required.")
            return
        colors = [label.cget("bg") for label in self.color_labels[:6]]
        path = os.path.join(self.PRESET_DIR, f"{preset_name}.json")
        with open(path, "w") as f:
            json.dump(colors, f)
        print(f"[INFO] Preset '{preset_name}' saved.")
        self.refresh_preset_menu()  # Update dropdown list

    def load_preset(self,preset_name):
        path = os.path.join(self.PRESET_DIR, f"{preset_name}.json")
        if not os.path.exists(path):
            print(f"[WARN] Preset '{preset_name}' not found.")
            return
        with open(path, "r") as f:
            colors = json.load(f)
        for i, color in enumerate(colors):
            self.color_labels[i].config(bg=color)
        print(f"[INFO] Preset '{preset_name}' loaded.")

    def hex_to_rgb(self,hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def handle_button_click(self,index, text_widget):
        output_folder = f"set{index + 1}"
        print(f"[INFO] Generating images in folder: {output_folder}")

        # Text input
        text_input = text_widget.get("1.0", tk.END).strip()
        phrases = [line.strip() for line in text_input.splitlines() if line.strip()]
        if not phrases:
            print("[WARN] No phrases found.")
            return

        print(phrases)
        
        # Get colors
        try:
            color_shadow_rgb   = self.hex_to_rgb(self.color_labels[0].cget("bg"))
            color_highlight_rgb = self.hex_to_rgb(self.color_labels[1].cget("bg"))
            color_main_rgb     = self.hex_to_rgb(self.color_labels[2].cget("bg"))
            color_shadow_rgb02   = self.hex_to_rgb(self.color_labels[3].cget("bg"))
            color_highlight_rgb02 = self.hex_to_rgb(self.color_labels[4].cget("bg"))
            color_main_rgb02     = self.hex_to_rgb(self.color_labels[5].cget("bg"))
        except Exception as e:
            print("exception: ",e)
            print("[ERROR] Invalid color format. Please pick 3 colors.")
            return

        # Call the image generator
        generate_images(
            phrases=phrases,
            output_folder="set1",
            font_size=48,
            image_size=(800, 250),
            color_shadow_rgb=color_highlight_rgb,
            color_highlight_rgb=color_shadow_rgb,
            color_main_rgb=color_main_rgb
        )
        generate_images(
            phrases=phrases,
            output_folder="set2",
            font_size=48,
            image_size=(800, 250),
            color_shadow_rgb=color_highlight_rgb02,
            color_highlight_rgb=color_shadow_rgb02,
            color_main_rgb=color_main_rgb02
        )
        # Call the specific function for this button
        image_func = self.image_functions[index]
        image_func("set1", "set2","output/"+self.function_name[index],steps=120)
    

    def choose_color(self, label):
        color_code = colorchooser.askcolor(title="Choose a color")[1]
        if color_code:
            label.config(bg=color_code)
            
    def __init__(self):
        
        #config
        # Function list
        self.COLOR_FILE = "colors.json"
        self.PRESET_DIR = "presets"
        os.makedirs(self.PRESET_DIR, exist_ok=True)
        
        self.function_name = [
            "Charging",
            "Floating",
            "Gradient",
            "inverted_Big",
            "Sliding",
            "Sliding_Fade",
            "Sliding_Gradient",
            "Subtitle"
        ]
        
        self.image_functions = [
            blend_images,
            float_animation,
            gradient_transition,
            invertedBig,
            slide_transition,
            slide_transition_with_fade,
            sliding_gradient_transition,
            subtitle,
        ]
        
        # Main window
        root = tk.Tk()
        root.title("Text Editor with Buttons")
        root.geometry("900x800")  # Width x Height

        # Left frame for buttons
        button_frame = tk.Frame(root, width=200)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Right frame for text editor
        text_frame = tk.Frame(root)
        text_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Text area with scroll bar
        text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Arial", 12))
        text_area.pack(expand=True, fill=tk.BOTH)

        # Color selector frame
        
        color_frame = [
                    tk.Frame(text_frame,width=20),
                    tk.Frame(text_frame,width=20)
        ]
        color_frame[0].pack(pady=15)
        color_frame[1].pack(pady=15)

        color_names = [
            "Shadow_set1",
            "Highlight_set1",
            "Main_set1",
            "Shadow_set2",
            "Highlight_set2",
            "Main_set2"
        ]

        self.color_labels = [] 
        for j in range(2):
            for i in range(3):
                label = tk.Label(color_frame[j], text=f"{color_names[j*3+i]}", width=15, height=5, bg="#dddddd")
                label.grid(row=0, column=i, padx=15)
                label.bind("<Button-1>", lambda e, lbl=label: self.choose_color(lbl))
                self.color_labels.append(label)
                
        # Preset controls
        preset_frame = tk.Frame(text_frame)
        preset_frame.pack(pady=5)

        preset_name_var = tk.StringVar()
        preset_entry = tk.Entry(preset_frame, textvariable=preset_name_var, width=20)
        preset_entry.grid(row=0, column=0, padx=5)

        tk.Button(
            preset_frame, text="💾 Save Preset", width=15,
            command=lambda: self.save_preset(preset_name_var.get())
        ).grid(row=0, column=1)

        # Preset dropdown
        self.preset_selector_var = tk.StringVar()
        self.preset_dropdown = tk.OptionMenu(preset_frame, self.preset_selector_var, "")
        self.preset_dropdown.grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            preset_frame, text="📂 Load Preset", width=15,
            command=lambda: self.load_preset(self.preset_selector_var.get())
        ).grid(row=1, column=1)
        
        # Call it once on startup
        self.refresh_preset_menu()
                
        # Create 8 function buttons
        for i in range(8):
            btn = tk.Button(button_frame, text=f"{self.function_name[i]}", width=20, height=2,
                            command=lambda idx=i: self.handle_button_click(idx, text_area))
            btn.pack(pady=5)

        # Start GUI loop
        root.mainloop()

if __name__ == "__main__":
    
    
    app = subtitleApp()