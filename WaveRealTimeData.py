#!/usr/bin/env python3

'''Matplotlib'''
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation

'''tkinter'''
import tkinter as tk
from tkinter import messagebox as MessageBox

'''Tools'''
import time
import serial
import RPi.GPIO as GPIO
import os

global tmax

MAXPTS = 50
trigger = 23
echo = 24
##GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

yv = []
tv = []
sound_speed = 343000  # cm/s


#fig = plt.figure()
#ax = plt.axes(ylim=(0, 80))
#line, = ax.plot([],[],lw=2)
f = Figure(figsize=(12,10), dpi=100)
a = f.add_subplot(111)
a.set_title('Gráfico 1')
a.set_xlabel('Tiempo (s)')
a.set_ylabel('Distancia (cm)')
a.grid(True)
style.use("ggplot")

def formato_excel(t, x, yMAX,yMIN):
    nombre_csv = 'data_waves '
    datetime = time.strftime("%d-%b-%Y %I:%M:%S%p")
    formato='.csv'
    file = open(nombre_csv+datetime+formato, "w")
    i = 0
    file.write("Tiempo,Distancia\n")
    for i in range(len(t)):
        file.write(str(t[i])+","+str(x[i])+"\n")
        file.flush()
    file.write("/////////////////,/////////////////"+"\n")
    file.write("Maximo:,"+str(yMAX)+"\n")
    file.write("Minimo:,"+str(yMIN)+"\n")
    file.write("Altura de la ola:,"+str(Height)+"\n")
    file.write("Periodo:,"+str(Period)+"\n")
    file.write("Frecuencia:,"+str(Hz)+"\n")
    
    file.close()

def distance():
    global t0_0
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    t0 = time.time()
    tf = time.time()

    while GPIO.input(echo)==0:
        t0 = time.time()
    while GPIO.input(echo)==1:
        tf = time.time()

    time_elapsed = tf - t0
    d = (time_elapsed*sound_speed)/2
    return [(tf+t0)/2 - t0_0, d/10]

def Max_Min(t,y):
    global Height,Period,Hz
    Max = y.index(max(y))	
    Min = y.index(min(y))

    texto2.config(state="normal")
    texto2.delete('1.0', tk.END)

    texto2.insert(tk.INSERT, "Màximo\t\t: {0:.3f}cm\n".format(y[Max]))
    texto2.insert(tk.INSERT, "Mìnimo\t\t: {0:.3f}cm\n".format(y[Min]))
    #print ("Maximo: {}, Minimo: {}".format(y[Max],y[Min]))
    Height = y[Max] - y[Min]
    texto2.insert(tk.INSERT, "Altura de\n".format(Height))
    texto2.insert(tk.INSERT, "la ola\t\t: {0:.3f}cm\n".format(Height))
    #print ("Altura de la ola: {}".format(Height))
    tiempo = t[Max]
    k = 0
    while True:
        if y[Max + k] - y[Max + k + 1] < 0:
            tiempo2 = t[Max + k]
            break
        k += 1
   
    #texto2.insert(tk.INSERT, "Tiempo2: {0:.3f}s\n".format(tiempo2))
    #texto2.insert(tk.INSERT, "Tiempo1: {0:.3f}s\n".format(tiempo))
    #print ("tiempo2: {} Tiempo : {}".format(tiempo2,tiempo))
    Period = (tiempo2 - tiempo)*2
    Hz = 1/Period
    texto2.insert(tk.INSERT, "Periodo\t\t: {0:.3f}s\n".format(Period))
    #print ("Periodo: {}".format(Period))
    texto2.insert(tk.INSERT, "Frecuencia\t\t: {0:.3f}Hz".format(Hz))
    #print ("Frecuencia: {}".format(Hz))
    texto2.config(state="disabled")
        
    return y[Max],y[Min]

def animate(i):
    global tv,yv
    a.clear()
    a.set_title('Gráfico Tiempo vs Distancia')
    a.set_xlabel('Tiempo (s)')
    a.set_ylabel('Distancia (cm)')
    a.plot(tv,yv)
    canvas.draw()


