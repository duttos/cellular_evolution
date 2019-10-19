import math
from sympy import isprime
import numpy as np
import matplotlib.pyplot as plot
import random

### UTILITIES ###
  
def N(M):
  '''
  Given a matrix M returns its vertical rotation by 1 position down,
  so that in place i,j there is the value North of the place i,j in M.
  '''
  return np.roll(M, 1, axis = 0)

def S(M):
  '''
  Given a matrix M returns its vertical rotation by 1 position up,
  so that in place i,j there is the value South of the place i,j in M.
  '''
  return np.roll(M, -1, axis = 0)

def W(M):
  '''
  Given a matrix M returns its horizontal rotation by 1 position right,
  so that in place i,j there is the value West of the place i,j in M.
  '''
  return np.roll(M, 1, axis = 1)

def E(M):
  '''
  Given a matrix M returns its horizontal rotation by 1 position left,
  so that in place i,j there is the value East of the place i,j in M.
  '''
  return np.roll(M, -1, axis = 1)
def binary(n):
  '''
  Converts an integer n is base 2.
  '''
  return [int(x) for x in bin(n)[2:]]

def supbin(nstat):
  '''
  Returns the minimum integer exp so that 2^exp >= nstat.
  '''
  exp = 0
  end = (2 ** exp >= nstat)
  while end == False:
    exp += 1
    end = (2 ** exp >= nstat)
  return exp

def contr(v):
  '''
  Returns the list v backwards
  '''
  return list(reversed(v))

def genprime3(a,n):
  '''
  Generates a list of n integers from numbers in the list
  [a, ..., a + n - 1] by checking and returning 0 if it fails,
  the value modulo 3 otherwise.
  '''
  ris = np.zeros(n, dtype = int)
  for j in range(a, a + n):
    if isprime(j):
      ris[j - a] = np.mod(j, 3)
  return ris

def genprime4(a,n):
  '''
  Generates a list of n integers from numbers in the list
  [a, ..., a + n - 1] by checking and returning 0 if it fails,
  the value modulo 4 otherwise.
  '''
  ris = np.zeros(n, dtype = int)
  for j in range(a, a + n):
    if isprime(j):
      ris[j - a] = np.mod(j, 4)
  return ris

def parity(m, n):
  ''' ??? '''
  p = np.zeros(n - m + 1, dtype = int)
  for j in range(n - m + 1):
    p[j] = np.mod(sum(binary(j + m)), 2)
  return p

### FITNESS FUNCTIONS ###

def fit_life(par, pop):
  '''
  Given par (a list of 12 integers) and pop (matrix of size m x n),
  after determining every cell state in the neightborhood modulo
  the 10th parameter, calculates the linear combination of these
  values with the first 9 parameters.
  Then returns the fitness value of each cell, which is is 1 only if:
  - his state modulo the 10th parameter is non zero and the l.c.
    is the 11th parameter;
  - the l.c. is the 12th parameter.
  '''
  [m, n] = np.shape(pop)
  pop = np.mod(pop, par[9]);
  
  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  q = par[8] * N(We) + par[1] * No  + par[2] * N(Ea) + \
      par[7] * We    + par[0] * pop + par[3] * Ea    + \
      par[6] * S(We) + par[5] * So  + par[4] * S(Ea)
  Q11 = np.full((m, n), q == par[10])
  Q12 = np.full((m, n), q == par[11])
  return np.logical_or(np.logical_and(pop, Q11), Q12).astype(int)

def fit_life3(par, pop):
  '''
  Given pop (matrix of size m x n and entries in Z3={0, 1, 2}),
  counts the number of 0, 1 and 2 in every neighborhood.
  Then, returns the output for the game of life with 3 colors:
  - 1 if the state is 0, #1 + #2 = 3 and #1 > #2;
  - 2 if the state is 0, #1 + #2 = 3 and #1 < #2;
  - the state if it is more than 0 and 1 < #1 + #2 < 4;
  - 0 otherwise.
  '''
  [m, n] = np.shape(pop)
  
  No = N(pop)
  NE = E(No)
  Ea = E(pop)
  SE = S(Ea)
  So = S(pop)
  SW = W(So)
  We = W(pop)
  NW = N(We)
  
  zeros = (NW == 0).astype(int) + (No == 0).astype(int) + (NE == 0).astype(int) + \
          (We == 0).astype(int) +                         (Ea == 0).astype(int) + \
          (SW == 0).astype(int) + (So == 0).astype(int) + (SE == 0).astype(int)
          
  ones = (NW == 1).astype(int) + (No == 1).astype(int) + (NE == 1).astype(int) + \
         (We== 1).astype(int) +                          (Ea == 1).astype(int) + \
         (SW == 1).astype(int) + (So == 1).astype(int) + (SE == 1).astype(int)
  
  twos = (NW == 2).astype(int) + (No == 2).astype(int) + (NE == 2).astype(int) + \
         (We == 2).astype(int) +                         (Ea == 2).astype(int) + \
         (SW == 2).astype(int) + (So == 2).astype(int) + (SE == 2).astype(int)

  return np.multiply(np.logical_and(pop == 0, ones + twos == 3).astype(int), (twos > ones) + 1) + \
         np.logical_and(pop == 1, np.logical_or(ones + twos == 2, ones + twos == 3)) + \
         np.logical_and(pop == 2, np.logical_or(ones + twos == 2, ones + twos == 3)) * 2


