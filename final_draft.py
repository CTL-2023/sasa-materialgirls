import csv
import random
import math
import matplotlib.pyplot as plt
import secrets
import string
import sys
ax = plt.subplots()[1]
pi = math.pi

file_directory = "/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/" # Include your directory here 
csv_name = "coordinates.csv" # Choose your csv output file name here (as separators, use / for mac, \\ for pc)

def generate_system(N, D, file_directory, csv_name):
    '''
    Creates a 'coordinates.csv' file in the given directory with D columns and N rows. 
    Entries are random floats between 0 and 1, which act as the center points of the circular/spherical particles
    in the 1x1-square/1x1x1-cube. Finally, it prints if the process was succesful, otherwise it raises an error.

    Args:
        N: Number of lines in csv / Number of center points
        D: Number of columns in csv / Number of dimensions in our simulation
        file_directory: Directory of saved csv-file
        csv_name: File name
    
    Returns:
        Nothing: Saves generated CSV file in desired location and prints success prompt or prints error message
    
    Example:
        >>> generate_system(3, 100, "/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/", "coordinates.csv")
        CSV file '/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/coordinates.csv' with 100 columns 
        and 3 rows has been created.
    '''

    output_file = f"{file_directory}{csv_name}"  # Defines the filepath and -name of the output file

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')

        # Generate and write random numbers to the CSV file
        if D == 3:
            for _ in range(N):
                row = [random.random(), random.random(), random.random()]
                writer.writerow(row)
        elif D == 2:
            for _ in range(N):
                row = [random.random(), random.random()]
                writer.writerow(row)
        else:
            print('Error! D must be either 2 or 3.')
            sys.exit(1)

    print(f"CSV file '{output_file}' with {D} columns and {N} rows has been created.\n")

def read_csv_file(file_directory, csv_name):
    '''
    Reads the 'coordinates.csv'-file in the given directory and returns a nested list 'coordinates' with N entries, 
    which each further contain D entries. Also returns D and N.

    Args: 
        file_directory: Directory of read csv-file
        csv_name: File name

    Returns:
        If file exists and D is 2 or 3:
            tuple: A tuple containing the following values:
                int: N
                int: D
                list: coordinates
        Else:
            Nothing: Prints error message

    Example:
        >>> read_csv_file("/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/", "coordinates.csv")
        (3, 2, [[1, 0], [0.5, 0.7], [0.9, 0.2]])
    '''
    file_path = f"{file_directory}{csv_name}"
    coordinates = [] # Initializes output list

    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=' ')
            for row in reader:
                # Convert each value to float and append to the row list
                float_row = [float(value) for value in row]
                coordinates.append(float_row)

        N, D = len(coordinates), len(coordinates[0])

        if D not in [2, 3]:
            print('Error! D must be either 2 or 3.\n')
            sys.exit(1)
        else:
            return N, D, coordinates
    except FileNotFoundError:
        print(f"File not found: {file_path}\n")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}\n")
        return None

