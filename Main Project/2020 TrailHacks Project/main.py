# IMPORTS
import tkinter as tk
from svglib.svglib import svg2rlg
from PIL import Image, ImageTk
from reportlab.graphics import renderPM
import pygal
from pygal.style import NeonStyle

#------------------FUNCTIONS
def create_radar(player_name,stats):
    radar_chart = pygal.Radar(width=500,height=400, style=NeonStyle)
    radar_chart.title = 'Comparing Businesses'
    radar_chart.x_labels = ["Customer Service", "Prices", "Popularity", "Product Quality", "Specialty"]
    radar_chart.add(player_name, stats)
    radar_chart.render_to_file("Images/radarchart.svg")

def convert_svg(svg_file):
    file = svg2rlg('Images/' + svg_file)
    renderPM.drawToFile(file,"Images/radarchart.png",fmt="PNG")

def main():
    root = tk.Tk()
    create_radar("Apple",[4,3,5,5,3])
    convert_svg('radarchart.svg')
    main_window = Window(root,'quickStat','600x600')

class Window:
    def __init__(self,root,title,size):
        self.root = root
        self.root.title(title)
        self.root.geometry(size)
        self.bg = '#292424'
        #self.font =


        self.design()
        self.root.mainloop()

    #@staticmethod
    #def load_font():
    #   font = tk.
    def design(self):
        self.root.configure(background=self.bg) # set bg colour on entire window
        tk.Label(self.root, text="Welcome to QuickStat!", background=self.bg).pack()
        tk.Entry(self.root,bd=1).pack()
#----------------------------

main()
