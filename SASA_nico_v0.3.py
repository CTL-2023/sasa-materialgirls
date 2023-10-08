import csv
import random
import math
import matplotlib.pyplot as plt
import secrets
import string
import sys

def generate_system(N, D):
    output_file = f"{file_directory}coordinates.csv"  # Change this to the desired output file name

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

def read_csv_file(file_directory):
    file_path = f"{file_directory}coordinates.csv"
    coordinates = []

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
    inside_sphere = 0
   
    if D == 3:
        for _ in range(S):
            test = [random.random(), random.random(), random.random()]

            for j in range(N):
                dx = abs(test[0] - coordinates[j][0])
                dy = abs(test[1] - coordinates[j][1])
                dz = abs(test[2] - coordinates[j][2])

                # Apply periodic boundary conditions
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)
                dz = min(dz, 1 - dz)

                distance_squared = dx**2 + dy**2 + dz**2

                if distance_squared <= R**2:
                    inside_sphere += 1
                    break
    
    elif D == 2:
        for _ in range(S):
            test = [random.random(), random.random()]

            for j in range(N):
                dx = abs(test[0] - coordinates[j][0])
                dy = abs(test[1] - coordinates[j][1])

                # Apply periodic boundary conditions
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)

                distance_squared = dx**2 + dy**2

                if distance_squared <= R**2:
                    inside_sphere += 1
                    break

    return inside_sphere / S

def random_vector(length, D):
    if D == 3:
        a, b, c = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
        l = math.sqrt(a**2 + b**2 + c**2)
        a *= length / l
        b *= length / l
        c *= length / l
        
        return [a, b, c]
    elif D == 2:
        a, b = random.uniform(-1, 1), random.uniform(-1, 1)
        l = math.sqrt(a**2 + b**2)
        a *= length / l
        b *= length / l
        
        return [a, b]

def SASA(N, coordinates, R, r, D, S):
    O = S

    if D == 3:
        A = N * 4 * math.pi * R**2
        for _ in range(S):
            center_point = coordinates[random.randint(0, N - 1)]
            vector = random_vector(R + r, D)
            P = [x + y for x, y in zip(center_point, vector)]  # Vector addition of center_point and vector

            for j in range(N):
                dx = abs(P[0] - coordinates[j][0])
                dy = abs(P[1] - coordinates[j][1])
                dz = abs(P[2] - coordinates[j][2])

                # Apply periodic boundary conditions
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)
                dz = min(dz, 1 - dz)

                distance_squared = dx**2 + dy**2 + dz**2

                if distance_squared < (R + r)**2:
                    O -= 1
                    break
    elif D == 2:
        A = N * math.pi * R**2
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
    if D == 2:
        return 1 - math.exp(-N * math.pi * R**2)
    elif D == 3:
        return 1 - math.exp(-N * 4/3 * math.pi * R**3)


    
def save_plot():
    # Generate a random string as a file name attachment
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(4))

    plt.savefig(f'{file_directory}plot_{random_string}.png')
    
########################################################################################################

def V_fraction_against_R(steps, S, R_max, N, D, coordinates): # D = 3 for app.1, D = 2 for app.5
    x, y_script, y_formula = [], [], []

    for i in range(steps):
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

def SASA_against_r(steps, R, S, r_max, N, D, coordinates):  # app.2
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

def draw_system(R, r, N, D, coordinates): # r = 0 for app.4, r > 0 for app.6
    ax = plt.subplots()[1]
    translate = [-1, 0, 1]

    if D != 2:
        print('Error! D has to be set to 2.\n')
        sys.exit(1)
    elif r > 0:
        total_steps = 18
        for i in range(3):
            transl_x = translate[i]
            for j in range(3):
                transl_y = translate[j]
                for coord in coordinates:
                    x, y = coord
                    circle = plt.Circle((x + transl_x, y + transl_y), R + r, color='c', fill=True,
                                         label='Particle-solvent contact zone')
                    ax.add_patch(circle)
                print(f'{i * 3 + j + 1} of {total_steps} complete.')
    else:
        total_steps = 9

    for i in range(3):
        transl_x = translate[i]
        for j in range(3):
            transl_y = translate[j]
            for coord in coordinates:
                x, y = coord
                circle = plt.Circle((x + transl_x, y + transl_y), R, color='grey', fill=True, label='particle')
                ax.add_patch(circle)
                circle = plt.Circle((x + transl_x, y + transl_y), R, color='black', fill=False, label='particle boundary')
                ax.add_patch(circle)
            print(f'{i * 3 + j + total_steps - 8} of {total_steps} complete.')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.title(f'{N} particles of radius {R}, solvent r = {r}')

########################################################################################################

file_directory = "/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/" # Include your directory here 
# (as separators, use / for mac, \\ for pc)
print()
generate_system(N = 500, D = 2)

N, D, coordinates = read_csv_file(file_directory) # Number of particles, Dimensions, Coordinates of particle centers

steps = 100
S = 10_000
R = 0.03
R_max = 0.25
r = 0.02
r_max = 0.25

# RUN YOUR FUNCTION HERE:
V_fraction_against_R(steps, S, R_max, N, D, coordinates)
# SASA_against_r(steps, R, S, r_max, N, D, coordinates)
# draw_system(R, r, N, D, coordinates)

print('\nDone.\n')

save_plot()
plt.show()