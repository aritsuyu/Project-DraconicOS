import tkinter as tk
from PIL import Image, ImageTk

class PetAndando:
    def __init__(self, root, scale=0.3):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 1.0)

        # image
        self.img = Image.open("Engine/Chibi/template.png")
        w, h = self.img.size
        self.img = self.img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(self.img)

        self.canvas = tk.Canvas(root, width=self.img.width, height=self.img.height,
                                highlightthickness=0, bd=0, bg="white")
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")

        # speed & xy
        self.x, self.y = 100, 100
        self.dx, self.dy = 3, 2

        self.being_dragged = False

        # start
        self.move()

        # Drag
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

    def move(self):
        if not self.being_dragged:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()

            self.x += self.dx
            self.y += self.dy

            # LG effect
            if self.x < 0 or self.x + self.img.width > sw:
                self.dx *= -1
            if self.y < 0 or self.y + self.img.height > sh:
                self.dy *= -1

            self.root.geometry(f"+{self.x}+{self.y}")

        self.root.after(30, self.move)

    def start_drag(self, event):
        self.being_dragged = True

    def drag(self, event):
        self.x = self.root.winfo_pointerx() - self.img.width // 2
        self.y = self.root.winfo_pointery() - self.img.height // 2
        self.root.geometry(f"+{self.x}+{self.y}")

    def stop_drag(self, event):
        self.root.after(1000, self.resume_moving)

    def resume_moving(self):
        self.being_dragged = False

if __name__ == "__main__":
    root = tk.Tk()
    pet = PetAndando(root, scale=0.3)
    root.mainloop()
