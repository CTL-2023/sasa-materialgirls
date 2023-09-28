import csv
import random
import math
from matplotlib import pyplot as plt

S = 10000 # 'Shots' in the Monte-Carlo-Simulation
file_directory = "/Users/nicol/Documents/Python_Projects/CTL_II/SASA" # Include your directory here
fig, ax = plt.subplots()

def generate_system(N, D):
    output_file = f"{file_directory}/coordinates.csv"  # Change this to the desired output file name

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
          print('D must be either 2 or 3.')
          return
        
    print(f"CSV file '{output_file}' with {D} colums and {N} rows has been created.")

def read_csv_file():
    file_path = f"{file_directory}/coordinates.csv"
    csv_data = []

    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=' ')
            for row in reader:
                # Convert each value to float and append to the row list
                float_row = [float(value) for value in row]
                csv_data.append(float_row)
        return len(csv_data), csv_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
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

    return inside_sphere/S

def random_vector(length, D):
    if D == 3:
        a, b, c = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
        l = math.sqrt(a**2 + b**2 + c**2)
        a *= length/l
        b *= length/l
        c *= length/l
        
        return [a, b, c]
    elif D == 2:
        a, b = random.uniform(-1, 1), random.uniform(-1, 1)
        l = math.sqrt(a**2 + b**2)
        a *= length/l
        b *= length/l
        
        return [a, b]

def SASA(N, coordinates, R, r, D):
    O = S

    if D == 3:
        A = N * 4 * math.pi * R**2
        for _ in range(S):
            center_point = coordinates[random.randint(0, N-1)]
            vector = random_vector(R + r, D)

            P = [x + y for x, y in zip(center_point, vector)] # Vector addition of center_point and vector

            for j in range(N):
                dx = abs(P[0] - coordinates[j][0])
                dy = abs(P[1] - coordinates[j][1])
                dz = abs(P[2] - coordinates[j][2])

                # Apply periodic boundary conditions
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)
                dz = min(dz, 1 - dz)

                distance_squared = dx**2 + dy**2 + dz**2

                if distance_squared < (R+r)**2:
                    O -= 1
                    break
    elif D == 2:
        A = N * math.pi * R**2
        for _ in range(S):
            center_point = coordinates[random.randint(0, N-1)]
            vector = random_vector(R + r, D)

            P = [x + y for x, y in zip(center_point, vector)] # Vector addition of center_point and vector

            for j in range(N):
                dx = abs(P[0] - coordinates[j][0])
                dy = abs(P[1] - coordinates[j][1])

                # Apply periodic boundary conditions
                dx = min(dx, 1 - dx)
                dy = min(dy, 1 - dy)

                distance_squared = dx**2 + dy**2

                if distance_squared < (R+r)**2:
                    O -= 1
                    break
    
    return O * A / S

def application_1(): # D = 3 for app.1, D = 2 for app.5
    N = 50
    D = 2
    steps = 100
    R_max = 1
    x, y_script, y_formula = [], [], []

    generate_system(N, D)
    N, coordinates = read_csv_file()

    if D == 3:
        for i in range(steps):
            R = i * R_max / steps
            x.append(R)
            y_script.append(estimate_volume_fraction(N, R, S, D, coordinates))
            y_formula.append(1 - math.exp(-N * 4/3 * math.pi * R**3))
            print(f'{i+1} of {steps} complete.')
    elif D == 2:
        for i in range(steps):
            R = i * R_max / steps
            x.append(R)
            y_script.append(estimate_volume_fraction(N, R, S, D, coordinates))
            y_formula.append(1 - math.exp(-N * math.pi * R**2))
            print(f'{i+1} of {steps} complete.')
    
    plt.plot(x, y_script, label='Script')
    plt.plot(x, y_formula, label='Formula')
    ax.set_xlabel('R')
    ax.set_ylabel('Volume Fraction')
    plt.title(f'{D}D-system of {N} particles')
    plt.legend()
    plt.show()

def application_2():
    N = 50
    D = 2
    generate_system(N, D)
    N, coordinates = read_csv_file()
    R = 0.1
    r_max = 0.25
    steps = 100
    x, y = [], []

    for i in range(steps):
        r = i*r_max/steps
        x.append(r)
        y.append(SASA(N, coordinates, R, r, D))
        print(f'{i+1} of {steps} complete.')

    plt.plot(x, y)
    ax.set_xlabel('r')
    ax.set_ylabel('SASA')
    plt.title(f'{D}D-SASA-simulation with {N} particles of radius {R}')
    plt.show()

def application_4():
    N = 50
    D = 2
    R = 0.1
    translate = [-1, 0, 1]
    generate_system(N, D)
    N, coordinates = read_csv_file()
    fig, ax = plt.subplots()

    # Plot each circle
    for i in range(3):
        transl_x = translate[i]
        for j in range(3):
            transl_y = translate[j]
            for coord in coordinates:
                x, y = coord
                circle = plt.Circle((x+transl_x, y+transl_y), R, color='grey', fill=True)
                ax.add_patch(circle)
                circle = plt.Circle((x+transl_x, y+transl_y), R, color='black', fill=False)
                ax.add_patch(circle)
            print(f'{i*3+j+1} of 9 complete.')
    
    # Set axis limits and labels
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')  # Equal aspect ratio to prevent distortion
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title(f'{N} particles of radius {R}')
    plt.show()

def application_6():
    N = 30
    D = 2
    R = 0.1
    r = 0.05
    translate = [-1, 0, 1]

    generate_system(N, D)
    N, coordinates = read_csv_file()
    fig, ax = plt.subplots()

    # Plot each circle
    for i in range(3):
        transl_x = translate[i]
        for j in range(3):
            transl_y = translate[j]
            for coord in coordinates:
                x, y = coord
                circle = plt.Circle((x+transl_x, y+transl_y), R+r, color='c', fill=True)
                ax.add_patch(circle)
            print(f'{i*3+j+1} of 18 complete.')

    for i in range(3):
        transl_x = translate[i]
        for j in range(3):
            transl_y = translate[j]
            for coord in coordinates:
                x, y = coord
                circle = plt.Circle((x+transl_x, y+transl_y), R, color='grey', fill=True)
                ax.add_patch(circle)
                circle = plt.Circle((x+transl_x, y+transl_y), R, color='black', fill=False)
                ax.add_patch(circle)
            print(f'{i*3+j+10} of 18 complete.')
    
    # Set axis limits and labels
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')  # Equal aspect ratio to prevent distortion

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title(f'{N} particles of radius {R}, solvent r = {r}')
    plt.show()

application_6()