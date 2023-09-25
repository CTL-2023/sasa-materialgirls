General information about the CTL course available at https://ctl.polyphys.mat.ethz.ch/ 

# :wave: Solvent (or Roomba) accessible surface area (SASA)

Consider a system composed of filled monodisperse spheres of identical radius $R$ contained in a periodic cubic (3D) box, and surrounded by empty space or 'solvent' (dust in the case you prefer to think of a Roomba problem, the Roomba problem is the 2D version of the SASA problem, which we are planning to treat as well). The filled spheres may partially overlap (in the figure below, they do not overlap). In this project, we will consider two of the many interesting geometrical properties of such systems. The first property we will consider is the volume fraction of the filled spheres, which corresponds to the ratio of the total volume occupied by the filled spheres to the volume of the entire cubic simulation box in which they are contained. The second property we will consider is the part of the filled regions's surface area which can be reached by an additional sphere (the blue roomba) of radius $r$ which is located entirely in the empty space but is in contact with the surface area of the filled region. This quantity is called SASA($r$). For $r=0$, SASA($r$) is the total surface area of the filled region, and for $r\rightarrow\infty$, SASA($r$) approaches zero (the larger the roomba, the more problematic becomes the cleaning. A related problem not treated in this exercise is the volume (or area) that can be reached by the 3D (2D) roomba.    

<img src="https://ctl.polyphys.mat.ethz.ch/CTL-I-PUBLIC/SASA/periodic-images-rev.png" width="50%">

# Warm-up exercise 

To prepare you for a possible solution strategy to these problems using random numbers, this project begins with two simpler tasks: compute (A) the area $A$ enclosed by, and (B) the perimeter $L$ (marked in red) of the overlapping half circles. 

<img src="https://ctl.polyphys.mat.ethz.ch/CTL-I-PUBLIC/SASA/preSASA.png" width="50%">

The centers of the half circles of radius $R_1=1.5$ and $R_2=0.5$ are at ${\bf c}^{(1)}=(0,0)$ and ${\bf c}^{(2)}=(1.2,0)$. The half circles are both enclosed within the rectangular area $[a,b]\times [c,d]$ with $a=-2$, $b=2$, $c=0$, and $d=2$, as shown.
(A) Implement the following three methods to estimate area $A$. To do so, you should first define a function $f(x)$ that agrees with the red line, and is zero otherwise, i.e., for $x < c_x^{(1)}-R_1=-1.5$ and $x > c_x^{(2)}+R_2=1.7$.

    Check your python def f(x): plot this function, and compare with the above figure.

The three methods are:

1. Classical Riemann definition of an integral upon replacing the half circles by a function $f(x)$, and using $N$ bins of size $dx=(b-a)/N$ to estimate $A=\int_a^b f(x)\ dx$.
2. Monte Carlo with probability density $p(x)=(b-a)^{-1}$, using $N$ shots. The integal $A$ is estimated via $\langle f(x)/p(x)\rangle = (b-a)\langle f(x)\rangle$, i.e., by the mean $f$-value at the random poxitions $x$, multiplied by the interval length $b-a$.
3. Monte Carlo with probability density $p(x,y)=[(b-a)(d-c)]^{-1}$, using $N$ shots. The integal $A$ is estimated via the fraction of $y$-values that reside below $f(x)$, multiplied by the rectangular area into which you shoot.

All three methods should return an estimate for the area $A$ for given $N$. 

    Check your implementations: upon increasing N the estimate for A should approach the exact result, A = 3.598616448..

(B) Invent a method to calculate the contour length $L$ of the red line in the above figure. If you choose a Monte Carlo method, instead of shooting into the $x$-axis or into the rectangular area, it may be useful to shoot into the perimeters of the complete half circles, i.e., use $p(\varphi)=(\pi R_1)^{-1}$ for the first half circle, and something similar for the 2nd half circle, where $\varphi$ denotes a polar angle, $\varphi$ in [0,&pi;].

    Check your implementations: upon increasing N the estimate for L should approach the exact result, L = 4.8061..

