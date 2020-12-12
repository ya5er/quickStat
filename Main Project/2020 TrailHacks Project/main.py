# IMPORTS
import tkinter as tk
from tkinter.font import Font
from svglib.svglib import svg2rlg
from PIL import Image, ImageTk
from reportlab.graphics import renderPM
import pygal
from pygal.style import NeonStyle
import requests
from bs4 import BeautifulSoup, Comment

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
    main_window = Window(root,'quickStat','800x500')

def oei(ts, ast, orb, tov):
    num = ((ts * 30) + ast + (orb * 2) - tov) * 2
    return num

def pgp(ts, e2, e1):
    num2 = ((ts*100) - (e2 + e1)) * 100
    return num2

class Window:
    def __init__(self,root,title,size):
        self.root = root
        self.root.title(title)
        self.root.geometry(size)
        self.root.resizable(0,0)
        self.gray = '#292424'
        self.orange = '#E68422'
        self.font = Font(family="MS Reference Sans Serif", size=40, weight="bold", slant="italic")
        self.font2 = Font(family="MS Reference Sans Serif",size=16, weight="bold", slant="italic")

        self.design()
        self.root.mainloop()

    def handle_focus_in(self,_):
        self.search_bar.delete(0, tk.END)
        self.search_bar.config(fg='black')

    def handle_focus_out(self,_):
        self.search_bar.delete(0, tk.END)
        self.search_bar.config(fg='grey')
        self.search_bar.insert(0, "Search for players, eg. Kawhi Leonard")

    def handle_enter(self,txt):
        self.player_name = self.search_bar.get()
        second_window = New_Window(self.player_name,self.root,'800x500','Database Information')
        self.root.withdraw()

    def design(self):
        self.root.configure(background=self.gray) # set bg colour on entire window
        tk.Label(self.root, text="quickStat", background=self.gray, fg=self.orange, font=self.font).pack(pady=(100,35))
        self.search_bar = tk.Entry(self.root,bd=1,width=75, fg='grey')
        self.search_bar.pack(ipady=10)
        self.search_bar.insert(0,"Search for players, eg. Kawhi Leonard")
        self.search_bar.bind("<FocusIn>",self.handle_focus_in)
        self.search_bar.bind("<FocusOut>",self.handle_focus_out)
        self.search_bar.bind("<Return>",self.handle_enter)

        tk.Label(self.root, text="The simplest, most relevant basketball database out there", background=self.gray, fg=self.orange, font=self.font2).pack(pady=(35,0))

class New_Window(): # inherit from main window
    def __init__(self,player_name,root,size,title):
        self.player_name = player_name
        self.new_window = tk.Toplevel(root)
        self.new_window.title(title)
        self.new_window.geometry(size)
        self.new_window.resizable(0,0)
        self.gray = '#292424'
        self.orange = '#E68422'
        self.player_stats = self.fetch_player_stats(player_name)
        self.font = Font(family="MS Reference Sans Serif", size=30, weight="bold")
        self.font2 = Font(family="MS Reference Sans Serif", size=10, weight="bold")
        self.design()

    def fetch_player_stats(self, player_name):
        name = player_name.split()
        if not len(name[1]) <= 5:
            name[1] = name[1][:5]
        name[0] = name[0][:2]
        add_to_url = name[1] + name[0] + "01.html"
        url = "https://www.basketball-reference.com/players/" + name[1][0] + "/" + add_to_url

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        tagName = 'table'
        className = 'row_summable sortable stats_table now_sortable'
        idName = "per_game"
        result = soup.find(tagName, id=idName)

        tagName = 'tbody'
        result = soup.find(tagName)
        per_game_stats = result.find_all()

        statList = []
        for stat in per_game_stats:
            statList.append(stat.getText(separator=' '))

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        tfoots = []
        for comment in comments:
            comment = BeautifulSoup(str(comment), 'html.parser')
            tfoot = comment.find('tfoot')
            if tfoot:
                tfoots.append(tfoot)

        advanced_stats = tfoots[3].getText(separator=' ').split()
        print(advanced_stats)

        ts_percent = advanced_stats[5]
        ast_percent = advanced_stats[11]
        orb_percent = advanced_stats[8]
        tov_percent = advanced_stats[14]

        ppg = statList[-1]
        ast = statList[-6]
        trb = statList[-7]
        efg1 = statList[-83]
        efg2 = statList[-13]
        self.radarstats = [ppg, ast, trb, oei(ts_percent, ast_percent, orb_percent, tov_percent), pgp(ts_percent, efg2, efg1)]

    def design(self): # configure the second window
        self.new_window.configure(background=self.gray)
        title = tk.Label(self.new_window, text=self.player_name, background=self.gray, fg=self.orange, font=self.font)

        open_img = Image.open('Images/radarchart.png')
        open_img = open_img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(open_img)
        picture = tk.Label(self.new_window, image=img)
        picture.photo = img
        info = tk.Message(self.new_window,text="Kawhi Anthony Leonard (/kəˈwaɪ/, born June 29, 1991) is an American professional basketball player for the Los Angeles Clippers of the National Basketball Association (NBA). He played two seasons of college basketball for the San Diego State Aztecs and was named a consensus second-team All-American as a sophomore.", background=self.gray, fg=self.orange, font=self.font2)
        stats = tk.Message(self.new_window,text="Pts Per Game: 18.57\nRebounds Per Game: 8.9\nAssists Per Game: 5.2\nOEI Rating: 92.45\nPGP Rating: 34.21", background=self.gray, fg=self.orange, font=self.font2)

        title.grid(row=0, column=1, pady=10, columnspan=2,sticky="N") # place title
        info.grid(row=1,column=0, sticky="E") # place info
        picture.grid(row=1,column=1,sticky="E") # place radar chart
        stats.grid(row=2,column=0,columnspan=2)


#----------------------------

main()
