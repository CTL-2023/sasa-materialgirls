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

n = 100


def f(): #red line

    theta = np.linspace(np.pi, 0, n)
    x1 = r1 * np.cos(theta) 
    y1 = r1 * np.sin(theta) 
    x2 = r2 * np.cos(theta) + c2[0]
    y2 = r2 * np.sin(theta)
    fig, ax = plt.subplots()
    x_finish = []
    y_finish = []
    
    counter = 0

    for x_large in x1:
        counter += 1
        for x_small in x2:
            if round(x_large,2) == round(x_small,2):
                print(counter)
                yneu = y1[counter-1]
                y2neu = y2[counter-1]
                if round(yneu,1) == round(y2neu,1):
                   print('kaka')
                   break

    counter = 93
    print('hai',counter)                     
    for i in range(0,counter):
        x_finish.append(x1[i])
        y_finish.append(y1[i])

    for j in range(counter+1,n-1):
        x_finish.append(x2[j])
        y_finish.append(y2[j])

    ax.plot(x_finish, y_finish)
    ax.set_xlim(a, b)
    ax.set_ylim(c, d)
    ax.set_aspect('equal') #aspect ratio to ensure the half-circle appears as a half-circle
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    plt.show()
    #plt.rcParams['figure.max_open_warning'] = 20
    return
print(f())

    