Having completed these warm-up exercises, you are in the position to treat the more complex problem using similar methods. You are free to choose a method. We propose the following structure of your code:  

# SASA code

## def generate_system(*N*)

Place $N$ points (3D) randomly into a square (or cubic) box of unit side length $1$. Write the coordinates of the $N$ points to a file named coordinates.csv ($N$ rows, $3$ columns, blank-separated numbers). 

## def read_system

Read the coordinates of the spheres from a file named coordinates.csv. Determine $N$ and return $N$ and the coordinates. 

## def estimate_volume_fraction(*N,coordinates},R*)

Estimate and return the volume fraction of the $N$ spheres of radius $R$ inside the cubic box. One Monte-Carlo-type approach consists of shooting randomly into the unit box volume and to then count the fraction $f$ of shots that hit at least one of the filled spheres. The volume fraction $\phi$ is then estimated as $\phi=f$. Return the estimated volume fraction $\phi$. Note that periodic boundary conditions have to be taken into account properly. Some of the filled spheres may cross one or more boundaries of the periodic box. If this function is implemented using a number $S$ of random shots, you may add $S$ to the list of arguments of this function.

## def random_unit_vector

This function will be needed below. It creates a random 3D vector of unit length and returns this vector. To test if this function works, create $S$ random unit vectors ${\bf u}$, and calculate their mean squared $x$-component, i.e., $\langle u_x^2\rangle$. This should result in $1/3$. Also check if $\langle u_xu_y\rangle$ approaches zero if $S$ is increased to a large value like $S=10000$.

## def SASA(*N,coordinates,R,r*)

For the given system characterized by $R$, estimate and return SASA as function of $r$, i.e., the surface area that can be reached by a sphere of radius $r$. For the simplest case of $r=0$, one approach is again using a Monte-Carlo scheme. To this end, randomly shoot into the surface of a randomly selected filled sphere using the random_unit_vector function. Let us denote this point by $P$. Check, if this point $P$ is located inside any of the remaining filled spheres. If not, $P$ is said to be 'ok', located on the surface of the filled region, i.e., exposed to the solvent accessible space, and can be reached by a solvent particle of radius $r=0$. Repeat this procedure, create a large number $S$ of points $P$ and count the number of shots that are 'ok'. Denote ths number by $O$. The fraction of the total surface $A=N\times 4\pi R^2$ of the individual filled spheres that is accessible to solvent particles of radius $r=0$ is hence $O/S$. Accordingly, the estimated SASA($r=0$) value is SASA($r=0)=OA/S$.

Based on these considerations, develop a method to estimate SASA($r$) for $r>0$. Hint: A solvent particle of radius $r$ touching the surface at point $P$ can be inserted into the empty space only if the distance between the solvent particle's center and the centers of all the filled spheres is $r$ or larger.

## Application 1

Use the above functions to create systems with $N=50$ spheres of radius $R$ between $R=0$ and $R=1$. Verify the applicability of the 3D formula $\phi=1-\exp(-4\pi N R^3/3)$.

## Application 2

Use the above functions to create a system with $N=50$ spheres of radius $R=0.1$, and plot SASA($r$) as function of $r$. SASA should decrease from a value smaller (why?) or equal to $A$ at $r=0$ to zero at $r=1$.

## Application 3

Modify the code so that it works equally well for 2D systems and introduce the space dimension $D$ as an additional argument in all functions (allow for $D=2$ or $D=3$). Note that several expression such as $A$ have to be adjusted, and generate_system as well. 

## Application 4

Generate a 2D system with $N=50$ circles of radius $R=0.1$ and plot the configuration. 

## Application 5

Verify the applicability of the 2D formula $\phi=1-\exp(-\pi N R^2)$.

## Application 6 (advanced)

Generate a 2D system with $N=30$ circles of radius $R=0.1$ and plot the configuration as well as the region occupied by solvent particles of radius 0.05 that touch the surface of the filled region.  