def toInt():
    global t0_0
    tmax = n1.get()
    y_data = []
    t_data = []
    texto.config(state="normal")
    texto.delete('1.0', tk.END)
    texto.insert(tk.INSERT,"Tiempo\tDistancia\n(s)\t(cm)")
    t0_0=time.time()
    j = 0
    while True:
        j += 1
        dist = distance()
        y_data.append(dist[1])
        t_data.append(dist[0])
        a.clear()
        a.set_title('Gráfico Tiempo vs Distancia')
        a.set_xlabel('Tiempo (s)')
        a.set_ylabel('Distancia (cm)')
        a.grid(True)
        #a.set_xlim(0,tmax)
        a.plot(t_data,y_data)
        canvas.draw()
        if dist[0] > tmax:
            break
        texto.config(state="normal")
        texto.insert(tk.INSERT,"\n{0:.3f}".format(dist[0]))
        texto.insert(tk.INSERT,"\t{0:.3f}".format(dist[1]))
        texto.config(state="disabled")
        time.sleep(0.05)

        
        '''Other functions'''
    [yMAX,yMIN] = Max_Min(t_data,y_data)
    formato_excel(y_data, t_data, yMAX, yMIN)
    a.clear()
    a.set_title('Gráfico Tiempo vs Distancia')
    a.set_xlabel('Tiempo (s)')
    a.set_ylabel('Distancia (cm)')
    a.grid(True)
    #a.set_xlim(0,tmax)
    a.plot(t_data,y_data)
    canvas.draw()
        #MessageBox.showerror("Error!","Solo se permiten numeros desde 1 al 120")
    #toolbar = NavigationToolbar2TkAgg(canvas)
    #toolbar.update()
    #canvas._tkcanvas.pack()
    

if __name__ == "__main__":
    
    '''Tkinter config'''
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h-65))
    #root.state('zoomed')
    root.title("Proyecto Generador de Olas")
    root.resizable(0,0)
    #root.tk.call('wn','iconbitmap',root._w,'/home/pi/images/wave.ico')

    '''Labels and buttons'''
    n1 = tk.IntVar()
    
    fm1 = tk.Frame(root)
    step = tk.LabelFrame(fm1, text="Opciones")
    step.grid(row=0,column=0,padx=10,pady=10)
    

    label = tk.Label(step, text="¿Cuàntos segundos debe medir el programa?")
    label.pack()
    spinbox = tk.Spinbox(step, from_=1, to=120, wrap=True, textvariable=n1)
    spinbox.pack()
    button = tk.Button(step,text="Go!",command=toInt)
    button.pack()

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
   

    
    fm2 = tk.Frame(root)

    fm3 = tk.LabelFrame(fm2, text="Datos")
    fm3.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    texto = tk.Text(fm3, width=20)
    scr = tk.Scrollbar(fm3, orient=tk.VERTICAL, command=texto.yview, width=10)
    scr.pack(side=tk.RIGHT, fill=tk.Y)
    texto.pack(side=tk.RIGHT, fill=tk.Y)

    fm4 = tk.LabelFrame(fm2, text="Info extra")
    fm4.grid(row=1, column=1, padx=10, pady=10)

    texto2 = tk.Text(fm4, width=30)
    texto2.pack(side=tk.RIGHT, fill=tk.Y)
    

    #fm1.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    #fm2.grid(row=0, column=1,padx=10,pady=10)
    #canvas.get_tk_widget().grid(row=0,column=2)
    fm1.pack(side=tk.LEFT,fill=tk.BOTH)
    fm2.pack(side=tk.LEFT,fill=tk.BOTH)
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
    
    
    

    texto.insert(tk.INSERT,"Tiempo\tDistancia\n(s)\t(cm)")
    texto.config(yscrollcommand=scr.set)
    
    texto2.insert(tk.INSERT,"Màximo\t\t:\n")
    texto2.insert(tk.INSERT,"Mìnimo\t\t:\n")
    texto2.insert(tk.INSERT,"Altura de\n")
    texto2.insert(tk.INSERT,"la ola\t\t:\n")
    texto2.insert(tk.INSERT,"Periodo\t\t:\n")
    texto2.insert(tk.INSERT,"Frecuencia\t\t:\n")
    
    #PlotData(t_data,y_data)

    '''End of root'''
    root.mainloop()