def fit_life4(par, pop):
  '''
  Given pop (matrix of size m x n and entries in Z4={0, 1, 2, 3}),
  counts the number of 1 and 3 in every neighborhood.
  Then, returns the output for the game of life with 4 colors:
  - 0 if the state is 1, #1 != 2, 3 and #3 != 1, 2, 3, 4
      or the state is 3, #3 != 2, 3 and #1 != 1, 2, 3, 4;
  - 1 if the state is 0, #1 = 3 or #1 + #3 = 3;
      or the state is 2, #3 = 3 or #1 + #3 = 3;
  - the state mod 2 otherwise.
  '''
  [m, n] = np.shape(pop)
  
  No = N(pop)
  NE = E(No)
  Ea = E(pop)
  SE = S(Ea)
  So = S(pop)
  SW = W(So)
  We = W(pop)
  NW = N(We)
          
  ones = (NW == 1).astype(int) + (No == 1).astype(int) + (NE == 1).astype(int) + \
         (We == 1).astype(int) +                         (Ea == 1).astype(int) + \
         (SW == 1).astype(int) + (So == 1).astype(int) + (SE == 1).astype(int)

  threes = (NW == 3).astype(int) + (No == 3).astype(int) + (NE == 3).astype(int) + \
           (We == 3).astype(int) +                         (Ea == 3).astype(int) + \
           (SW == 3).astype(int) + (So == 3).astype(int) + (SE == 3).astype(int)

  return np.logical_and(pop == 0, np.logical_or(ones == 3, ones + threes == 3)) + \
         np.logical_and(pop == 1, np.logical_or(np.logical_or(1 < ones, ones < 4),
                                                np.logical_or(0 < threes, threes < 5))) + \
         np.logical_and(pop == 2, np.logical_or(threes == 3, ones + threes == 3)) + \
         np.logical_and(pop == 3, np.logical_or(np.logical_or(1 < threes, threes < 4),
                                                np.logical_or(0 < ones, ones < 5)))

def fit_lifeh(par,pop):
  '''
  Given par (a list of 12 integers) and pop (matrix of size m x n),
  after determining every cell state in the neightborhood modulo
  the 10th parameter, calculates the linear combination of these
  values with the first 9 parameters.
  Then returns the fitness value of each cell, which is is 1 only if:
  - his state is non zero and the l.c. is the 11th parameter;
  - the l.c. is the 12th parameter.
  '''
  [m, n] = np.shape(pop)
  popmod = np.mod(pop, par[9]);

  No = N(popmod)
  So = S(popmod)
  We = W(popmod)
  Ea = E(popmod)
  
  q = par[8] * N(We) + par[1] * No  + par[2] * N(Ea) + \
      par[7] * We    + par[0] * pop + par[3] * Ea    + \
      par[6] * S(We) + par[5] * So  + par[4] * S(Ea)
  Q11 = np.full((m, n), q == par[10])
  Q12 = np.full((m, n), q == par[11])
  return np.logical_or(np.logical_and(pop, Q11), Q12).astype(int)

def fit_metaprime(par,pop):
  '''
  Given par (a list with at least 10 integers, possibly hundreds)
  and pop (matrix of size m x n), calculates the linear combination
  of the states in the neightborhood with the first 9 parameters
  and returns as fitness value the (l.c.+10)th parameter.
  '''
  [m, n] = np.shape(pop)

  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  q = par[8] * N(We) + par[1] * No  + par[2] * N(Ea) + \
      par[7] * We    + par[0] * pop + par[3] * Ea    + \
      par[6] * S(We) + par[5] * So  + par[4] * S(Ea)
  return par[9 + q]

