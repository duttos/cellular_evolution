import math
from sympy import isprime
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.animation as animation
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
  Then returns the fitness value of each cell, which is 1 only if:
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
         (We== 1).astype(int)  +                         (Ea == 1).astype(int) + \
         (SW == 1).astype(int) + (So == 1).astype(int) + (SE == 1).astype(int)
  
  twos = (NW == 2).astype(int) + (No == 2).astype(int) + (NE == 2).astype(int) + \
         (We == 2).astype(int) +                         (Ea == 2).astype(int) + \
         (SW == 2).astype(int) + (So == 2).astype(int) + (SE == 2).astype(int)

  return np.multiply(np.logical_and(pop == 0, ones + twos == 3).astype(int), (twos > ones) + 1) + \
         np.logical_and(pop == 1, np.logical_or(ones + twos == 2, ones + twos == 3)).astype(int) + \
         np.logical_and(pop == 2, np.logical_or(ones + twos == 2, ones + twos == 3)).astype(int) * 2


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

  return np.logical_and(pop == 0, np.logical_or(ones == 3, ones + threes == 3)).astype(int) + \
         np.logical_and(pop == 1, np.logical_or(np.logical_and(1 < ones, ones < 4),
                                                np.logical_and(0 < threes, threes < 5))).astype(int) + \
         np.logical_and(pop == 2, np.logical_or(threes == 3, ones + threes == 3)).astype(int) + \
         np.logical_and(pop == 3, np.logical_or(np.logical_and(1 < threes, threes < 4),
                                                np.logical_and(0 < ones, ones < 5)).astype(int))

