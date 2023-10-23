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
n = 1000


def circle(r,c):
    x = np.linspace(c[0]-r, c[0]+r, n)
    y = []
    for value in x:
        y.append(np.sqrt(r**2-(value-c[0])**2))
    return (x,y)





no_match = True
counter = 0
while no_match:
    for x_large in circle(r1,c1)[0]:
        counter += 1
        for x_small in circle(r2,c2)[0]:
            if  np.isclose(x_large, x_small, rtol=1e-1, atol=1e-5):
                print(counter)
                y1 = circle(r1,c1)[1]
                y2 = circle(r2,c2)[1]
                if np.isclose(y1[counter - 1], y2[counter - 1], rtol=1e-1, atol=1e-5):
                    no_match = False




'''
statement = False
counter = 0
for x_large in circle(r1,c1)[0]:
    counter += 1
    for x_small in circle(r2,c2)[0]:
        if np.isclose(x_large, x_small, rtol=1e-3, atol=1e-5):
            print(counter)
            y1 = circle(r1,c1)[1]
            y2 = circle(r2,c2)[1]
            if p.isclose(y1[counter - 1], y2[counter - 1], rtol=1e-1, atol=1e-5):
                statement = True
                
    if statement:
        break           
                
print(counter)
'''

'''
fig,ax = plt.subplots()
ax.set_xlim(a, b)
ax.set_ylim(c, d)
ax.scatter(circle(r1,c1)[0], circle(r1,c1)[1]) 
ax.scatter(circle(r2,c2)[0], circle(r2,c2)[1])

ax.set_aspect('equal') 
plt.show()
'''

