# Group Report: Solvent Accessible Surface Area (SASA) Calculation Project

The project aims to develop a codebase for the calculation of Solvent Accessible Surface Area (SASA) in various scenarios, including 2D and 3D systems with overlapping spheres and circles of different radii, using a Monte-Carlo-approach. The prerequisites for the project are given in the according [README](https://github.com/CTL-2023/sasa-materialgirls/blob/main/README.md). The code for the main task and a geometrical approach to the warm-up exercise are given in the [final draft](https://github.com/CTL-2023/sasa-materialgirls/blob/main/SASA_nico_final.py).

## Layout of the Algorithm and Functions
### Generate System
Creates a 'coordinates.csv' file in the given directory with D columns and N rows. Entries are random floats between 0 and 1, which act as the center points of the circular/spherical particles in the 1x1-square/1x1x1-cube. Finally, it prints if the process was succesful, otherwise it raises an error.

    generate_system(N, D, file_directory, csv_name)
        '''
        Args:
            N: Number of lines in csv / Number of center points
            D: Number of colums in csv / Number of dimensions in our simulation
            file_directory: Directory of saved csv-file
            csv_name: File name
        
        Returns:
            Nothing: Saves generated CSV file in desired location and prints success prompt or prints error message
        '''

### Read CSV File
Reads the 'coordinates.csv'-file in the given directory and returns a nested list 'coordinates' with N entries, which each further contain D entries. Also returns D and N.

    read_csv_file(file_directory, csv_name):
        '''
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
        '''

### Estimate Volume/Area Fraction
Returns the volume/area-fraction of the randomly distributed particles with radius R in the 1x1-square, depending whether it's a 1D- or 2D-system. The 2D-approach is analogous to the 3D one, and they could probably be generalized into one approach.

    estimate_volume_fraction(N, R, S, D, coordinates):
        '''
        Args:
            N: Number of particles
            R: Radius of particles
            S: Number of randomized 'shots' in the Monte-Carlo-approach
            D: Dimension of system
            coordinates: List of points of the particle centers, N entries which each contain D other entries
            
        Returns: 
            float: Volume/Area fraction of the overlapping particles in the 1x1(x1) grit (between 0 and 1)
        '''

### Generate Random Vector

Generates a D-dimensional vector of a given length, pointing in a random direction. Here, the two approaches could probably also be generalized into one approach. It first checks the dimension of the vector, then generates three random floats between -1 and 1, then calculates the length of this first vector using Pythagoras and multiplies it by the desired length.
Then outputs the vector as a list.
   
    random_vector(length, D):
        '''
        Args:
                length: Vector length
                D: Vector dimension
            
        Returns:
                list: Random D-dimensional vector of length 'length
        '''

### Calculate SASA
This function returns the total solvent accessible surface area (SASA) of the system, based on a Monte-Carlo-approach. There's also two approaches based on the dimension of the system, which could probably be generalized within one approach. We start with initializing O as O = S, the function then first checks the dimensionality of the system, then calculates the hypothetical total area (A) of all the spheres/circles if they weren't touching each other. Then it chooses a random particle center and adds a random vector of length R+r to this point and checks the distance to  every othe point in the list 'coordinates'. If one of these other points is closer than R+r to the original point,  the value of O gets decreased by 1, which means that the point lies within another sphere of radius R+r and is 'not okay'. We do this S times in total, and finally return O*A/S, which should be equal to SASA.

    SASA(N, coordinates, R, r, D, S):
        '''
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
        '''

### Volume/Area Fraction: Mathematical Formula
Returns the volume/area fraction of the system using the appropriate formula.

    volume_fraction_formula(N, R, D):
        '''
        Args:
            N: Number of particles
            R: Radius of particles
            D: Dimension of system
        
        Returns:
            float: volume/area fraction
        '''

### Save Plot
Saves a given plot and adds a randomly generated string as a file name attachment, so the newly saved file doesn't potentially overwrite an older file.

    save_plot():
        '''
        Example:
            >>> plt.plot(x, y)
            >>> save_plot()
            Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_yyC1.png
        '''

### Warmup Exercise: A Geometrical Approach
The area under the two conjoined semi-circles and their arc length are calculated using trigonometry. The function first calculates the distance between the two circle centers 'triangle_base'. Then it checks, whether the circles are dijunct (first if statement). If True, the areas/circumferences of the two semi-circles are calculated seoparately, using the classical circle formulas, and then added together. Otherwise, the function checks whether or not one semi-circle completely lies within the other semi-circle (2nd and 3rd if-statement). If True, the function returns the area/circumference of only the larger semi-circle. If all the previous if-statements were False, the function calculates the area of the triangle ('triangle_area'), composed of the contact point of the semi-circles and their centers using the side lengths of the triangle, given by the two radii and 'triangle_base'. The formula that is used to calculate the triangle area is called 'Herons formula'. 'triangle_area' is then further used to calculate the triangle's height 'height'. The angles of the two triangle vertices touching the circle centers are calculated, using the fact that sin(phi) == height / r, and they are defined as 'phi1' and 'phi2'. These angles are then used to determine the circle sector and to calculate their total arc length and area.

    warmup(r1, r2, c1, c2):
        '''
        Args:
            r1: Radius of first circle
            r2: Radius of second circle
            c1: center of first circle (x-coordinate)
            c2: center of second circle
        
        Returns:
            tuple:
                float: Total area of the two cojoined semi-circles
                float: Total arc length
        '''

### Warm-Up Plot Function
Prepares the plots for the semi-circles according to the function warmup().

    plot_warmup(r1, r2, c1, c2):
    '''
        Args:
            r1: Radius of first circle
            r2: Radius of second circle
            c1: center of first circle (x-coordinate)
            c2: center of second circle
        
        Returns:
            Nothing: Plot is ready to be plotted
    '''

### Plot the Volume Fraction Against Particle Radius (Application 1 & 5)
To solve application 1, use: D = 2, N = 50, R_max = 1
Application 5: D = 3, N = 50, R_max = 1

Plots the volume/area fraction against the radius of the particles (R) from R = 0 to R = R_max. The number of steps between 0 and R_max is given by 'steps. It calculates the volume fraction using the Monte-Carlo-approach given with function estimate_volume_fraction() and compares it with the idealized values of the formula given by the function volume_fraction_formula().

    V_fraction_against_R(steps, S, R_max, N, D, coordinates):
        '''
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
        '''

### Plot SASA Against the Solvent Particle Radius (Application 2)
Application 2: N = 50, R = 0.1, r_max = 1

Plots the solvent accessible surface area (SASA) against the radius of solvent(!) particles (r) from r = 0 to r = r_max. It calculates SASA using the Monte-Carlo-approach given by the function SASA().

    SASA_against_r(steps, R, S, r_max, N, D, coordinates):
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
        '''

### Plot the System (Application 4 & 6)
Application 4: N = 0, R = 0.1, r = 0
Application 6: N = 30, R = 0.1, r = 0.05

Draws the particles in a 2D-system as circles of radius 'R', with their position according to the list 'coordinates'. It also draws the area that is closer to the circles than the solvent radius, 'r'. To apply the periodic boundary conditions, it does this nine times, translating to the according positions. The function also implements a rather sophisticated status message system.

    draw_system(R, r, N, D, coordinates):
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
        '''

## How To Run the Code
Firstly, it's important to have Python installed (we used version 3.11.5), as well as the necessary libraries, from which numpy and matplotlib are not installed by default. Secondly, choose the according file directory where you want to save your files  by editing the file_directory constant:

    file_directory = "/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/" # Include your directory here, as separators, use / for mac, \\ for pc

After that, you can run one of the functions or try one of the example uses, according to the 'applications' in the [README.md](https://github.com/CTL-2023/sasa-materialgirls/blob/main/README.md).

## Example Uses & Results
Run one of the code snippets at the end of the code. The text in *italic* is copied unchanged from [README.md](https://github.com/CTL-2023/sasa-materialgirls/blob/main/README.md)

### Warm-Up Exercise
    r1, r2, c1, c2 = 1.5, 0.5, 0, 1.2
    area, arclength = warmup(r1, r2, c1, c2)
    plot_warmup(r1, r2, c1, c2)
    save_plot()
    print(f'The area is {area:.3f}, the arc length is {arclength:.3f}.\n')
    plt.show()

    >>> The area is 3.720, the arc length is 5.292.

<img src="https://github.com/CTL-2023/sasa-materialgirls/blob/main/warmup.png" width=50%>

### Application 1:
*Use the above functions to create systems with $N=50$ spheres of radius $R$ between $R=0$ and $R=1$. Verify the applicability of the 3D formula $\phi=1-\exp(-4\pi N R^3/3)$.*

    N, D, steps, S, R_max= 50, 3, 100, 10_000, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    V_fraction_against_R(steps, S, R_max, N, D, coordinates)
    save_plot()
    plt.show()

    >>> 1 of 100 complete.
    >>> ...
    >>> 100 of 100 complete.
    >>> Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_o1Za.png

<img src="https://github.com/CTL-2023/sasa-materialgirls/blob/b1cc859bd5046319c6968ea1de20d346b79d8510/app1.png" width=50%>

### Application 2:
*Use the above functions to create a system with $N=50$ spheres of radius $R=0.1$, and plot SASA($r$) as function of $r$. SASA should decrease from a value smaller (why?) or equal to $A$ at $r=0$ to zero at $r=1$.*

    N, D, steps, S, R, r_max = 50, 3, 100, 10_000, 0.1, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    SASA_against_r(steps, R, S, r_max, N, D, coordinates)
    save_plot()
    plt.show()

    >>> 1 of 100 complete.
    >>> ...
    >>> 100 of 100 complete.
    >>> Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_H9px.png

<img src="https://github.com/CTL-2023/sasa-materialgirls/blob/b1cc859bd5046319c6968ea1de20d346b79d8510/app2.png" width=50%>

### Application 4:
*Generate a 2D system with $N=50$ circles of radius $R=0.1$ and plot the configuration.*

    N, D, R, r = 50, 2, 0.1, 0
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    draw_system(R, r, N, D, coordinates)
    save_plot()
    plt.show()

    >>> 1 of 9 complete.
    >>> ...
    >>> 9 of 9 complete.
    >>> Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_kCZ0.png

<img src="https://github.com/CTL-2023/sasa-materialgirls/blob/b1cc859bd5046319c6968ea1de20d346b79d8510/app4.png" width=50%>

### Application 5:
*Verify the applicability of the 2D formula $\phi=1-\exp(-\pi N R^2)$.*

    N, D, steps, S, R_max= 50, 2, 100, 10_000, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    V_fraction_against_R(steps, S, R_max, N, D, coordinates)
    save_plot()
    plt.show()

    >>> 1 of 100 complete.
    >>> ...
    >>> 100 of 100 complete.
    >>> Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_3nR6.png

<img src="https://github.com/CTL-2023/sasa-materialgirls/blob/b1cc859bd5046319c6968ea1de20d346b79d8510/app5.png" width=50%>

### Application 6:
*Generate a 2D system with $N=30$ circles of radius $R=0.1$ and plot the configuration as well as the region occupied by solvent particles of radius 0.05 that touch the surface of the filled region.*

    N, D, R, r = 30, 2, 0.1, 0.05
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    draw_system(R, r, N, D, coordinates)
    save_plot()
    plt.show()

    >>> 1 of 27 complete.
    >>> ...
    >>> 27 of 27 complete.
    >>> Plot has been saved as: /Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/plot_fNqA.png

<table>
  <tr>
    <td><img src="https://github.com/CTL-2023/sasa-materialgirls/blob/b1cc859bd5046319c6968ea1de20d346b79d8510/app6_2.png" alt="Image 1"></td>
    <td><img src="https://github.com/CTL-2023/sasa-materialgirls/blob/b1cc859bd5046319c6968ea1de20d346b79d8510/app6.png" alt="Image 2"></td>
  </tr>
</table>

The figure on the left uses the parameters given by the readme file, the figure on the right is an example using different parameters.