def fit_lifeh(par,pop):
  '''
  Given par (a list of 12 integers) and pop (matrix of size m x n),
  after determining every cell state in the neightborhood modulo
  the 10th parameter, calculates the linear combination of these
  values with the first 9 parameters.
  Then returns the fitness value of each cell, which is 1 only if:
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
  
def fit_prisoner(par, pop):
  '''
  In the population there are cooperative prisoners (state = 0) and
  traitorous prisoners (state = 1). Given 4 parameters representing:
  - the gain for cooperating with a cooperative neighbor
  - the gain for cooperating with traitorous neighbor
  - the gain for betraying a cooperative neighbor
  - the gain for betrying a traitorous neighbor
  the fitness is given by:
  - par[0] * ncoop + par[1] * nbetr, if the cell is cooperative
  - par[2] * ncoop + par[3] * nbetr, if the cell is traitorous
  '''
  [m, n] = np.shape(pop)

  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  nbetr = N(We) + No  + N(Ea) + \
          We    +       Ea    + \
          S(We) + So  + S(Ea)
  ncoop = 8 - nbetr
  coops = (pop == 0).astype(int)	
  return np.multiply(coops, par[0] * ncoop + par[1] * nbetr) + \
         np.multiply(pop, par[2] * ncoop + par[3] * nbetr)

def fit_prisoner1cons(par, pop):
  '''
  In the population there are cooperative prisoners (state = 0) and
  traitorous prisoners (state = 1). Given 4 parameters representing:
  - the gain for cooperating with a cooperative neighbor
  - the gain for cooperating with traitorous neighbor
  - the gain for betraying a cooperative neighbor
  - the gain for betrying a traitorous neighbor
  - a rate of consumption for all prisoners
  the fitness is given by:
  - par[0] * ncoop + par[1] * nbetr - par[4], if the cell is cooperative
  - par[2] * ncoop + par[3] * nbetr - par[4], if the cell is traitorous
  If the fitness value becomes negative, the returned value is 0.
  '''
  [m, n] = np.shape(pop)

  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  nbetr = N(We) + No  + N(Ea) + \
          We    +       Ea    + \
          S(We) + So  + S(Ea)
  ncoop = 8 - nbetr
  coops = (pop == 0).astype(int)	
  return np.maximum(np.multiply(coops, par[0] * ncoop + par[1] * nbetr) + \
                    np.multiply(pop, par[2] * ncoop + par[3] * nbetr) - par[4], \
                    0)
  
def fit_prisoner2cons(par, pop):
  '''
  In the population there are cooperative prisoners (state = 0) and
  traitorous prisoners (state = 1). Given 4 parameters representing:
  - the gain for cooperating with a cooperative neighbor
  - the gain for cooperating with traitorous neighbor
  - the gain for betraying a cooperative neighbor
  - the gain for betrying a traitorous neighbor
  - a rate of consumption for cooperative prisoners
  - a rate of consumption for traitorous prisoners
  the fitness is given by:
  - par[0] * ncoop + par[1] * nbetr - par[4], if the cell is cooperative
  - par[2] * ncoop + par[3] * nbetr - par[5], if the cell is traitorous
  If the fitness value becomes negative, the returned value is 0.
  '''
  [m, n] = np.shape(pop)

  No = N(pop)
  So = S(pop)
  We = W(pop)
  Ea = E(pop)
  
  nbetr = N(We) + No  + N(Ea) + \
          We    +       Ea    + \
          S(We) + So  + S(Ea)
  ncoop = 8 - nbetr
  coops = (pop == 0).astype(int)		
  return np.maximum(np.multiply(coops, par[0] * ncoop + par[1] * nbetr - par[4]) + \
                    np.multiply(pop, par[2] * ncoop + par[3] * nbetr - par[5]), \
                    0)
                    
def fit_rps(par, pop):
  '''
  In the population there are scissors (state = 0), papers (state = 1) and 
  rocks (state = 2). Given 3 gain paramenters (relative to scissors, paper
  and rock wins, respectively) returns the total gain for each cell.
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
  
  scissors = (pop == 0).astype(int)
  papers = (pop == 1).astype(int)
  rocks = (pop == 2).astype(int)

  nsc = (NW == 0).astype(int) + (No == 0).astype(int) + (NE == 0).astype(int) + \
        (We == 0).astype(int) + scissors              + (Ea == 0).astype(int) + \
        (SW == 0).astype(int) + (So == 0).astype(int) + (SE == 0).astype(int)

  npa = (NW == 1).astype(int) + (No == 1).astype(int) + (NE == 1).astype(int) + \
        (We == 1).astype(int) + papers                + (Ea == 1).astype(int) + \
        (SW == 1).astype(int) + (So == 1).astype(int) + (SE == 1).astype(int)

  nro = (NW == 2).astype(int) + (No == 2).astype(int) + (NE == 2).astype(int) + \
        (We == 2).astype(int) + rocks                 + (Ea == 2).astype(int) + \
        (SW == 2).astype(int) + (So == 2).astype(int) + (SE == 2).astype(int)
       
  return par[0] * np.multiply(scissors, npa) + \
         par[1] * np.multiply(papers, nro) + \
         par[2] * np.multiply(rocks, nsc)
         
def fit_nrps(par, pop):
  '''
  Gereralization of rock-paper-scissors for n inputs.
  In the given n parameters, the i-th one represents the 
  gain for the win of state i over state i + 1. There is 
  no gain for encounters between non-consecutive inputs.
  The fitness value is the total gain.
  '''
  [nrow, ncol] = np.shape(pop)
  n = np.shape(par)[0]
  
  inputs = np.zeros([nrow, ncol, n], dtype = int)
  ninputs = np.zeros([nrow, ncol, n], dtype = int)
  gain = np.zeros([nrow, ncol], dtype = int)
  
  for i in range(n):
    inputs[:, :, i] = (pop == i).astype(int)
    No = N(inputs[:, :, i])
    So = S(inputs[:, :, i])
    We = W(inputs[:, :, i])
    Ea = E(inputs[:, :, i])
    ninputs[:, :, i] = N(We) + No              + N(Ea) + \
                       We    + inputs[:, :, i] + Ea    + \
                       S(We) + So              + S(Ea)
  
  for i in range(n - 1):
    gain = np.add(gain, par[i] * np.multiply(inputs[:, :, i], ninputs[:, :, i + 1]))
    
  return gain + par[n - 1] * np.multiply(inputs[:, :, n - 1], ninputs[:, :, 0])
         
