
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt 
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from tkinter import ttk

fig = plt.figure(figsize=(12,9))

window=tk.Tk()
window.wm_title("Map Displayer")
window.columnconfigure(0, weight=1)

p_info = tk.LabelFrame(window, text='Longitude and latitude setting')
p_info.grid(sticky=(tk.W + tk.E))
for i in range(2):
  p_info.columnconfigure(i, weight=1 )

latitude_variable = tk.DoubleVar()
tk.Label(p_info, text="Latitude").grid(row=2, column=0)
tk.Spinbox(
    p_info, textvariable=latitude_variable,
    from_=0, to=250, increment=0.0001,
).grid(row=1, column=0, sticky=(tk.W + tk.E))

longitude_variable = tk.DoubleVar()
tk.Label(p_info, text="Longitude").grid(row=2, column=1)
tk.Spinbox(
    p_info, textvariable=longitude_variable,
    from_=0, to=250, increment=0.0001,
).grid(row=1, column=1, sticky=(tk.W + tk.E))

zoom_info = tk.LabelFrame(window, text='Longitude and latitude setting')
zoom_info.grid(sticky=(tk.W + tk.E))
for i in range(2):
  zoom_info.columnconfigure(i, weight=1 )

zoom_list = ["10","1","0.01","0.001","0.00075"]

zoom_variable = tk.StringVar()
ttk.Label(zoom_info, text='Zoom').grid(row=2, column=0)
ttk.Combobox(
  zoom_info,
  textvariable=zoom_variable,
  values=zoom_list
).grid(row=3, column=0, sticky=(tk.W + tk.E))

map_type_list = ["Map","Satellite Photo"]

map_type_variable = tk.StringVar()
ttk.Label(zoom_info, text='Map Type').grid(row=2, column=1)
ttk.Combobox(
  zoom_info,
  textvariable=map_type_variable,
  values=map_type_list
).grid(row=3, column=1, sticky=(tk.W + tk.E))

reload_button_frame = tk.LabelFrame(window, text='Reload button')
reload_button_frame.grid(sticky=(tk.W + tk.E))

for i in range(3):
  reload_button_frame.columnconfigure(i, weight=1 )

tk.Label(reload_button_frame , text='Click Reload button to refresh the map after setting changes').pack(side=tk.TOP)
Reload_button = tk.Button(reload_button_frame, text='RELOAD')
Reload_button.pack(side=tk.LEFT)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().grid(row=7, column=0, sticky=(tk.W + tk.E))

def on_reset():

    latitude_variable_value = float(latitude_variable.get())
    longitude_variable_value = float(longitude_variable.get())
    zoom_variable_value = float(zoom_variable.get())
    map_type_variable_value = map_type_variable.get()
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=7, column=0, sticky=(tk.W + tk.E))

    if map_type_variable_value == "Map":

        osm_img = cimgt.OSM()
        ax1 = plt.axes(projection=osm_img.crs)
        image = osm_img

    elif map_type_variable_value == "Satellite Photo":

        QuadtreeTiles_img = cimgt.QuadtreeTiles()
        ax1 = plt.axes(projection=QuadtreeTiles_img.crs)
        image = QuadtreeTiles_img

    center_pt = [latitude_variable_value, longitude_variable_value]
    zoom = zoom_variable_value
    extent = [center_pt[1]-(zoom*2.0),center_pt[1]+(zoom*2.0),center_pt[0]-zoom,center_pt[0]+zoom]
    ax1.set_extent(extent)
    
    scale = np.ceil(-np.sqrt(2)*np.log(np.divide(zoom,350.0)))
    scale = (scale<20) and scale or 19
    ax1.add_image(image, int(scale))

Reload_button.configure(command=on_reset)

tk.mainloop()















