import tkinter as tk
from tkinter import messagebox

class Memo:
    def __init__(self, root):
        self.memo_mode = False
        self.memo_values = [[None for _ in range(9)] for _ in range(9)]
        self.entries = None
        self.root = root

    def set_entries(self, entries):
        self.entries = entries

    def toggle_memo_mode(self, event=None):
        if self.entries is None:
            return

        self.memo_mode = not self.memo_mode
        messagebox.showinfo("메모 모드",
                            "메모 모드가 활성화되었습니다!" if self.memo_mode
                            else "메모 모드가 비활성화되었습니다!")

        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                if entry['state'] == "readonly":
                    continue

                if self.memo_mode:
                    val = self.memo_values[i][j]
                    if val is not None and val.strip() != "":
                        entry.delete(0, tk.END)
                        entry.insert(0, val)
                        entry.config(fg="gray")
                #else:
                    #entry.delete(0, tk.END)
                    # entry.config(fg="black")

    def handle_input(self, i, j):
        if self.entries is None:
            return

        entry = self.entries[i][j]
        if entry['state'] == "readonly":
            return

        val = entry.get().strip()
        print(f"Cell ({i},{j}) 입력값: '{val}'")
        if self.memo_mode:
            if val:
                self.memo_values[i][j] = val
                entry.config(fg="gray")
            else:
                self.memo_values[i][j] = None
        else:
            self.memo_values[i][j] = None
            entry.config(fg="black")