def estimate_volume_fraction(N, R, S, D, coordinates):
    '''
    Returns the volume/area-fraction of the randomly distributed particles with radius R in the 1x1-square, 
    depending whether it's a 1D- or 2D-system.
    The 2D-approach is analogous to the 3D one, and they could probably be generalized into one approach.

    Args:
        N: Number of particles
        R: Radius of particles
        S: Number of randomized 'shots' in the Monte-Carlo-approach
        D: Dimension of system
        coordinates: List of points of the particle centers, N entries which each contain D other entries
        
    Returns: 
        float: Volume/Area fraction of the overlapping particles in the 1x1(x1) grit (between 0 and 1)
    
    Example:
        >>> estimate_volume_fraction(2, 0.2, 1000, 2, [[0, 0.5], [0.5, 0.8]])
        0.25132
    '''
    inside_sphere = 0 # Initializes number of shots inside the sphere
   
    if D == 3: # For 3D-systems
        for _ in range(S): # Executes the following part S times
            test = [random.random(), random.random(), random.random()] # Generates a random 'shot' into the 1x1x1 cube

            for j in range(N): # Iterates over every particle inside 'coordinates'
                dx = abs(test[0] - coordinates[j][0]) # Measures difference of shot and particle center point in x-direction
                dy = abs(test[1] - coordinates[j][1]) # y-direction
                dz = abs(test[2] - coordinates[j][2]) # z-direction

                '''
                Apply periodic boundary conditions
                The cube side length is 1, so take the shortest route between particle center and shot, which is dx if not 
                going through the border and 1-dx if going through the border
                '''
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)
                dz = min(dz, 1 - dz)

                distance_squared = dx**2 + dy**2 + dz**2 # Apply Pythagoras to calculate the square of the total distance 
                                                        #  between particle and shot.

                if distance_squared <= R**2: # If the squared distance is smaller than the squared particle radius, 
                                            #  increase number of points inside the sphere by one
                    inside_sphere += 1
                    break
    
    elif D == 2: # Analogous to 3D-system
        for _ in range(S):
            test = [random.random(), random.random()]

            for j in range(N):
                dx = abs(test[0] - coordinates[j][0])
                dy = abs(test[1] - coordinates[j][1])

                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)

                distance_squared = dx**2 + dy**2

                if distance_squared <= R**2:
                    inside_sphere += 1
                    break

    return inside_sphere / S # Returns the Volume/Area fraction, which is the same as the number of shots inside 
                            #  the sphere/circle, normalized by the number of total shots.

def random_vector(length, D):
    '''
    Generates a D-dimensional vector of a given length, pointing in a random direction.
    Here, the two approaches could probably also be generalized into one approach.
    It first checks the dimension of the vector, then generates three random floats between -1 and 1,
    then calculates the length of this first vector using Pythagoras and multiplies it by the desired length.
    Then outputs the vector as a list.

    Args:
        length: Vector length
        D: Vector dimension
    
    Returns:
        list: Random D-dimensional vector of length 'length'
    
    Example:
        >>> random_vector(0.5, 2)
        [-0.20000000, 0.45825757]
    '''
    if D == 3: # Checks dimension of vector
        a, b, c = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1) # Calculates unnormalized vector
        l = math.sqrt(a**2 + b**2 + c**2) # Calculates length of this first vector using the Pythagorean theorem 
        a *= length / l # Normalizes each vector entry and multiplies it by the desired length
        b *= length / l
        c *= length / l
        
        return [a, b, c] # Returns vector as a list
    
    elif D == 2: # Analogous to 3D-approach
        a, b = random.uniform(-1, 1), random.uniform(-1, 1)
        l = math.sqrt(a**2 + b**2)
        a *= length / l
        b *= length / l
        
        return [a, b]