def fit_nrpsthres(par, pop):
  '''
  Gereralization of rock-paper-scissors for n inputs.
  In the given n + 1 parameters, the i-th one represents the 
  gain for the win of state i over state i + 1. There is 
  no gain for encounters between non-consecutive inputs.
  The last parameter is a threshold. If the total gain is
  less than the threshold then the fitness is 0, otherwise
  the fitness is 1.
  '''
  [nrow, ncol] = np.shape(pop)
  n = np.shape(par)[0] - 1
  
  inputs = np.zeros([nrow, ncol, n], dtype = int)
  ninputs = np.zeros([nrow, ncol, n], dtype = int)
  gain = np.zeros([nrow, ncol], dtype = int)
  
  for i in range(n):
    inputs[:, :, i] = (pop == i).astype(int)
    No = N(inputs[:, :, i])
    So = S(inputs[:, :, i])
    We = W(inputs[:, :, i])
    Ea = E(inputs[:, :, i])
    ninputs[:, :, i] = N(We) + No              + N(Ea) + \
                       We    + inputs[:, :, i] + Ea    + \
                       S(We) + So              + S(Ea)
  
  for i in range(n - 1):
    gain = np.add(gain, par[i] * np.multiply(inputs[:, :, i], ninputs[:, :, i + 1]))
  gain = np.add(gain, par[n - 1] * np.multiply(inputs[:, :, n - 1], ninputs[:, :, 0]))
    
  return (gain > par[n]).astype(int)
          
### GENERATORS OF INITIAL POPULATION ###

def pop_rand(dim, max_pop, seed):
  '''
  Generates a matrix of size dim (list [m, n])
  which entries are integers from 0 to max_pop
  randomly obtained with the given seed.
  '''
  np.random.seed(seed)
  return np.random.randint(0, max_pop + 1, dim)

def pop_bordered(dim, max_pop, fixed, seed):
  '''
  Generates a matrix of size dim (list [m, n])
  which entries are integers from 0 to max_pop
  randomly obtained with the given seed, except for
  border values that are the given fixed value.
  '''
  np.random.seed(seed)
  pop = np.random.randint(0, max_pop + 1, dim)
  pop[0, :] = fixed
  pop[dim[0] - 1, :] = fixed
  pop[:, 0] = fixed
  pop[:, dim[1] - 1] = fixed
  return pop

def life3_glidergun(m, n):
  '''
  Generates the initial population of size [m, n] that 
  works as a glider gun with the 3-life variant of GoL.
  '''
  pop = np.zeros([m, n], dtype = int)
  pop[6, 2] = 1
  pop[7, 2] = 2
  pop[6, 3] = 2
  pop[7, 3] = 1
  pop[6:9, 12] = 2
  pop[5, 13] = 2
  pop[9, 13] = 1
  pop[4, 14:16] = 2
  pop[10, 14:16] = 2
  pop[7, 16] = 1
  pop[5, 17] = 1
  pop[9, 17] = 2
  pop[6, 18] = 1
  pop[8, 18] = 2
  pop[7, 18:20] = 1
  pop[4:7, 22:24] = 1
  pop[3, 24] = 1
  pop[7, 24] = 2
  pop[2:4, 26] = 1
  pop[7:9, 26] = 2
  pop[4, 36] = 1
  pop[5, 36] = 2
  pop[4, 37] = 2
  pop[5, 37] = 1
  return pop
      
def life4_generator(m, n):
  '''
  Generates the initial population of size [m, n] that 
  works as life generator with the 4-life variant of GoL.
  '''
  pop = np.zeros([m, n], dtype = int)
  midrow = m // 2
  midcol = n // 2
  pop[midrow - 3, midcol - 1] = 3
  pop[midrow - 3, midcol + 1] = 3
  pop[midrow - 1, (midcol - 1):(midcol + 2)] = 3
  pop[midrow + 1, (midcol - 1):(midcol + 2)] = 3
  pop[midrow + 3, midcol:(midcol + 2)] = 3
  return pop
  
def pd_0square(m, n):
  '''
  Generates a population of size [m, n] 
  with all states 1 except for the center 
  2x2 square that has value 0.
  '''
  pop = np.ones([m, n])
  midrow = m // 2
  midcol = n // 2
  pop[(midrow - 1):(midrow + 1), (midcol - 1):(midcol + 1)] = 0
  return pop
  
