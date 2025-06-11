import tkinter as tk

class Trans:
    def __init__(self, master_window, initial_alpha, save_callback):
        self.main_window = master_window
        self.save_callback = save_callback
        self.root = tk.Toplevel(master_window)
        self.root.title("투명도 조절기")
        self.root.geometry("300x180")

        self.slide_label = tk.Label(self.root, text=f"투명도: {round(initial_alpha, 2)}")
        self.slide_label.pack(pady=5)

        self.slide_bar = tk.Scale(self.root, from_=0.1, to=1.0, resolution=0.01,
                                  orient=tk.HORIZONTAL, command=self.slide)
        self.slide_bar.set(initial_alpha)
        self.slide_bar.pack(pady=5)

        self.save_btn = tk.Button(self.root, text="적용", command=self.save_transparency)
        self.save_btn.pack(pady=5)

    def slide(self, val):
        self.slide_label.config(text=f"투명도: {round(float(val), 2)}")

    def save_transparency(self):
        alpha = round(self.slide_bar.get(), 2)
        self.save_callback(alpha)
        self.root.destroy()

    def toggle_transparency(self):
        current_alpha = self.main_window.attributes('-alpha')
        new_alpha = 0.5 if current_alpha == 1.0 else 1.0
        self.main_window.attributes('-alpha', new_alpha)
        self.slide_bar.set(new_alpha)
        self.slide_label.config(text=f"토글됨: {round(new_alpha, 2)}")
