import numpy as np
import matplotlib.pyplot as plt

r1= 1.5
r2 = 0.5
c1 = (0,0)
c2 = (1.2,0)
a = -2
b = 2
c = 0
d = 2

def f(): #red line

    theta = np.linspace(0, np.pi, 100)
    x1 = r1 * np.cos(theta) 
    y1 = r1 * np.sin(theta) 
    x2 = r2 * np.cos(theta) + c2[0]
    y2 = r2 * np.sin(theta)
    fig, ax = plt.subplots()

    for x in x1:
        if x < c1[0]:
            -r1 == - 1.5
            r2 == 0
        if x > c2[0]:
            r2 == 1.7
            r1 == 0
    else:
        x1 == 0
        x2 == 0

    ax.plot(x1, y1, x2, y2)
    ax.set_xlim(a, b)
    ax.set_ylim(c, d)
    ax.set_aspect('equal') #aspect ratio to ensure the half-circle appears as a half-circle
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    plt.show()
    plt.rcParams['figure.max_open_warning'] = 20
    return
print(f())

    