def SASA(N, coordinates, R, r, D, S):
    '''
    This function returns the total solvent accessible surface area (SASA) of the system, based on a Monte-Carlo-approach.
    There's also two approaches based on the dimension of the system, which could probably be generalized within one approach.
    We start with initializing O as O = S, the function then first checks the dimensionality of the system, then calculates the
    hypothetical total area (A) of all the spheres/circles if they weren't touching each other.
    Then it chooses a random particle center and adds a random vector of length R+r to this point and checks the distance to 
    every othe point in the list 'coordinates'. If one of these other points is closer than R+r to the original point, 
    the value of O gets decreased by 1, which means that the point lies within another sphere of radius R+r and is 'not okay'. 
    We do this S times in total, and finally return O*A/S, which should be equal to SASA.

    Args:
        N: Number of particles
        R: Radius of particles
        S: Number of randomized 'shots' in the Monte-Carlo-approach
        D: Dimension of system
        coordinates: List of points of the particle centers, N entries which each contain D other entries
        r: Radius of solvent particle

    Returns:
        float: SASA

    Calls:
        random_vector(R+r, D): Is called to add a random vector of length R+r to a randomly chosen point of 'coordinates'

    Example:
        >>> SASA(2, [[0, 0.5], [0.5, 0.7]], 0.1, 0.1, 2, 1000)
        1.256636
    '''
    O = S # Starts with assuming that all points are 'okay'

    if D == 3: # Checks if the dimension of the system is 3
        A = N * 4 * pi * R**2 # Surface area of N non-touching (3D-)spheres with radius R
        for _ in range(S): # Iterates the following S times
            center_point = coordinates[random.randint(0, N - 1)] # Chooses a random point from 'coordinates'
            vector = random_vector(R + r, D) # Defines a random 3D-vector of length R+r, using the according function
            P = [x + y for x, y in zip(center_point, vector)]  # Vector addition of center_point and vector

            for j in range(N): # Checks the distance between P and every other point in 'coordinates', following
                                #the same approach as in 'estimate_volume_fraction()'
                dx = abs(P[0] - coordinates[j][0])
                dy = abs(P[1] - coordinates[j][1])
                dz = abs(P[2] - coordinates[j][2])

                # Apply periodic boundary conditions
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)
                dz = min(dz, 1 - dz)

                distance_squared = dx**2 + dy**2 + dz**2

                if distance_squared < (R + r)**2:
                    O -= 1 # If P is inside of any other sphere with radius R+r, the shot is 'not okay', 
                            #and O is decreased by 1
                    break
    elif D == 2: # Analogous to 3D-approach
        A = N * pi * R**2
        for _ in range(S):
            center_point = coordinates[random.randint(0, N - 1)]
            vector = random_vector(R + r, D)
            P = [x + y for x, y in zip(center_point, vector)]  # Vector addition of center_point and vector

            for j in range(N):
                dx = abs(P[0] - coordinates[j][0])
                dy = abs(P[1] - coordinates[j][1])

                # Apply periodic boundary conditions
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)

                distance_squared = dx**2 + dy**2

                if distance_squared < (R + r)**2:
                    O -= 1
                    break
    
    return O * A / S

def volume_fraction_formula(N, R, D):
    '''
    Returns the volume/area fraction of the system using the appropriate formula.

    Args:
        N: Number of particles
        R: Radius of particles
        D: Dimension of system
    
    Returns:
        float: volume/area fraction
    
    Example:
        >>> volume_fraction_formula(500, 0.3, 2)
        0.756762438562467
    '''
    if D == 2:
        return 1 - math.exp(-N * pi * R**2)
    elif D == 3:
        return 1 - math.exp(-N * 4/3 * pi * R**3)
    
def save_plot():
    '''
    Saves a given plot and adds a randomly generated string as a file name attachment, so the newly saved file
    doesn't potentially overwrite an older file.

    Example:
        >>> plt.plot(x, y)
        >>> save_plot()
        Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_yyC1.png
    '''
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(4))

    plt.savefig(f'{file_directory}plot_{random_string}.png', dpi=300)
    print(f'Plot has been saved as: {file_directory}plot_{random_string}.png\n')