def fit_mod(par,pop):
  '''
  Given par (a list of 10 integers) and pop (matrix of size m x n),
  calculates the linear combination of the states in the neightborhood
  with the first 9 parameters and returns as fitness value the l.c.
  modulo the 10th parameter.
  '''
  [m, n] = np.shape(pop)

  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  q = par[8] * N(We) + par[1] * No  + par[2] * N(Ea) + \
      par[7] * We    + par[0] * pop + par[3] * Ea    + \
      par[6] * S(We) + par[5] * So  + par[4] * S(Ea)
  return np.mod(q, par[9])

def fit_modmod(par, pop):
  '''
  Given par (a list of 11 integers) and pop (matrix of size m x n),
  after determining every cell state in the neightborhood modulo
  the 10th parameter, calculates the linear combination of these
  values with the first 9 parameters and returns as fitness value
  the l.c. modulo the 11th parameter.
  '''
  [m, n] = np.shape(pop)
  pop = np.mod(pop, par[9]);
  
  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  q = par[8] * N(We) + par[1] * No  + par[2] * N(Ea) + \
      par[7] * We    + par[0] * pop + par[3] * Ea    + \
      par[6] * S(We) + par[5] * So  + par[4] * S(Ea)
  return np.mod(q, par[10])

def fit_prime(par, pop):
  '''
  Given par (a list of 9 integers) and pop (matrix of size m x n),
  calculates the linear combination of the states in the neightborhood
  with the 9 parameters and returns 1 if the absolute value of the l.c. 
  is prime, 0 otherwise.
  '''
  [m, n] = np.shape(pop)

  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  q = par[8] * N(We) + par[1] * No  + par[2] * N(Ea) + \
      par[7] * We    + par[0] * pop + par[3] * Ea    + \
      par[6] * S(We) + par[5] * So  + par[4] * S(Ea)
  Q = np.empty([m, n], dtype = int)
  for i in range(m):
    for j in range(n):
      Q[i, j] = int(isprime(int(abs(q[i, j]))))
  return Q

def fit_primes(par, pop):
  '''
  Given par (a list of 9 integers) and pop (matrix of size m x n),
  calculates the linear combination of the states in the neightborhood
  with the 9 parameters and returns the numbers of prime in the set
  {abs(l.c.), abs(l.c.) + 2, abs(l.c.) + 4, abs(l.c.) + 6}.
  '''
  [m, n] = np.shape(pop)

  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  q = par[8] * N(We) + par[1] * No  + par[2] * N(Ea) + \
      par[7] * We    + par[0] * pop + par[3] * Ea    + \
      par[6] * S(We) + par[5] * So  + par[4] * S(Ea)
  Q = np.empty([m, n], dtype = int)
  for i in range(m):
    for j in range(n):
      Q[i, j] = int(isprime(int(abs(q[i, j])))) + \
                int(isprime(int(abs(q[i, j]) + 2))) + \
                int(isprime(int(abs(q[i, j]) + 4))) + \
                int(isprime(int(abs(q[i, j]) + 6)))
  return Q

### GENERATORS OF INITIAL POPULATION ###

def randpop(dim, nstates, seed):
  '''
  Generates a matrix of size dim (list [m, n])
  which entries are integers from 0 to nstates-1
  randomly obtained with the given seed.
  '''
  np.random.seed(seed)
  return np.random.randint(0, nstates, dim)

def randpop1(dim, nstates, fixed, seed):
  '''
  Generates a matrix of size dim (list [m, n])
  which entries are integers from 0 to nstates-1
  randomly obtained with the given seed, except for
  border values that are the given fixed value.
  '''
  np.random.seed(seed)
  pop = np.random.randint(0, nstates, dim)
  pop[0, :] = fixed
  pop[dim[0] - 1, :] = fixed
  pop[:, 0] = fixed
  pop[:, dim[1] - 1] = fixed
  return pop

### CROSSOVER OPERATORS ###

def co_life(nstates, nfit):
  M = np.zeros([nstates, nfit, nstates, nfit], dtype = int)
  for i in range(nfit):
    M[:, i, :, :] = i 
  return M

def co_life3():
  M = co_life(3,3) 
  return M

def co_life4():
  M = co_life(4,2)
  return M
  
def co_second(nstates, nfit):
  M = np.zeros([nstates, nfit, nstates, nfit], dtype = int)
  for i in range(nstates):
    M[:, :, i, :] = i 
  return M

def co_floor(nstates, nfit):
  M = np.zeros([nstates, nfit, nstates, nfit], dtype = int)
  for i in range(nstates):
    for j in range(nstates):
      M[i, :, j, :] = (i + j) // 2
  return M

def co_balance(nstates, nfit):
  M = np.zeros([nstates, nfit, nstates, nfit], dtype = int)
  for i in range(nstates):
    for j in range(nstates):
      if i <= nstates - j:
        M[i, :, j, :] = (i + j) // 2
      else:
        M[i, :, j, :] = math.ceil((i + j) / 2.0)
  return M

