# Group Report: Solvent Accessible Surface Area (SASA) Calculation Project

The project aims to develop a codebase for the calculation of Solvent Accessible Surface Area (SASA) in various scenarios, including 2D and 3D systems with overlapping spheres and circles of different radii, using a Monte-Carlo-approach. The prerequisites for the project are given in the according README.md: https://github.com/CTL-2023/sasa-materialgirls/blob/main/README.md

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
        
        Example:
            >>> generate_system(3, 100, "/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/", "coordinates.csv")
            CSV file '/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/coordinates.csv' with 100 columns 
            and 3 rows has been created.
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

        Example:
            >>> read_csv_file("/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/", "coordinates.csv")
            (3, 2, [[1, 0], [0.5, 0.7], [0.9, 0.2]])
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
        
        Example:
            >>> estimate_volume_fraction(2, 0.2, 1000, 2, [[0, 0.5], [0.5, 0.8]])
            0.25132
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
                list: Random D-dimensional vector of length 'length'
            
            Example:
                >>> random_vector(0.5, 2)
                [-0.20000000, 0.45825757]
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

        Example:
            >>> SASA(2, [[0, 0.5], [0.5, 0.7]], 0.1, 0.1, 2, 1000)
            1.256636

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
        
        Example:
            >>> volume_fraction_formula(500, 0.3, 2)
            0.756762438562467
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

        Example:
            >>> warmup(1.5, 0.5, 0, 1.2)
            (3.719995978594346, 5.29165947685138)
        '''

### Warmup Plot Function
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

## How To Run the Code
Firstly, it's important to have Python installed (we used version 3.11.5), as well as the necessary libraries, from which numpy and matplotlib are not installed by default. Secondly, choose the according file directory where you want to save your files  by editing the file_directory constant:

    file_directory = "/Users/nicol/Documents/Python_Projects/CTL_II/SASA/data/" # Include your directory here, as separators, use / for mac, \\ for pc

After that, you can run one of the functions or try one of the example uses, according to the 'applications' in the README.md:

### Warmup
    r1, r2, c1, c2 = 1.5, 0.5, 0, 1.2
    area, arclength = warmup(r1, r2, c1, c2)
    plot_warmup(r1, r2, c1, c2)
    save_plot()
    print(f'The area is {area:.3f}, the arc length is {arclength:.3f}.\n')
    plt.show()

### Application 1:
    N, D, steps, S, R_max= 50, 3, 100, 10_000, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    V_fraction_against_R(steps, S, R_max, N, D, coordinates)
    save_plot()
    plt.show()

### Application 2:
    N, D, steps, S, R, r_max = 50, 3, 100, 10_000, 0.1, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    SASA_against_r(steps, R, S, r_max, N, D, coordinates)
    save_plot()
    plt.show()

### Application 4:
    N, D, R, r = 50, 2, 0.1, 0
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    draw_system(R, r, N, D, coordinates)
    save_plot()
    plt.show()

### Application 5:
    N, D, steps, S, R_max= 50, 2, 100, 10_000, 1
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    V_fraction_against_R(steps, S, R_max, N, D, coordinates)
    save_plot()
    plt.show()

### Application 6:
    N, D, R, r = 30, 2, 0.1, 0.05
    generate_system(N, D, file_directory, csv_name)
    N, D, coordinates = read_csv_file(file_directory, csv_name)
    draw_system(R, r, N, D, coordinates)
    save_plot()
    plt.show()

Press 'Run' to execute.

## Resulting Files
<img src="https://github.com/CTL-2023/sasa-materialgirls/blob/b1cc859bd5046319c6968ea1de20d346b79d8510/app1.png" width=50%>