def warmup(r1, r2, c1, c2):
    '''
    The area under the two conjoined semi-circles and their arc length are calculated using trigonometry. 
    The function first calculates the distance between the two circle centers 'triangle_base'.
    Then it checks, whether the circles are dijunct (first if statement). If True, the areas/circumferences of the
    two semi-circles are calculated seoparately, using the classical circle formulas, and then added together.
    Otherwise, the function checks whether or not one semi-circle completely lies within the other semi-circle 
    (2nd and 3rd if-statement). If True, the function returns the area/circumference of only the larger semi-circle.
    If all the previous if-statements were False, the function calculates the area of the triangle ('triangle_area'),
    composed of the contact point of the semi-circles and their centers using the side lengths of the triangle, given 
    by the two radii and 'triangle_base'. The formula that is used to calculate the triangle area is called 'Herons formula'.
    'triangle_area' is then further used to calculate the triangle's height 'height'.
    The angles of the two triangle vertices touching the circle centers are calculated, using the fact that 
    sin(phi) == height / r, and they are defined as 'phi1' and 'phi2'.
    These angles are then used to determine the circle sector and to calculate their total arc length and area.

    Args:
        r1: Radius of first circle
        r2: Radius of second circle
        c1: center of first circle (x-coordinate)
        c2: center of second circle
    
    Returns:
        tuple:
            float: Total area of the two cojoined semi-circles
            float: Total arc length

    Example:
        >>> warmup(1.5, 0.5, 0, 1.2)
        (3.719995978594346, 5.29165947685138)
    '''
    triangle_base = abs(c2 - c1) # Distance between circle centers, which is also the base of the
                                #  triangle touching the contact point and the centers of the two semi-circles

    if triangle_base >= (r1 + r2): # Checks if the two circles are disjunct
        circles_area = pi/2 * (r1**2 + r2**2)
        arc_length = pi * (r1 + r2)
    
    elif triangle_base + r1 <= r2: # Checks whether circle 1 lies within circle 2
        circles_area = pi/2 * r2**2
        arc_length = pi * r2
    
    elif triangle_base + r2 <= r1: # Checks whether circle 2 lies within circle 1
        circles_area = pi/2 * r1**2
        arc_length = pi * r1
    
    else: # If none of the previous cases were true, use Heron's formula and angle approach
        s = (r1 + r2 + triangle_base) / 2
        triangle_area = math.sqrt(s * (s - r1) * (s - r2) * (s - triangle_base))
        height = 2 * triangle_area / triangle_base
        phi1 = math.asin(height/r1)
        phi2 = math.asin(height/r2)

        circles_area = r1**2 * (pi - phi1)/2 + r2**2 * (pi - phi2)/2 + triangle_area
        arc_length = r1 * (pi - phi1) + r2 * (pi - phi2)
    
    return circles_area, arc_length

def plot_warmup(r1, r2, c1, c2):
    '''
    Prepares the plots for the semi-circles according to the function warmup()

    Args:
        r1: Radius of first circle
        r2: Radius of second circle
        c1: center of first circle (x-coordinate)
        c2: center of second circle
    
    Returns:
        Nothing: Plot is ready to be plotted
    
    Example:
        >>> r1, r2, c1, c2 = 1.5, 0.5, 0, 1.2
        >>> area, arclength = warmup(r1, r2, c1, c2)
        >>> plot_warmup(r1, r2, c1, c2)
        >>> save_plot()
        >>> print(f'The area is {area:.3f}, the arc length is {arclength:.3f}.')
        >>> plt.show()
        Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_yyC1.png
        The area is 3.720, the arc length is 5.292.
    '''
    ax.add_patch(plt.Circle((c1, 0), r1, fill=False, color='black'))
    plt.scatter(c1, 0, color='black')
    ax.add_patch(plt.Circle((c2, 0), r2, fill=False, color='black'))
    plt.scatter(c2, 0, color='black')

    ax.set_ylim(0, max(r1, r2)*1.05)
    ax.set_xlim(min(c1-r1, c2-r2)-0.05*max(r1, r2), max(c1+r1, c2+r2)+0.05*max(r1, r2))
    ax.set_aspect('equal')
    plt.title(f'$r_1 = {r1:.2f},\; c_1 = {c1:.2f},\; r_2 = {r2:.2f},\; c_2 = {c2:.2f}$')