def co_ceiling(nstates, nfit):
  M = np.zeros([nstates, nfit, nstates, nfit], dtype = int)
  for i in range(nstates):
    for j in range(nstates):
      M[i, :, j, :] = math.ceil((i + j) / 2.0)
  return M

def co_dynamic(nstates, nfit):
  M = np.zeros([nstates, nfit, nstates, nfit], dtype = int)
  for i in range(nstates):
    for j in range(nstates):
      if i < j:
        M[i, :, j, :] = j - 1
      elif i > j:
        M[i, :, j, :] = j + 1
      else:
        M[i, :, j, :] = i
  return M

def co_lazy(nstates, nfit):
  M = np.zeros([nstates, nfit, nstates, nfit], dtype = int)
  for i in range(nstates):
    for j in range(int(nstates)):
      if i < j:
        M[i, :, j, :] = i + 1
      elif i > j:
        M[i, :, j, :] = i - 1
      else:
        M[i, :, j, :] = i
  return M

### CELLEVOLUTION ###

def cellevolution(pop, shape, grid, ngen, mem, fitfun, par, co, nmut, pmut, seed, color):
  '''
  Main function for cellevolution. Given:
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
  of the last mem generations in two trhee-dimensional matrix of size
  shape(pop) x mem.
  '''
  
  [m, n] = np.shape(pop)
  nstates = np.shape(co)[0]
        
  order = list(range(9))
  
  np.random.seed(seed)
        
  xindex = np.repeat(np.vstack(range(m)), n, axis = 1)
  yindex = np.repeat([range(n)], m, axis = 0)

  savedpop = np.zeros([m, n, mem])
  savedfit = np.zeros([m, n, mem])

  fig = plot.figure()

  fixed = np.empty([m, n])
  if shape == 0:
    R = xindex
    C = yindex
  elif shape == 1:
    R = np.repeat(np.vstack(range(1, m - 1)), n - 2, axis = 1)
    C = np.repeat([range(1, n - 1)], m - 2, axis = 0)
  elif shape == 2:
    R = np.repeat(np.vstack(range(1, m - 1)), n, axis = 1)
    C = np.repeat([range(n)], m - 2, axis = 0)
  else:
    R = np.repeat(np.vstack(range(m)), n - 2, axis = 1)
    C = np.repeat([range(1, n - 1)], m, axis = 0)
  if grid == 1:
    Grid = pop[r - 1 : m : r, c - 1 : n : c]
  
  for i in range(ngen):

    fit = fitfun(par, pop)
      
    popgr = plot.subplot2grid((1, 2), (0, 0))
    popgr.set_title('Population')
    popgr.matshow(pop, cmap = plot.get_cmap(color))
    popgr.axis('off')
    fitgr = plot.subplot2grid((1, 2), (0, 1))
    fitgr.set_title('Fitness')
    fitgr.matshow(fit, cmap = plot.cm.jet)
    fitgr.axis('off')
    fig.canvas.set_window_title('Cellular Evolution - Generation ' + str(i + 1))
    plot.draw()
    plot.pause(0.000000000001)            
    
    if i >= (ngen - mem):
      savedpop[:, :, i - ngen + mem] = pop
      savedfit[:, :, i - ngen + mem] = fit

    random.shuffle(order)

    Np = N(pop)
    Sp = S(pop)
    Wp = W(pop)
    Ep = E(pop)
    
    p = np.empty([9, m, n], dtype = int)
    p[order, :, :] = [pop, Np, N(Ep), Ep, S(Ep), Sp, S(Wp), Wp, N(Wp)]

    Nf = N(fit)
    Sf = S(fit)
    Wf = W(fit)
    Ef = E(fit)
    
    f = np.empty([9, m, n], dtype = int)
    f[order, :, :] = [fit, Nf, N(Ef), Ef, S(Ef), Sf, S(Wf), Wf, N(Wf)]

    selindex = np.argmax(f, axis=0)
    selp = p[selindex, xindex, yindex]
    self = f[selindex, xindex, yindex]

    pop[R, C] = co[pop[R, C].astype(int),
                   fit[R, C].astype(int),
                   selp[R, C].astype(int),
                   self[R, C].astype(int)]

    if pmut > 0:
      if (i + 1) % nmut == 0:
        P = np.greater(np.full([len(R), len(C)], pmut),
                       np.random.rand(len(R), len(C)) * 100)
        pop[R,C] -= np.multiply(P, np.random.randint(0, nstates, [len(R), len(C)]))
        
    if grid == 1:
      pop[r - 1 : m : r, c - 1 : n : c] = Grid
