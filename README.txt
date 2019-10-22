
1.  Get Python from 

      https://www.python.org/downloads/

2.  Get pip (if not already installed with python)

3.  In the Command Prompt run
	
      pip install numpy
	
      pip install matplotlib

      pip install sympy

4.  Depending on the version of python installed (2.x or 3.x), the gui versions are:
    - cellevolution_gui_py2.x.py 
    - cellevolution_gui_py3.x.py
    See details in the gui help.
   
    The script version is cellevolution.py where the main fuction is:
      cellevolution(pop, shape, grid, ngen, mem, fitfun, par, co, nmut, pmut, seed, color)
    This fuction, given:
    - pop = the matrix of the initial population (see randpop and randpop1);
    - shape = the shape of the world, where:
      0 = torus, 1 = closed, 2 = vertical cylinder, 3 = horizontal cylinder;
    - grid = the presence of a grid of fixed cells, is a triplet [p, r, c] where:
      p = 0 -> no grid, p = 1 -> grid with cells every r rows and c columns;
    - ngen = number of total iterations;
    - mem = number of generations to be saved;
    - fitfun = fitness function (see functions with "fit_" in the name);
    - par = parameters for the fitness function;
    - co = crossover operator (see functions with "co_" in the name);
    - nmut = period of mutation (integer);
    - pmut = probability of mutation (between 0 and 1);
    - seed = seed for random parts;
    - color = colormap for plots
      (see https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html);
    prints the evolution of the system and returns population and fitness values
    of the last mem generations in two trhee-dimensional matrix of size shape(pop) x mem.
    For further details, run >>> help(function_name).
