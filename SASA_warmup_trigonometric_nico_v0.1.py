'''
The area under the two conjoined semi-circles and their arc length are calculated using trigonometry. For the area, the area of the 
triangle connecting the circle centers and the circle contact point is calculated first (black triangle in the plot). Secondly, the 
areas of the circle sectors that aren't part of the triangle are calculated using the angle of the according triangle vertex.

The arc length is calculated using a similar approach, adding the according parts of the circumference together, given by the 
previosly calculated angles.
'''

import math
from matplotlib import pyplot as plt
pi = math.pi

# Initialize circles [x-Position, radius]
circle_1, circle_2 = [0, 1.5], [1.2, 0.5]
x_range, y_range = [-2, 2], [0, 2]

r_1, r_2 = circle_1[1], circle_2[1]
x_1, x_2 = circle_1[0], circle_2[0]

def calculations():
    # Calculate the area and the height of the triangle made by the two circle centers and the contact point of the two circles
    triangle_base = x_2 - x_1

    # Calculate triangle area using Heron's formula
    s = (r_1 + r_2 + triangle_base) / 2
    triangle_area = math.sqrt(s * (s - r_1) * (s - r_2) * (s - triangle_base))

    #calculate (x, y) coordinates of  the contact point of the two circles (contact_point, height)
    height = 2 * triangle_area / triangle_base
    contact_point = math.sqrt(r_1**2 - height**2) + x_1

    # Calculate the angles of the triangle
    phi_1, phi_2 = math.asin(height/r_1), math.asin(height/r_2)

    # Calculate the area under the two half circles
    circles_area = r_1**2 * (pi - phi_1)/2 + r_2**2 * (pi - phi_2)/2 + triangle_area

    # Calculate the arc length of the two half circles
    arc_length = r_1 * (pi - phi_1) + r_2 * (pi - phi_2)

    return circles_area, arc_length, height, contact_point

def function_list(radius, center):
    steps = 1000
    start_point = center - radius
    x, y = [], []

    for i in range(steps+1):
        x_value = start_point + 2 * i * radius / steps
        y_value = math.sqrt(radius**2 - (x_value - center)**2)
        x.append(x_value)
        y.append(y_value)

    return x, y


def plot():
    x_plot, y_plot = function_list(r_1, x_1)
    plt.plot(x_plot, y_plot, color='r', label='circle 1')
    x_plot, y_plot = function_list(r_2, x_2)
    plt.plot(x_plot, y_plot, color='b', label='circle 2')

    plt.scatter(contact_point, height, color='black', marker='o', label='contact point')
    plt.scatter(x_1, 0, color='black', marker='o', label='center 1')
    plt.scatter(x_2, 0, color='black', marker='o', label='center 2')
    
    plt.plot([x_1, contact_point, x_2, x_1], [0, height, 0, 0], color='black', label='triangle')
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(x_range)
    plt.ylim(y_range)
    plt.show()


circles_area, arc_length, height, contact_point = calculations()
print(f'The area is {circles_area}, the arc length is {arc_length}.')
plot()