Group report 

# Group Report: Solvent Accessible Surface Area (SASA) Calculation Project

The project aims to develop a codebase for the calculation of Solvent Accessible Surface Area (SASA) in various scenarios, including 2D and 3D systems with overlapping spheres and circles of different radii, using a Monte-Carlo-approach.

## Layout of the Algorithm and Functions
### Important Functions

    generate_system(N, D, file_directory, csv_name)
        '''
        Creates a 'coordinates.csv' file in the given directory with D columns and N rows. 
        Entries are random floats between 0 and 1, which act as the center points of the circular/spherical particles
        in the 1x1-square/1x1x1-cube. Finally, it prints if the process was succesful, otherwise it raises an error.

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

    read_csv_file(file_directory, csv_name):
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
