"""
    Quantitative graphics drawer
    Author: Faceless Creator

    Далее на русском

    ОПИСАНИЕ:
    Скрипт используется для отображения количественных графиков измерений. 
    Точки графика берутся из указанного файла. 
    Редактируйте настройки как вам вздумается.
    
    НАСТРОЙКА:
    Настройте виртуальное окружение и установите matplotlib. В случае с Linux также установите пакет tk для отрисовки окон
"""

# ---------
# LIBRARIES
# ---------

import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, pi
import shutil
import os

# --------
# SETTINGS
# --------

save_folder = 'images'

window_size = [6.4, 6.4] # window size in ??? [x, y]

main_graph_style = '-r' # style of main graphic; view pyplot.plot
row_graph_style = '-b' # style of row graphic

x_main_tick_period = 1 # period between X main ticks
x_sub_ticks = 2 # count of sub ticks for each x main tick
y_main_tick_period = 0.5 # period between Y main ticks
y_sub_ticks = 2 # count of sub ticks for each y main tick

trigcount_func_start = 1
trigcount_func_end = 10
def getTrigcount(i):
    return i

xmin = -3
xmax = 3
xcount = 100 # count of points for graphic

def func(x):
    """# classic
    if x>=0 and x<2:
        return 1
    else:
        return 2-x
    """
    
    # sin
    if x >=-3 and x<=-2:
        return -x-2
    elif x>-2 and x< 0:
        return -1
    elif x>=0 and x<2:
        return 1
    else:
        return 2-x
    
    """ # cos
    if x >=-3 and x<=-2:
        return x+2
    elif x>-2 and x<2:
        return 1
    else:
        return 2-x
    """

#a0 = 1/2 # classic
a0 = 0 # sin
# a0 = 1/2 # cos
def getA(m):
    #return sin(2*pi*m/3)/pi/m - 3/m/m/pi/pi*(-1)**m + 3/m/m/pi/pi*cos(2*m*pi/3) # classic
    return 0 # sin
    #return -2*sin(m*pi/2)/m/pi - 12*cos(m*pi/2)/m/m/pi/pi + 12*cos(m*pi/3)/m/m/pi/pi + 2*sin(m*pi/3)/m/pi # cos
def getB(m):
    #return + 1/m/pi + 1/m/pi*(-1)**m - cos(2*pi*m/3)/m/pi + 3/m/m/pi/pi*sin(2*pi*m/3) # classic
    return 2*cos(m*pi/2)/m/pi + 12*sin(m*pi/3)/m/m/pi/pi - 12*sin(m*pi/2)/m/m/pi/pi + 2/m/pi - 2*cos(m*pi/3)/m/pi # sin
    #return 0 # cos

# -------
# PROGRAM
# -------

os.system("rm -rf {}/*.png".format(save_folder))
os.system("mkdir -p {}".format(save_folder))

width = xmax-xmin

# generate function
X = np.arange(xmin, xmax, width/xcount)
Y = []
for x in X:
    Y.append(func(x))

# set window
fig = plt.figure(figsize=window_size)
ax = fig.add_subplot(111)

# generate ticks
x_major_ticks = np.arange(min(X) // x_main_tick_period * x_main_tick_period, (max(X) // x_main_tick_period + 1) * x_main_tick_period, x_main_tick_period)
x_minor_ticks = np.arange(min(X) // x_main_tick_period * x_main_tick_period, (max(X) // x_main_tick_period + 1) * x_main_tick_period, x_main_tick_period/x_sub_ticks)
y_major_ticks = np.arange(min(Y) // y_main_tick_period * y_main_tick_period, (max(Y) // y_main_tick_period + 1) * y_main_tick_period, y_main_tick_period)
y_minor_ticks = np.arange(min(Y) // y_main_tick_period * y_main_tick_period, (max(Y) // y_main_tick_period + 1) * y_main_tick_period, y_main_tick_period/y_sub_ticks)
# set ticks
ax.set_xticks(x_major_ticks)
ax.set_xticks(x_minor_ticks, minor=True)
ax.set_yticks(y_major_ticks)
ax.set_yticks(y_minor_ticks, minor=True)

# graw graphs
ax.plot(X, Y, main_graph_style)

# set grid
# почему-то сразу две сетки не включаются. Сетку нужно активировать ПОСЛЕ ПОСТРОЕНИЯ ГРАФИКОВ
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

# generate all the images
for trigcount_i in range(trigcount_func_start, trigcount_func_end+1):
    trigcount = getTrigcount(trigcount_i)
    # generate row
    A = []
    B = []
    A.append(a0)
    B.append(0)
    for i in range(1,trigcount+1):
        A.append(getA(i))
        B.append(getB(i))
    # calc points
    Yrow = []
    for x in X:
        yrow = A[0]/2
        for i in range(1, trigcount+1):
            yrow += A[i]*cos(x*i*pi/width) + B[i]*sin(x*i*pi/width)
        Yrow.append(yrow)
    # draw ir
    ax.plot(X, Yrow, row_graph_style)
    plt.savefig('{}/image{}.png'.format(save_folder, trigcount_i))
    ax.lines.pop(1)

# generate GIF
cmd = 'convert {}/image%01d.png[{}-{}] result.gif'
cmd = cmd.format(save_folder, trigcount_func_start, trigcount_func_end)
os.system(cmd)