def V_fraction_against_R(steps, S, R_max, N, D, coordinates):
    '''
    To solve application 1, use: D = 2, N = 50, R_max = 1
    Application 5: D = 3, N = 50, R_max = 1
    
    Plots the volume/area fraction against the radius of the particles (R) from R = 0 to R = R_max.
    The number of steps between 0 and R_max is given by 'steps.
    It calculates the volume fraction using the Monte-Carlo-approach given with function estimate_volume_fraction()
    and compares it with the idealized values of the formula given by the function volume_fraction_formula()

    Args:
        steps: Number of steps to be plotted along the x-axis
        S: Number of Monte-Carlo-'shots' that is fed into estimate_volume_fraction()
        R_max: Gives the range of the particle radii R, 0 <= R <= R_max
        N: Number of particles
        D: Dimension of simulation
        coordinates: List of center points of the particles
    
    Returns:
        Nothing: Prints status messages and creates plot
    
    Calls:
        estimate_volume_fraction(N, R, S, D, coordinates)
        volume_fraction_formula(N, R, D)
    
    Example:
        >>> N, D = 500, 2
        >>> generate_system(N, D, file_directory, csv_name)
        >>> N, D, coordinates = read_csv_file(file_directory, csv_name)
        >>> steps, S, R_max = 100, 10_000, 1
        >>> V_fraction_against_R(steps, S, R_max, N, D, coordinates)
        >>> save_plot()
        >>> plt.show()
        CSV file '/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/coordinates.csv' with 2 columns and 500 rows has been created.
        1 of 100 complete.   
        ...
        100 of 100 complete.
        Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_y1xC.png
    '''
    x, y_script, y_formula = [], [], [] # Initializes the list for the x values and the according y-values

    for i in range(steps): # Iterates 'R' in 'steps' steps from 0 to 'R_max'
        R = i * R_max / steps
        x.append(R)
        y_script.append(estimate_volume_fraction(N, R, S, D, coordinates))
        y_formula.append(volume_fraction_formula(N, R, D))
        print(f'{i + 1} of {steps} complete.')

    plt.plot(x, y_script, label='Script')
    plt.plot(x, y_formula, label='Formula')
    plt.xlabel('R')
    plt.ylabel('Volume Fraction')
    plt.title(f'{D}D-system of {N} particles')
    plt.legend()

def SASA_against_r(steps, R, S, r_max, N, D, coordinates):
    '''
    Application 2: N = 50, R = 0.1, r_max = 1

    Plots the solvent accessible surface area (SASA) against the radius of solvent(!) particles (r) from r = 0 to r = r_max.
    It calculates SASA using the Monte-Carlo-approach given by the function SASA().
    
    Args:
        steps: Number of steps to be plotted along the x-axis
        R: Particle radius
        S: Number of Monte-Carlo-'shots' that is fed into SASA()
        r_max: Gives the range of the solvent(!) particle radii r, 0 <= r <= r_max
        N: Number of particles
        D: Dimension of simulation
        coordinates: List of center points of the particles
    
    Returns:
        Nothing: Prints status messages, generates plot
    
    Calls:
        SASA(N, coordinates, R, r, D, S)
    
    Example:
        >>> N, D = 50, 2
        >>> generate_system(N, D, file_directory, csv_name)
        >>> N, D, coordinates = read_csv_file(file_directory, csv_name)
        >>> steps, S, R, r_max = 100, 10_000, 0.1, 0.2
        >>> SASA_against_r(steps, R, S, r_max, N, D, coordinates)
        >>> save_plot()
        >>> plt.show()
        CSV file '/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/coordinates.csv' with 2 columns and 50 rows has been created.
        1 of 100 complete.   
        ...
        100 of 100 complete.
        Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_7u3R.png
    '''
    x, y = [], []

    for i in range(steps):
        r = i * r_max / steps
        x.append(r)
        y.append(SASA(N, coordinates, R, r, D, S))
        print(f'{i + 1} of {steps} complete.')

    plt.plot(x, y, label='SASA')
    plt.xlabel('r_solvent')
    plt.ylabel('SASA')
    plt.title(f'{D}D-SASA-simulation with {N} particles of radius {R}')

