
1.  Get Python v3.x from 

      https://www.python.org/downloads/

2.  Get pip (if not already installed with python)

3.  In the Command Prompt run
	
      pip install numpy
	
      pip install matplotlib

      pip install sympy

4.  In the file cellevolution.py, the main fuction is:
      cellevolution(pop, max_pop, shape, grid, ngen, mem, fitfun, par, max_fit, co, nmut, pmut, seed, color)
    This fuction, given:
  - pop = the matrix of the initial population (see pop_rand and pop_bordered);
  - max_pop = the maximum state value in the population
  - shape = the shape of the world, where:
    't' = torus, 'c' = closed, 'v' = vertical cylinder, 'h' = horizontal cylinder;
  - grid = the presence of a grid of fixed cells, is a triplet [p, r, c] where:
    p = False -> no grid, p = True -> grid with cells every r rows and c columns;
  - ngen = number of total iterations;
  - mem = number of generations to be saved;
  - fitfun = fitness function (see functions with "fit_" in the name);
  - par = parameters for the fitness function;
  - max_fit = the maximum fitness value achievable
  - co = crossover operator (see functions with "co_" in the name);
  - nmut = period of mutation (integer);
  - pmut = probability of mutation (between 0 and 1);
  - seed = seed for random parts;
  - color = colormap for plots
    (see https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html);
  prints the evolution of the system and returns population and fitness values
  of the last mem generations in two trhee-dimensional matrix of size
  mem x shape(pop).