def pd_1square(m, n):
  '''
  Generates a population of size [m, n] 
  with all states 0 except for the center 
  2x2 square that has value 1.
  '''
  pop = np.zeros([m, n])
  midrow = m // 2
  midcol = n // 2
  pop[(midrow - 1):(midrow + 1), (midcol - 1):(midcol + 1)] = 1
  return pop
  
def rps_glider1(m, n):
  '''
  Generates a population of size [m, n] with a glider for 
  the rock-paper-scissors system with fit_rps, parameters 
  [1, 1.1, 1.2], and co_selected.
  '''
  pop = np.zeros([m, n], dtype = int)
  pop[2, 2:7] = 1
  pop[3, 2] = 1
  pop[3, 3:6] = 2
  pop[3, 6] = 1
  pop[4, 2] = 1
  pop[4, 3:6] = 2
  pop[4, 6] = 1
  pop[5, 2] = 1
  pop[5, 3:6] = 2
  pop[6, 2:5] = 1
  return pop
  
def rps_glider2(m, n):
  '''
  Generates a population of size [m, n] with a 
  glider for the rock-paper-scissors system with 
  fit_rps, parameters [1, 2, 3] and co_selected.
  '''
  pop = np.zeros([m, n], dtype = int)
  pop[2:8, 2:8] = 1
  pop[7, 1] = 0
  pop[1, 7] = 0
  pop[6:8, 7] = 0
  pop[7, 6] = 0
  pop[4:7, 4:7] =2 
  return pop
  
def rps_generator(m, n):
  '''
  Generates a population of size [m, n] with a 
  life generator for the rock-paper-scissors system 
  with fit_rps, parameters [1.7, 3, 5] and co_selected.
  '''
  pop = np.zeros([m, n], dtype = int)
  midrow = m // 2
  midcol = n // 2
  pop[midrow - 2, (midcol - 4):(midcol + 1)] = 1
  pop[midrow, (midcol - 4):(midcol - 1)] = 1
  pop[midrow, midcol:(midcol + 3)] = 1
  pop[midrow + 1, (midcol - 5):(midcol + 4)] = 2
  pop[midrow + 2, (midcol - 4):(midcol - 2)] = 2
  pop[midrow + 2, (midcol - 2):(midcol + 1)] = 1
  pop[midrow + 2, (midcol + 1):(midcol + 4)] = 2
  pop[midrow + 2, midcol + 4] = 1
  return pop
  
def rps_midglider1(m, n):
  '''
  Generates a population of size [m, n] with at the center
  a glider for the rock-paper-scissors system with fit_rps, 
  parameters [1, 1.1, 1.2], and co_selected.
  It works as a life generator when co_fitequable is used.
  '''
  pop = np.zeros([m, n], dtype = int)
  midrow = m // 2 - 5
  midcol = n // 2 - 5
  pop[midrow:(midrow + 10), midcol:(midcol + 10)] = rps_glider1(10, 10)
  return pop
  
### CROSSOVER OPERATORS ###

