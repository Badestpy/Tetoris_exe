import os
import sys
print("E:\Code\Tetoris", os.getcwd())
import PIL
import pygame
import tkinter as tk
from itertools import count
from PIL import Image, ImageTk
import project_colors

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path, delay=100):
        super().__init__(master, bg='BLACK')
        gif_path = resource_path(gif_path)
        self.gif = Image.open(gif_path) # FIXED: overwrite gif_path with full path
        self.frames = []
        self.delay = delay


        try:
            for frame in count(1):
                self.frames.append(ImageTk.PhotoImage(self.gif.copy()))
                self.gif.seek(frame)
        except EOFError:
            pass # End of sequence

        
        self.index = 0
        self.update_frame()


    def update_frame(self):
        if self.frames:
            self.config(image=self.frames[self.index])
            self.index = (self.index + 1) % len(self.frames)
            self.after(self.delay, self.update_frame)


# create main window
root = tk.Tk()
root.title("Tetoris")
root.geometry("400x400") # this is the resolution I want, don't question me
root.resizable(False, False) # Lock window size
root.configure(bg='BLACK') # window background


# Display the GIF
gif_label = AnimatedGIF(root, "tetoris.gif", delay=100)
gif_label.pack(expand=True)


# Initialize pygame mixer to play background music
pygame.mixer.init()
music_path = resource_path("tetoris_bit_crushed_midi.mp3")
pygame.mixer.music.load("tetoris_bit_crushed_midi.mp3")
pygame.mixer.music.play(loops=-1) # loops indefinitly

# Pause/resume music on window minimize/restore
def pause_music(event=None):
    pygame.mixer.music.pause()

def resume_music(event=None):
    pygame.mixer.music.unpause()

root.bind("<Unmap>", pause_music)
root.bind("<Map>", resume_music)


# Start the program
root.mainloop()
