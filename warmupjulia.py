import numpy as np
import matplotlib.pyplot as plt
import random as rn

r1= 1.5
r2 = 0.5
c1 = (0,0)
c2 = (1.2,0)
a = -2
b = 2
c = 0
d = 2
n = 10000
fy = []
fx = []

def circle(r,c): #creates circles 
    x = np.linspace(c[0]-r, c[0]+r, n)
    y = np.sqrt(r**2-(x-c[0])**2)
    return x,y

#calculate intersection point 
x_intersection = (r1**2 - r2**2 + c2[0]**2)/(2*c2[0]) 
y_intersection = np.sqrt(r1**2-x_intersection**2)

#combine both circles into 1 list
for i in range(n):
    x_large = circle(r1, c1)[0][i]
    y_large = circle(r1, c1)[1][i]
    
    if x_large < x_intersection:
        fx.append(x_large)
        fy.append(y_large)

for i in range(n):
    x_small = circle(r2, c2)[0][i]
    y_small = circle(r2, c2)[1][i]
    
    if x_small > x_intersection:
        fx.append(x_small)
        fy.append(y_small)

#calc area using rieman integration
def riemann_sum():
    area = 0
    for i in range(1, n):
        dx = fx[i] - fx[i - 1]  # Width of the rectangle
        rectangle_area = fy[i - 1] * dx  # Area of the rectangle
        area += rectangle_area
    return area
print(riemann_sum())

def monte_carlo():
    points_below_curve = 0
    total_points = 0
    
    for _ in range(n):
        x_random = rn.uniform(a, b)  
        y_random = rn.uniform(c, d)  
        
        if y_random <= fy[int((x_random - a) / (b - a) * n)]:
            points_below_curve += 1
        
        total_points += 1

    # Calculate the estimated area using Monte Carlo method
    total_area = (b - a) * (d - c)
    estimated_area = total_area * (points_below_curve / total_points)
    
    return estimated_area

print(monte_carlo())

#plot everything                 
fig,ax = plt.subplots()
ax.set_xlim(a, b)
ax.set_ylim(c, d)
ax.plot(fx,fy, lw= 2)
ax.set_aspect('equal')
plt.show()