def co_life(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover used for the implementation of Game of Life,
  it returns as new state its current fitness value.
  '''
  return fit

def co_life4(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover used for the implementation of the variant of 
  Game of Life with 4 states, it returns as new state:
  - 0 if the previous state is 0 or 1 and the fitness is 0
  - 1 if the previous state is 0 or 1 and the fitness is 1
  - 2 if the previous state is 2 or 3 and the fitness is 0
  - 3 if the previous state is 2 or 3 and the fitness is 1
  '''
  
  pop0 = (pop == 0).astype(int)
  pop1 = (pop == 1).astype(int)
  pop2 = (pop == 2).astype(int)
  pop3 = (pop == 3).astype(int)
  
  fit0 = (fit == 0).astype(int)
  fit1 = (fit == 1).astype(int)
  
  [m, n] = np.shape(pop)
  M = np.zeros([m, n])
  
  M = M + np.multiply(pop0, fit1) + np.multiply(pop1, fit1) + \
          (np.multiply(pop2, fit0) + np.multiply(pop3, fit0)) * 2 + \
          (np.multiply(pop2, fit1) + np.multiply(pop3, fit1)) * 3
  
  return M
  
def co_selected(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state that of the selected cell.
  '''
  return sel_pop

def co_floor(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state the arithmetic mean between
  the old state and the one of the selected cell, rounded down.
  '''
  return (pop + sel_pop) // 2

def co_equable(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state the arithmetic mean between
  the old state and that of the selected cell, rounded down if their
  sum is equal or below the maximum state and rounded up elsewhere.
  '''
  tot = pop + sel_pop
  tot_down = (tot <= max_pop).astype(int)
  tot_up = (tot > max_pop).astype(int)
  
  return np.multiply(tot_down, tot // 2) + \
         np.multiply(tot_up, np.ceil(tot / 2.0))
  
def co_ceil(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state the arithmetic mean between
  the old state and that of the selected cell, rounded up.
  '''
  return np.ceil((pop + sel_pop) / 2.0)

def co_dynamic(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state:
  - the old state if it is equal to the state of the selected cell
  - the selected cell state minus one if it is greater than the old state
  - the selected cell state plus one if it is smaller than the old state
  '''
  pop_down = (pop < sel_pop).astype(int)
  pop_same = (pop == sel_pop).astype(int)
  pop_up = (pop > sel_pop).astype(int)
  
  return np.multiply(pop_down, sel_pop - 1) + \
         np.multiply(pop_same, pop) + \
         np.multiply(pop_up, sel_pop + 1) 

def co_lazy(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state:
  - the old state if it is equal to that of the selected cell
  - the old state minus one if it is greater than the selected cell state
  - the old state plus one if it is smaller than the selected cell state
  '''
  pop_down = (pop < sel_pop).astype(int)
  pop_same = (pop == sel_pop).astype(int)
  pop_up = (pop > sel_pop).astype(int)
  
  return np.multiply(pop_down, pop + 1) + \
         np.multiply(pop_same, pop) + \
         np.multiply(pop_up, pop - 1) 
  
def co_fitselect(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns the old state if its fitness is equal or
  greater than that of the selected cell or equal to it, and the 
  state of the selected cell otherwise.
  '''
  return np.multiply((fit >= sel_fit).astype(int), pop) + \
         np.multiply((fit < sel_fit).astype(int), sel_pop)
  
def co_fitfloor(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state the fitness weighed mean between
  the old state and that of the selected cell, rounded down.
  '''
  tot = fit + sel_fit
  zeros = (tot == 0).astype(int)
  nonzeros = (tot != 0).astype(int)
  tot_no0 = tot + zeros
  
  return np.multiply(nonzeros, \
                     (np.multiply(pop, fit) + np.multiply(sel_pop,sel_fit)) // tot_no0)

def co_fitequable(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state the fitness weighed mean between
  the old state and that of the selected cell, rounded down if their 
  sum is equal or below the maximum state and rounded up elsewhere.
  '''
  tot_pop = pop + sel_pop
  tot_down = (tot_pop <= max_pop).astype(int)
  tot_up = (tot_pop > max_pop).astype(int)
  wtot = np.multiply(pop, fit) + np.multiply(sel_pop,sel_fit)
  
  tot_fit = fit + sel_fit
  zeros = (tot_fit == 0).astype(int)
  nonzeros = (tot_fit != 0).astype(int)
  tot_no0 = tot_fit + zeros
  
  return np.multiply(nonzeros, \
                     np.multiply(tot_down, wtot // tot_no0) + \
                     np.multiply(tot_up, np.ceil(wtot / tot_no0)))
  
def co_fitceil(pop, fit, sel_pop, sel_fit, max_pop, max_fit):
  '''
  Crossover that returns as new state the fitness weighed mean between
  the old state and that of the selected cell, rounded up.
  '''
  tot = fit + sel_fit
  zeros = (tot == 0).astype(int)
  nonzeros = (tot != 0).astype(int)
  tot_no0 = tot + zeros
  
  return np.multiply(nonzeros, \
                     np.ceil((np.multiply(pop, fit) + np.multiply(sel_pop,sel_fit)) / tot_no0))

### CELLEVOLUTION ###

def cellevolution(pop, max_pop, shape, grid, ngen, mem, fitfun, par, max_fit, co, nmut, pmut, seed, color):
  '''
  Main function for cellevolution. Given:
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
  
  Examples: 
  START WITH 
  >>> import cellevolution as ce
  - classic Game of Life (Conway)
    >>> [p, f] = ce.cellevolution(ce.pop_rand([100, 100], 1, 3), 1, 't', [False, 0, 0], 500, 500, \
                                  ce.fit_life, [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 3], 1, \
                                  ce.co_life, 10, 0.01, 3, 'nipy_spectral')
  - 3-life variant glider gun
    >>> [p, f] = ce.cellevolution(ce.life3_glidergun(50, 50), 2, 'c', [False, 0, 0], 300, 300, \
                                  ce.fit_life3, [], 1, \
                                  ce.co_life, 0, 0, 3, "nipy_spectral")
  - 4-life variant life generator
    >>> [p, f] = ce.cellevolution(ce.life4_generator(100, 100), 3, 'c', [False, 0, 0], 500, 500, \
                                  ce.fit_life4, [], 1, \
                                  ce.co_life4, 0, 0, 3, "nipy_spectral")
  - prisoner's dilemma kaleidoscope
    >>> [p, f] = ce.cellevolution(ce.pd_1square(100, 100), 1, 't', [False, 0, 0], 1000, 1000, \
                                  ce.fit_prisoner, [1, 0, 1.65, 0], 22, \
                                  ce.co_selected, 0, 0.01, 3, "nipy_spectral")
  - prisoner's dilemma flashing kaleidoscope
    >>> [p, f] = ce.cellevolution(ce.pd_1square(100, 100), 1, 't', [False, 0, 0], 1000, 1000, \
                                  ce.fit_prisoner, [1, 0, 2.5, 0], 22, \
                                  ce.co_fitceil, 0, 0.01, 3, "nipy_spectral")
  - classic rock-paper-scissors
    >>> [p, f] = ce.cellevolution(ce.pop_rand([100, 100], 2, 3), 2, 't', [False, 0, 0], 1000, 1000, \
                                  ce.fit_rps, [1, 1, 1], 8, \
                                  ce.co_selected, 0, 0.01, 3, "nipy_spectral")
  - rock-paper-scissors glider with period 4
    >>> [p, f] = ce.cellevolution(ce.rps_glider1(100,100), 2, 't', [False, 0, 0], 100, 100, \
                                  ce.fit_rps, [1, 1.1, 1.2], 10, \
                                  ce.co_selected, 0, 0.01, 3, "nipy_spectral")     
  - rock-paper-scissors pseudo-glider
    >>> [p, f] = ce.cellevolution(ce.rps_glider1(20, 20), 2, 't', [False, 0, 0], 100, 100, \
                                  ce.fit_rps, [1, 1.5, 2], 16, \
                                  ce.co_selected, 0, 0.01, 3, "nipy_spectral")
  - rock-paper-scissors glider with period 1
    >>> [p, f] = ce.cellevolution(ce.rps_glider2(20, 20), 2, 't', [False, 0, 0], 100, 100, \
                                  ce.fit_rps, [1, 2, 3], 24, \
                                  ce.co_selected, 0, 0.01, 3, "nipy_spectral")   
  - rock-paper-scissors life generator
    >>> [p, f] = ce.cellevolution(ce.rps_generator(100, 100), 2, 't', [False, 0, 0], 40, 40, \
                                  ce.fit_rps, [1.7, 3, 5], 40, \
                                  ce.co_selected, 0, 0.01, 3, "nipy_spectral")
  - rock-paper-scissors life generator with co_fitequable
    >>> [p, f] = ce.cellevolution(ce.rps_midglider1(200, 200), 2, 't', [False, 0, 0], 100, 100, \
                                  ce.fit_rps, [1, 1.1, 1.2], 10, \
                                  ce.co_fitequable, 0, 0.01, 3, "nipy_spectral")
  '''
  
  [m, n] = np.shape(pop)
        
  order = list(range(9))
  
  random.seed(seed)
        
  xindex = np.repeat(np.vstack(range(m)), n, axis = 1)
  yindex = np.repeat([range(n)], m, axis = 0)

  savedpop = np.zeros([mem, m, n])
  savedfit = np.zeros([mem, m, n])

  fixed = np.empty([m, n])
  if shape == 't':
    R = xindex
    C = yindex
  elif shape == 'c':
    R = np.repeat(np.vstack(range(1, m - 1)), n - 2, axis = 1)
    C = np.repeat([range(1, n - 1)], m - 2, axis = 0)
  elif shape == 'v':
    R = np.repeat(np.vstack(range(1, m - 1)), n, axis = 1)
    C = np.repeat([range(n)], m - 2, axis = 0)
  elif shape == 'h':
    R = np.repeat(np.vstack(range(m)), n - 2, axis = 1)
    C = np.repeat([range(1, n - 1)], m, axis = 0)
  if grid == True:
    Grid = pop[r - 1 : m : r, c - 1 : n : c]

  plot.close('all')
  fig, (ax1, ax2) = plot.subplots(1, 2)

  ax1.set_title('Population')
  ax1.axis('off')
  popgr = ax1.matshow(np.zeros([m,n]),
                      cmap = plot.get_cmap(color), vmin = 0, vmax = max_pop)

  ax2.set_title('Fitness')
  ax2.axis('off')
  fitgr = ax2.matshow(np.zeros([m,n]),
                      cmap = plot.cm.nipy_spectral, vmin = 0, vmax = max_fit)
  
  for i in range(ngen):

    fit = fitfun(par, pop)
    
    fig.suptitle('Cellular Evolution - Generation ' + str(i + 1))
    popgr.set_data(pop)
    fitgr.set_data(fit)
    plot.pause(0.01)
    
    if i >= (ngen - mem):
      savedpop[i - ngen + mem, :, :] = pop
      savedfit[i - ngen + mem, :, :] = fit

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
    
    f = np.empty([9, m, n])
    f[order, :, :] = [fit, Nf, N(Ef), Ef, S(Ef), Sf, S(Wf), Wf, N(Wf)]

    selindex = np.argmax(f, axis=0)
    sel_pop = p[selindex, xindex, yindex]
    sel_fit = f[selindex, xindex, yindex]
    
    pop[R, C] = co(pop[R, C], fit[R, C],
                   sel_pop[R, C], sel_fit[R, C],
                   max_pop, max_fit)

    if nmut > 0 and pmut > 0:
      if (i + 1) % nmut == 0:
        P = np.greater(np.full([len(R), len(C)], pmut),
                       np.random.rand(len(R), len(C)) * 100)
        pop[R,C] -= np.multiply(P, np.random.randint(0, max_pop + 1, [len(R), len(C)]))
        
    if grid == 1:
      pop[r - 1 : m : r, c - 1 : n : c] = Grid
  
  plot.show()
  
  return [savedpop, savedfit]
  
def make_video(savedpop, savedfit, max_pop, max_fit, color, path):
  '''
  Create a mp4 file from the savedpop and savedfit matrices.
  The same max_pop, max_fit and color for cellevolution are 
  also required, as well as the path of an existing folder
  with the name of the mp4 file (e.g., '../video/name.mp4').
  ATTENTION: the creation of a mp4 requires ffmpeg.
  '''
  
  # animation function.  This is called sequentially
  def animate(i):
    
    pop = savedpop[i, :, :]
    fit = savedfit[i, :, :]
    
    fig.suptitle('Cellular Evolution - Generation ' + str(i + 1))
    popgr.set_data(pop)
    fitgr.set_data(fit)
    
    return popgr, fitgr
    
  [mem, m, n] = np.shape(savedpop)
  
  plot.close('all')
  fig, (ax1, ax2) = plot.subplots(1, 2)
  
  ax1.set_title('Population')
  ax1.axis('off')
  popgr = ax1.matshow(np.zeros([m,n]),
                      cmap = plot.get_cmap(color), vmin = 0, vmax = max_pop)
  pticks = range(max_pop + 1)
  pbar = fig.colorbar(popgr, ax = ax1, orientation = 'horizontal', ticks = pticks)

  ax2.set_title('Fitness')
  ax2.axis('off')
  fitgr = ax2.matshow(np.zeros([m,n]),
                      cmap = plot.cm.nipy_spectral, vmin = 0, vmax = max_fit)
  fbar = fig.colorbar(fitgr, ax = ax2, orientation = 'horizontal')
  
  # call the animator
  anim = animation.FuncAnimation(fig, animate,
                                 frames = mem, interval = 50, repeat = False)
  anim.save(path)
  