def draw_system(R, r, N, D, coordinates):
    '''
    Application 4: N = 0, R = 0.1, r = 0
    Application 6: N = 30, R = 0.1, r = 0.05

    Draws the particles in a 2D-system as circles of radius 'R', with their position according to the list 'coordinates.
    It also draws the area that is closer to the circles than the solvent radius, 'r'.
    To apply the periodic boundary conditions, it does this nine times, translating to the according positions.
    The function also implements a rather sophisticated status message system.

    Args:
        R: Particle radius
        r: solvent particle radius
        N: Number of particles
        D: Dimension of system (must be 2!)
        coordinates: List of particle center points
    
    Returns:
        Nothing: Creates plot and prints status or error messages
    
    Example:
        >>> N, D, R, r = 30, 2, 0.1, 0.05
        >>> generate_system(N, D, file_directory, csv_name)
        >>> N, D, coordinates = read_csv_file(file_directory, csv_name)
        >>> draw_system(R, r, N, D, coordinates)
        >>> save_plot()
        >>> plt.show()
        CSV file '/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/coordinates.csv' with 2 columns and 30 rows has been created.
        1 of 18 complete.
        ...
        18 of 18 complete.
        Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_Kghz.png
    '''
    translate = [-1, 0, 1]

    if D != 2: # It has to be a 2D-system, otherwise print error
        print('Error! D has to be set to 2.\n')
        sys.exit(1)
    elif r > 0: # Plots region occupied by solvent particles that touch the particles
        total_steps = 27

        for i in range(3):
                    transl_x = translate[i]
                    for j in range(3):
                        transl_y = translate[j]
                        for coord in coordinates:
                            x, y = coord
                            circle = plt.Circle((x + transl_x, y + transl_y), R + r + 0.003, color='black', fill=True,
                                                label='Contact zone boundary')
                            ax.add_patch(circle)
                        print(f'{i * 3 + j + 1} of {total_steps} complete.')

        for i in range(3):
            transl_x = translate[i]
            for j in range(3):
                transl_y = translate[j]
                for coord in coordinates:
                    x, y = coord
                    circle = plt.Circle((x + transl_x, y + transl_y), R + r, color='c', fill=True,
                                         label='Particle-solvent contact zone')
                    ax.add_patch(circle)
                print(f'{i * 3 + j + 10} of {total_steps} complete.')
    else:
        total_steps = 9

    for i in range(3): # Plots particles
        transl_x = translate[i]
        for j in range(3):
            transl_y = translate[j]
            for coord in coordinates:
                x, y = coord
                circle = plt.Circle((x + transl_x, y + transl_y), R + 0.003, color='black', fill=True, label='particle boundary')
                ax.add_patch(circle)
                circle = plt.Circle((x + transl_x, y + transl_y), R, color='grey', fill=True, label='particle')
                ax.add_patch(circle)
            print(f'{i * 3 + j + total_steps - 8} of {total_steps} complete.')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.title(f'{N} particles of radius {R}, solvent r = {r}')

########################################################################################################

'''
EXAMPLE USES:

Warm up:
    r1, r2, c1, c2 = 1.5, 0.5, 0, 1.2
    area, arclength = warmup(r1, r2, c1, c2)
    plot_warmup(r1, r2, c1, c2)
    save_plot()
    print(f'The area is {area:.3f}, the arc length is {arclength:.3f}.\n')
    plt.show()

Application 1:
    N, D, steps, S, R_max= 50, 3, 100, 10_000, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    V_fraction_against_R(steps, S, R_max, N, D, coordinates)
    save_plot()
    plt.show()

Application 2:
    N, D, steps, S, R, r_max = 50, 3, 100, 10_000, 0.1, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    SASA_against_r(steps, R, S, r_max, N, D, coordinates)
    save_plot()
    plt.show()

Application 4:
    N, D, R, r = 50, 2, 0.1, 0
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    draw_system(R, r, N, D, coordinates)
    save_plot()
    plt.show()

Application 5:
    N, D, steps, S, R_max= 50, 2, 100, 10_000, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    V_fraction_against_R(steps, S, R_max, N, D, coordinates)
    save_plot()
    plt.show()

Application 6:
    N, D, R, r = 30, 2, 0.1, 0.05
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    draw_system(R, r, N, D, coordinates)
    save_plot()
    plt.show()
'''
