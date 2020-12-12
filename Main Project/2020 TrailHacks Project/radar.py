import pygal
from pygal.style import Style, DarkStyle

def create_radar():
    radar_chart = pygal.Radar(width=500,height=400, style=DarkStyle)
    radar_chart.title = 'Comparing Businesses'
    radar_chart.x_labels = ["Customer Service", "Prices", "Popularity", "Product Quality", "Specialty"]
    radar_chart.add('Apple', [4,3,5,5,3])
    radar_chart.render_to_file("Images/radarchart.svg")