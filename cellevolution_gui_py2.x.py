import Tkinter as tk
import tkMessageBox
from tkSimpleDialog import askinteger
import math
from sympy import isprime
import numpy as np
import matplotlib.pyplot as plt
from ttk import Combobox
import random

# GENERAL FUNCTIONS

def center(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry('{}x{}+{}+{}'.format(w, h, x, y))

def convmatstr(M):
    s=''
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            s=s+'  '+str(int(M[i,j]))
        s=s+'\n'
    return s

def int_input(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

def num_input(val):
    try:
        float(val)
        return True
    except ValueError:
        if val == '':
            return True
        else:
            return False

# PARTICULAR CASES FUNCTIONS

def PCinfo():
    tkMessageBox.showinfo('Cellular Evolution', \
                          'Here are some prefinite cases:\n'\
                          '- Game of Life: the original Conway creation\n'\
                          '- Game of Life (3 col.):\n'\
                          'two lifes (with values 0/1 and 0/2) interacting\n'\
                          '- Game of Life (4 col.):\n'\
                          'two lifes (with values 0/1 and 2/3) interacting\n')

def cases(event):
    global ff
    global par
    global num_col
    global fitmsg
    global op
    global comsg
    global s
    PCcheck.select()
    check[11] = 1
    if PCcombo.current()==0:
        FFbutton2.config(state='disabled')
        FFcheck.select()
        check[0] = 1
        CMbutton2.config(state='disabled')
        CMcheck.select()
        check[1] = 1
        IPbutton2.config(state='normal')
        IPcheck.deselect()
        check[2] = 0
        ff=1
        par=[1,1,1,1,1,1,1,1,1,2,4,3]
        num_col=2
        s=0
        fitmsg='Game of Life'
        op=np.zeros((2,2,2,2))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        op[i,j,k,l] = j
        comsg='Game of Life'
    elif PCcombo.current()==2:
        FFbutton2.config(state='disabled')
        FFcheck.select()
        check[0] = 1
        CMbutton2.config(state='disabled')
        CMcheck.select()
        check[1] = 1
        IPbutton2.config(state='normal')
        IPcheck.deselect()
        check[2] = 0
        ff=8
        par=[]
        num_col=2
        s=0
        fitmsg='Game of Life (4 col.)'
        op=np.zeros((4,2,4,2))
        for j in range(2):
            for k in range(4):
                for l in range(2):
                    op[0,j,k,l] = j
                    op[1,j,k,l] = j
                    op[2,j,k,l] = j+2
                    op[3,j,k,l] = j+2
        comsg='Game of Life (4 col.)'
    elif PCcombo.current()==1:
        FFbutton2.config(state='disabled')
        FFcheck.select()
        check[0] = 1
        CMbutton2.config(state='disabled')
        CMcheck.select()
        check[1] = 1
        IPbutton2.config(state='normal')
        IPcheck.deselect()
        check[2] = 0
        ff=9
        par=[]
        num_col=3
        s=0
        fitmsg='Game of Life(3 col.)'
        op=np.zeros((3,3,3,3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        op[i,j,k,l] = j
        comsg='Game of Life (3 col.)'
    else:
        FFbutton2.config(state='normal')
        FFcheck.deselect()
        check[0] = 0
        CMbutton2.config(state='disabled')
        CMcheck.deselect()
        check[1] = 0
        IPbutton2.config(state='disabled')
        IPcheck.deselect()
        check[2] = 0

# FITNESS FUNCTION FUNCTIONS

def FFinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                    'The fitness function indicates the cell predispotion to interact.')

def FF():

    global ff
    ff=1
    global num_col
    num_col=2
         
    fitness = tk.Toplevel(main)
    
    fitness.wm_title('Fitness Function')
    fitframe = tk.Frame(fitness, width = 515, height = 500)
    fitframe.pack(expand='true')
    center(fitness)

    FFcheck.deselect()
    check[0] = 0
    CMcheck.deselect()
    check[1] = 0
    CMbutton2.config(state='disabled')
    IPcheck.deselect()
    check[2] = 0
    IPbutton2.config(state='disabled')
    
    FFintrolabel1 = tk.Label(fitframe, justify='left',\
    text='The fitness function associates a fitness value to any cell of the population.\n'\
         'During the process, at any instant, every cell will select as a partner the\n'\
         'first cell in its Moore neightborhood that has maximum fitness value.')
    FFintrolabel1.grid(row=0, column=0, sticky='W', columnspan=3)

    FFintrolabel2 = tk.Label(fitframe, justify='left',\
    text='In every neightborhood the used order is given by:')
    FFintrolabel2.grid(row=2, column=0, sticky='W', columnspan=2)

    FFintrolabel3 = tk.Label(fitframe, justify='center',\
    text='9  2  3\n8  1  4\n7  6  5')
    FFintrolabel3.grid(row=1, column=2, rowspan=3)

    FFintrolabel4 = tk.Label(fitframe, justify='left',\
    text='Every type of fitness function listed below depends form a list of parameters.\n'\
         'They are at least 9 and everyone is a positive integer.\n'\
         'You have also to insert a seed for the random selection of the fittest mate.\n\n'\
         'Choose one of the following fitness function:')
    FFintrolabel4.grid(row=4, column=0, sticky='W', columnspan=3)

    Infolabel = tk.Label(fitframe, justify='left', width=45)
    Infolabel.grid(row=5,column=1,rowspan=7,columnspan=2,sticky='W')
    Infolabel.config(text = 'Function to {0,1} that needs 12 parameters.\n'\
           'After determining every cell state in the\n'\
           'neightborhood modulo the 10th parameter,\n'\
           'it calculates the linear combination of\n'\
           'this values with the first 9 parameters.\n'\
           'The fitness value of the cell is 1 only if:\n'\
           '- his state modulo the 10th parameter is\n'\
           '  non zero and the l.c. is the 11th parameter\n'\
           '- the l.c. is the 12th parameter\n')
            
    def lifesel():
        ex='Function to {0,1} that needs 12 parameters.\n'\
           'After determining every cell state in the\n'\
           'neightborhood modulo the 10th parameter,\n'\
           'it calculates the linear combination of\n'\
           'this values with the first 9 parameters.\n'\
           'The fitness value of the cell is 1 only if:\n'\
           '- his state modulo the 10th parameter is\n'\
           '  non zero and the l.c. is the 11th parameter\n'\
           '- the l.c. is the 12th parameter\n'
        Infolabel.config(text = ex)
        global ff
        ff = 1
        
    Lifebutton = tk.Radiobutton(fitframe, text='Life Fitness',\
                                  value=1, command=lifesel)
    Lifebutton.grid(row=5, column =0, sticky='W')
    Lifebutton.select()
    
    def lifehsel():
        ex='Function to {0,1} that needs 12 parameters.\n'\
           'After determining every cell state in the\n'\
           'neightborhood modulo the 10th parameter,\n'\
           'it calculates the linear combination of\n'\
           'this values with the first 9 parameters.\n'\
           'The fitness value of the cell is 1 only if:\n'\
           '- his state is non zero and the l.c. is\n'\
           '  the 11th parameter\n'\
           '- the l.c. is the 12th parameter\n'
        Infolabel.config(text = ex)
        global ff
        ff = 2
        
    Lifehbutton = tk.Radiobutton(fitframe, text='Lifeh Fitness',\
                                  value=2, command=lifehsel)
    Lifehbutton.grid(row=6, column =0, sticky='W')

    def metasel():
        ex='Function that needs lots of parameters.\n'\
           'It calculates the linear combination of\n'\
           'the states in the neightborhood with the\n'\
           'first 9 parameters and return as fitness\n'\
           'value the (l.c.+10)th parameter.\n'
        Infolabel.config(text = ex)
        global ff
        ff = 3
        
    Metabutton = tk.Radiobutton(fitframe, text='Metaprimes Fitness',\
                                  value=3, command=metasel)
    Metabutton.grid(row=7, column =0, sticky='W')

    def modsel():
        ex='Function that needs 10 parameters.\n'\
           'It calculates the linear combination of\n'\
           'the states in the neightborhood with the\n'\
           'first 9 parameters and return as fitness\n'\
           'value the l.c. modulo the 10th parameter.\n'
        Infolabel.config(text = ex)
        global ff
        ff = 4
        
    Modbutton = tk.Radiobutton(fitframe, text='Mod Fitness',\
                                  value=4, command=modsel)
    Modbutton.grid(row=8, column =0, sticky='W')

    def modmodsel():
        ex='Function that needs 11 parameters.\n'\
           'After determining every cell state in the\n'\
           'neightborhood modulo the 10th parameter,\n'\
           'it calculates the linear combination of\n'\
           'these values with the first 9 parameters\n'\
           'and return as fitness value the l.c.\n'\
           'modulo the 11th parameter.\n'
        Infolabel.config(text = ex)
        global ff
        ff = 5
        
    Modmodbutton = tk.Radiobutton(fitframe, text='Mod Mod Fitness',\
                                  value=5, command=modmodsel)
    Modmodbutton.grid(row=9, column =0, sticky='W')

    def primesel():
        ex='Function to {0,1} that needs 9 parameters.\n'\
           'It calculates the linear combination of\n'\
           'the states in the neightborhood with the\n'\
           'first 9 parameters and return as fitness\n'\
           'value 1 if the absolute value of the l.c.\n'\
           'is prime and 0 otherwise.'
        Infolabel.config(text = ex)
        global ff
        ff = 6
        
    Primebutton = tk.Radiobutton(fitframe, text='Prime Fitness',\
                                  value=6, command=primesel)
    Primebutton.grid(row=10, column =0, sticky='W')

    def primessel():
        ex='Function to {0,1} that needs 9 parameters.\n'\
           'It calculates the linear combination of\n'\
           'the states in the neightborhood with the\n'\
           'first 9 parameters and return as fitness\n'\
           'value the sum of the prime test results\n'\
           'of the l.c., the l.c.+2, the l.c.+4 and\n'\
           'the l.c.+6.'
        Infolabel.config(text = ex)
        global ff
        ff = 7
        
    Primesbutton = tk.Radiobutton(fitframe, text='Primes Fitness',\
                                  value=7, command=primessel)
    Primesbutton.grid(row=11, column =0, sticky='W')

    def fitnessf():
        global par
        global num_col
        global s
        fitname = ['Life','Lifeh','Metaprimes','Mod','Mod Mod','Prime','Primes']
        global fitmsg
        FFesc = False
        pars=''
        if ff==1:
            num_col = 2
            par=np.zeros(12)
            for i in range(12):
                a=askinteger('Fitness Function',\
                                'Insert parameter '+str(i+1)+'.',\
                                parent = fitness, initialvalue=1)
                if a is None:
                    FFesc=True
                    break
                else:
                    par[i]=int(a)
                    pars=pars+str(int(a))+'  '
            a=askinteger('Fitness Function',\
                            'Insert a seed for the selection.',\
                                parent = fitness, initialvalue=1)
            if a is None:
                FFesc=True
            else:
                s=int(a)
        elif ff==2:
            num_col = 2
            par=np.zeros(12)
            for i in range(12):
                a=askinteger('Fitness Function',\
                                'Insert parameter '+str(i+1)+'.',\
                                parent = fitness, initialvalue=1)
                if a is None:
                    FFesc=True
                    break
                else:
                    par[i]=int(a)
                    pars=pars+str(int(a))+'  '
            a=askinteger('Fitness Function',\
                            'Insert a seed for the selection.',\
                                parent = fitness, initialvalue=1)
            if a is None:
                FFesc=True
            else:
                s=int(a)
        elif ff==3:
            parn=askinteger('Fitness Function',\
                                'How many parameters do you want?\n(besides first 9)',\
                                parent = fitness, minvalue=1, initialvalue=200)
            if parn is None:
                FFesc=True
            else:
                parm=askinteger('Fitness Function',\
                                    'These parameters will be numbers from 0 to '\
                                    +str(parn-1)+' modulo m.\n Insert m.',\
                                    parent = fitness, minvalue=1, initialvalue=1)
                if parm is None:
                    FFesc=True
                else:
                    num_col = parm
                    par=np.zeros(9+parn)
                    for i in range(9):
                        a=askinteger('Fitness Function',\
                                        'Insert parameter '+str(i+1)+'.',\
                                        parent = fitness, initialvalue=1)
                        if a is None:
                            FFesc=True
                            break
                        else:
                            par[i]=int(a)
                            pars=pars+str(int(a))+'  '
            a=askinteger('Fitness Function',\
                            'Insert a seed for the selection.',\
                                parent = fitness, initialvalue=1)
            if a is None:
                FFesc=True
            else:
                s=int(a)
        elif ff==4:
            par=np.zeros(10)
            for i in range(10):
                a=askinteger('Fitness Function',\
                                'Insert parameter '+str(i+1)+'.',\
                                parent = fitness, initialvalue=1)
                if a is None:
                    FFesc=True
                    break
                else:
                    par[i]=int(a)
                    pars=pars+str(int(a))+'  '
            a=askinteger('Fitness Function',\
                            'Insert a seed for the selection.',\
                                parent = fitness, initialvalue=1)
            if a is None:
                FFesc=True
            else:
                s=int(a)
            num_col = par[9]
        elif ff==5:
            par=np.zeros(11)
            for i in range(11):
                a=askinteger('Fitness Function',\
                                'Insert parameter '+str(i+1)+'.',\
                                parent = fitness, initialvalue=1)
                if a is None:
                    FFesc=True
                    break
                else:
                    par[i]=int(a)
                    pars=pars+str(int(a))+'  '
            a=askinteger('Fitness Function',\
                            'Insert a seed for the selection.',\
                                parent = fitness, initialvalue=1)
            if a is None:
                FFesc=True
            else:
                s=int(a)
            num_col = par[10]
        elif ff==6:
            num_col = 2
            par=np.zeros(9)
            for i in range(9):
                a=askinteger('Fitness Function',\
                                'Insert parameter '+str(i+1)+'.',\
                                parent = fitness, initialvalue=1)
                if a is None:
                    FFesc=True
                    break
                else:
                    par[i]=int(a)
                    pars=pars+str(int(a))+'  '
            a=askinteger('Fitness Function',\
                            'Insert a seed for the selection.',\
                                parent = fitness, initialvalue=1)
            if a is None:
                FFesc=True
            else:
                s=int(a)
        else:
            num_col = 5
            par=np.zeros(9)
            for i in range(9):
                a=askinteger('Fitness Function',\
                                'Insert parameter '+str(i+1)+'.',\
                                parent = fitness, initialvalue=1)
                if a is None:
                    FFesc=True
                    break
                else:
                    par[i]=int(a)
                    pars=pars+str(int(a))+'  '
            a=askinteger('Fitness Function',\
                            'Insert a seed for the selection.',\
                                parent = fitness, initialvalue=1)
            if a is None:
                FFesc=True
            else:
                s=int(a)
        if FFesc==False:
            if ff==3:
                fitmsg = fitname[2]+'\n  parameters: '
                for i in range(0,parn):
                    par[9+i]=i%parm
                tkMessageBox.showinfo('Fitness Function',\
                                  'The fitness function parameters will be:\n'+pars+\
                                  '(0 ... '+str(parn-1)+')mod '+str(parm)+' seed ' +str(s),\
                                      parent=fitness)
                fitmsg = fitmsg+pars+'(0 ... '+str(parn-1)+')mod '+str(parm)+' seed ' +str(s)
            else:
                tkMessageBox.showinfo('Fitness Function',\
                                  'The fitness function parameters will be:\n'\
                                  +pars+' seed ' +str(s),\
                                  parent=fitness)
                fitmsg = fitname[ff-1]+'\n  parameters: '+pars+' seed ' +str(s)
            fitness.destroy()
            FFcheck.select()
            check[0] = 1
            CMbutton2.config(state='normal')
        
        
    Fitnessbutton = tk.Button(fitframe, text='Insert parameters and save', width=30,\
                            command=fitnessf)
    Fitnessbutton.grid(row=12, column=0, columnspan=3)

def fitmat(t, v, M):
    
    x, y = M.shape
    N=np.roll(range(x), 1)
    S=np.roll(range(x), -1)
    W=np.roll(range(y), 1)
    E=np.roll(range(y), -1)
    Z=np.zeros((x,y))
    if t==1:
        A = M%v[9]
        B = v[0]*A+v[1]*A[N,:]+v[2]*A[N,:][:,E]+v[3]*A[:,E]+v[4]*A[S,:][:,E]+v[5]*A[S,:]+\
            v[6]*A[S,:][:,W]+v[7]*A[:,W]+v[8]*A[N,:][:,W]
        C = np.logical_or(np.logical_and(np.greater( A ,Z),B==np.full((x,y),v[10])),\
                          B==np.full((x,y),v[11])).astype(int)
    elif t==2:
        A = M%v[9]
        B = v[0]*A+v[1]*A[N,:]+v[2]*A[N,:][:,E]+v[3]*A[:,E]+v[4]*A[S,:][:,E]+v[5]*A[S,:]+\
            v[6]*A[S,:][:,W]+v[7]*A[:,W]+v[8]*A[N,:][:,W]
        C = np.logical_or(np.logical_and(np.greater( M ,Z),B==np.full((x,y),v[10])),\
                          B==np.full((x,y),v[11])).astype(int)
    elif t==3:
        B = v[0]*M+v[1]*M[N,:]+v[2]*M[N,:][:,E]+v[3]*M[:,E]+v[4]*M[S,:][:,E]+v[5]*M[S,:]+\
            v[6]*M[S,:][:,W]+v[7]*M[:,W]+v[8]*M[N,:][:,W]
        C = np.take(v.astype(int),(B.reshape(x*y)+9).astype(int)).reshape((x,y))
    elif t==4:
        B = v[0]*M+v[1]*M[N,:]+v[2]*M[N,:][:,E]+v[3]*M[:,E]+v[4]*M[S,:][:,E]+v[5]*M[S,:]+\
            v[6]*M[S,:][:,W]+v[7]*M[:,W]+v[8]*M[N,:][:,W]
        C = B%v[9]
    elif t==5:
        A = M%v[9]
        B = v[0]*A+v[1]*A[N,:]+v[2]*A[N,:][:,E]+v[3]*A[:,E]+v[4]*A[S,:][:,E]+v[5]*A[S,:]+\
            v[6]*A[S,:][:,W]+v[7]*A[:,W]+v[8]*A[N,:][:,W]
        C = B%v[10]
    elif t==6:
        B = v[0]*M+v[1]*M[N,:]+v[2]*M[N,:][:,E]+v[3]*M[:,E]+v[4]*M[S,:][:,E]+v[5]*M[S,:]+\
            v[6]*M[S,:][:,W]+v[7]*M[:,W]+v[8]*M[N,:][:,W]
        C = np.zeros((x,y))
        for i in range(x):
            for j in range(y):
                C[i,j]=int(isprime(int(B[i,j])))
    elif t==7:
        B = v[0]*M+v[1]*M[N,:]+v[2]*M[N,:][:,E]+v[3]*M[:,E]+v[4]*M[S,:][:,E]+v[5]*M[S,:]+\
            v[6]*M[S,:][:,W]+v[7]*M[:,W]+v[8]*M[N,:][:,W]
        C = np.zeros((x,y))
        for i in range(x):
            for j in range(y):
                C[i,j]=int(isprime(int(B[i,j]))+isprime(int(B[i,j]+2))+\
                           isprime(int(B[i,j]+4))+isprime(int(B[i,j]+6)))
    elif t==8:
        zeros = (M[N,:]==Z).astype(int)+(M[N,:][:,E]==Z).astype(int)+\
                (M[:,E]==Z).astype(int)+(M[S,:][:,E]==Z).astype(int)+\
                (M[S,:]==Z).astype(int)+(M[S,:][:,W]==Z).astype(int)+\
                (M[:,W]==Z).astype(int)+(M[N,:][:,W]==Z).astype(int)
        O = np.ones((x,y))
        ones = (M[N,:]==O).astype(int)+(M[N,:][:,E]==O).astype(int)+\
                (M[:,E]==O).astype(int)+(M[S,:][:,E]==O).astype(int)+\
                (M[S,:]==O).astype(int)+(M[S,:][:,W]==O).astype(int)+\
                (M[:,W]==O).astype(int)+(M[N,:][:,W]==O).astype(int)
        Tw = O + O
        twos = (M[N,:]==Tw).astype(int)+(M[N,:][:,E]==Tw).astype(int)+\
                (M[:,E]==Tw).astype(int)+(M[S,:][:,E]==Tw).astype(int)+\
                (M[S,:]==Tw).astype(int)+(M[S,:][:,W]==Tw).astype(int)+\
                (M[:,W]==Tw).astype(int)+(M[N,:][:,W]==Tw).astype(int)
        Th = Tw + O
        threes = (M[N,:]==Th).astype(int)+(M[N,:][:,E]==Th).astype(int)+\
                (M[:,E]==Th).astype(int)+(M[S,:][:,E]==Th).astype(int)+\
                (M[S,:]==Th).astype(int)+(M[S,:][:,W]==Th).astype(int)+\
                (M[:,W]==Th).astype(int)+(M[N,:][:,W]==Th).astype(int)
        C = (np.logical_and(M==Z,\
                    np.logical_or(ones==Th,zeros+twos==Tw+Th))).astype(int)\
            + (np.logical_and(M==O,\
                    np.logical_or(np.logical_or(ones==Tw,ones==Th),\
                            np.logical_and(np.greater(threes,Z),np.greater(Tw+Th,threes))))).astype(int)\
            + (np.logical_and(M==Tw,\
                    np.logical_or(threes==Th,zeros+twos==Tw+Th))).astype(int)\
            + (np.logical_and(M==Th,\
                    np.logical_or(np.logical_or(threes==Tw,threes==Th),\
                            np.logical_and(np.greater(ones,Z),np.greater(Tw+Th,ones))))).astype(int)
    else:
        zeros = (M[N,:]==Z).astype(int)+(M[N,:][:,E]==Z).astype(int)+\
                (M[:,E]==Z).astype(int)+(M[S,:][:,E]==Z).astype(int)+\
                (M[S,:]==Z).astype(int)+(M[S,:][:,W]==Z).astype(int)+\
                (M[:,W]==Z).astype(int)+(M[N,:][:,W]==Z).astype(int)
        O = np.ones((x,y))
        ones = (M[N,:]==O).astype(int)+(M[N,:][:,E]==O).astype(int)+\
                (M[:,E]==O).astype(int)+(M[S,:][:,E]==O).astype(int)+\
                (M[S,:]==O).astype(int)+(M[S,:][:,W]==O).astype(int)+\
                (M[:,W]==O).astype(int)+(M[N,:][:,W]==O).astype(int)
        Tw = O + O
        twos = (M[N,:]==Tw).astype(int)+(M[N,:][:,E]==Tw).astype(int)+\
                (M[:,E]==Tw).astype(int)+(M[S,:][:,E]==Tw).astype(int)+\
                (M[S,:]==Tw).astype(int)+(M[S,:][:,W]==Tw).astype(int)+\
                (M[:,W]==Tw).astype(int)+(M[N,:][:,W]==Tw).astype(int)
        Th = Tw + O
        C = (np.multiply(np.logical_and(M==Z, ones+twos==Th),(np.greater(twos,ones)+O))).astype(int)+\
            (np.logical_and(M==O,np.logical_or(ones+twos==Tw,ones+twos==Th))).astype(int)+\
            (2*np.logical_and(M==Tw,np.logical_or(ones+twos==Tw,ones+twos==Th))).astype(int)
    return C

# CROSSOVER MATRIX FUNCTIONS

def CMinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'The crossover matrix explains interactions between cells\n'\
                         '(Fitness Function required).')
def second(dim):
    M=np.zeros((int(dim),int(num_col),int(dim),int(num_col)))
    for i in range(dim):
        for j in range(int(num_col)):
            for k in range(dim):
                for l in range(int(num_col)):
                    M[i,j,k,l] = int(k)
    return M

def floor(dim):
    M=np.zeros((int(dim),int(num_col),int(dim),int(num_col)))
    for i in range(dim):
        for j in range(int(num_col)):
            for k in range(dim):
                for l in range(int(num_col)):
                    M[i,j,k,l] = int((i+k)//2)
    return M

def balance(dim):
    M=np.zeros((int(dim),int(num_col),int(dim),int(num_col)))
    for i in range(dim):
        for j in range(int(num_col)):
            for k in range(dim):
                for l in range(int(num_col)):
                    if i < dim-k:
                        M[i,j,k,l] = int((i+k)//2)
                    else:
                        M[i,j,k,l] = math.ceil((i+k)/2.0)
    return M

def ceiling(dim):
    M=np.zeros((int(dim),int(num_col),int(dim),int(num_col)))
    for i in range(dim):
        for j in range(int(num_col)):
            for k in range(dim):
                for l in range(int(num_col)):
                    M[i,j,k,l] = int(math.ceil((i+k)/2.0))
    return M

def dynamic(dim):
    M=np.zeros((int(dim),int(num_col),int(dim),int(num_col)))
    for i in range(dim):
        for j in range(int(num_col)):
            for k in range(dim):
                for l in range(int(num_col)):
                    if i < k:
                        M[i,j,k,l] = int(k - 1)
                    elif i > k:
                        M[i,j,k,l] = int(k + 1)
                    else:
                        M[i,j,k,l] = int(i)
    return M

def lazy(dim):
    M=np.zeros((int(dim),int(num_col),int(dim),int(num_col)))
    for i in range(dim):
        for j in range(int(num_col)):
            for k in range(dim):
                for l in range(int(num_col)):
                    if i < k:
                        M[i,j,k,l] = int(i + 1)
                    elif i > k:
                        M[i,j,k,l] = int(i - 1)
                    else:
                        M[i,j,k,l] = int(i)
    return M

def CM():
    
    global mt
    mt=0
    global ex
    ex='Choose a style for the crossover matrix.'
    
    crossover = tk.Toplevel(main)

    crossover.wm_title('Crossover Matrix')
    cmframe = tk.Frame(crossover, width = 455, height = 290)
    cmframe.pack(expand='true')
    center(crossover)

    CMcheck.deselect()
    check[1] = 0
    IPcheck.deselect()
    check[2] = 0
    IPbutton2.config(state='disabled')
    
    CMintrolabel = tk.Label(cmframe, justify='left',\
    text='The crossover matrix describes interactions between cells:\n'\
         'it takes state and fitness value of two cells and returns a new state.\n'\
         'We use a 4-dimensional matrix with value in the range of possible\n'\
         'states whose dimensions are M x N x M x N where M and N are\n'\
         'amounts of fitness values and states respectively.')
    CMintrolabel.grid(row=0, column=0, sticky='W', columnspan=3)

    CMDlabel = tk.Label(cmframe, anchor='center',\
                        text='Number of states = N')
    CMDlabel.grid(row=1, column=0)
    
    CMDval = (crossover.register(int_input), '%S')
    CMDentry= tk.Entry (cmframe, width=23, justify='center', validate='key',\
                        validatecommand=CMDval)
    CMDentry.grid(row=1, column=1, columnspan=2)

    CMTlabel = tk.Label(cmframe, anchor='center',\
                        text='Parameters used in the crossover')
    CMTlabel.grid(row=2, column=0)

    def cmtype(event):
        global mt
        if CMcombo.current()==0:
            CMSlabel.config(text='\nChoose a prefinite style or insert your own matrix:')
            CMScombo.config(state='readonly',\
                            value=('the second state wins',\
                                   'average values floor rounded',\
                                   'Balanced average values',\
                                   'average values ceiling rounded',\
                                   'dynamic values',\
                                   'lazy values',\
                                   'insert matrix values'))
            CMSbutton.config(state='normal')
        elif CMcombo.current()==1:
            mt = 8
            CMSlabel.config(text='\nClick the button below to insert values.')
            CMScombo.config(state='disabled')
            CMSbutton.config(state='disabled')
        else:
            mt = 9
            CMSlabel.config(text='\nClick the button below to insert values.')
            CMScombo.config(state='disabled')
            CMSbutton.config(state='disabled')
            
    CMcombo = Combobox(cmframe, width=20, justify='center', state='readonly', \
                       value=('only states',\
                              'only fitness values',\
                              'states and fitness values'))
    CMcombo.grid(row=2, column=1, columnspan=2)
    CMcombo.bind('<<ComboboxSelected>>', cmtype)

    CMSlabel = tk.Label(cmframe, justify='left',text='\nChoose used parameters to continue.')
    CMSlabel.grid(row=3, column=0, sticky='W', columnspan=3)

    def cmstyle(event):
        global mt
        global ex
        if CMScombo.current()==0:
            ex='Example:\n'+convmatstr(second(7)[:,0,:,0])
            mt = 1
        elif CMScombo.current()==1:
            ex='Example:\n'+convmatstr(floor(7)[:,0,:,0])
            mt = 2
        elif CMScombo.current()==2:
            ex='Example:\n'+convmatstr(balance(7)[:,0,:,0])
            mt = 3
        elif CMScombo.current()==3:
            ex='Example:\n'+convmatstr(ceiling(7)[:,0,:,0])
            mt = 4
        elif CMScombo.current()==4:
            ex='Example:\n'+convmatstr(dynamic(7)[:,0,:,0])
            mt = 5
        elif CMScombo.current()==5:
            ex='Example:\n'+convmatstr(lazy(7)[:,0,:,0])
            mt = 6
        else:
            ex='Click the button below to insert values.'
            mt = 7
                
    CMScombo = Combobox(cmframe, width=40, justify='center', state='disabled')
    CMScombo.grid(row=4, column=0, columnspan=2)
    CMScombo.lower()
    CMScombo.bind('<<ComboboxSelected>>',cmstyle)

    def CMSinfo():
        tkMessageBox.showinfo('Crossover Matrix', ex, parent=crossover)
        
    CMSbutton = tk.Button(cmframe, text='?', width=3, command = CMSinfo, state='disabled')
    CMSbutton.grid(row=4, column=2)

    def crossoverf():
        global op
        global opmsg
        global comsg
        coname = ['Second','Floor','Balanced','Ceiling','Dynamic','Lazy','Personal']
        CMesc = False
        if CMDentry.get() != '' and int(CMDentry.get())>0 and mt>0:
            m = int(CMDentry.get())
            if mt==1:
                op = second(m)
                opmsg = convmatstr(op[:,0,:,0])
                comsg = coname[mt-1]+' state \n  dimension '+str(m)
            elif mt==2:
                op = floor(m)
                opmsg = convmatstr(op[:,0,:,0])
                comsg = coname[mt-1]+' state \n  dimension '+str(m)
            elif mt==3:
                op = balance(m)
                opmsg = convmatstr(op[:,0,:,0])
                comsg = coname[mt-1]+' state \n  dimension '+str(m)
            elif mt==4:
                op = ceiling(m)
                opmsg = convmatstr(op[:,0,:,0])
                comsg = coname[mt-1]+' state \n  dimension '+str(m)
            elif mt==5:
                op = dynamic(m)
                opmsg = convmatstr(op[:,0,:,0])
                comsg = coname[mt-1]+' state \n  dimension '+str(m)
            elif mt==6:
                op = lazy(m)
                opmsg = convmatstr(op[:,0,:,0])
                comsg = coname[mt-1]+' state \n  dimension '+str(m)
            elif mt==7:
                op = np.zeros((m,int(num_col),m,int(num_col)))
                for i in range(m):
                    for k in range(m):
                        a=askinteger('Crossover Matrix',\
                            'Insert the result of the interaction\n'\
                            'between states '+str(i)+' and '+str(k)+'.',\
                            parent = crossover, minvalue=0, maxvalue=m-1)
                        if a is None:
                            CMesc=True
                            break
                        else:
                            for j in range(int(num_col)):
                                for l in range(int(num_col)):
                                    op[i,j,k,l]=int(a)
                    else:
                        continue
                    break
                opmsg = coname[mt-1]+' state \n'+convmatstr(op[:,0,:,0])
                comsg = opmsg
            elif mt==8:
                op = np.zeros((m,int(num_col),m,int(num_col)))
                for j in range(int(num_col)):
                    for l in range(int(num_col)):
                        a=askinteger('Crossover Matrix',\
                                     'Insert the result of the interaction\n'\
                                     'between fitness values '+str(j)+' and '+str(l)+'.',\
                                     parent = crossover, minvalue=0, maxvalue=m-1)
                        if a is None:
                            CMesc=True
                            break
                        else:
                            for i in range(m):
                                for k in range(m):
                                    op[i,j,k,l]=int(a)
                    else:
                        continue
                    break
                opmsg = 'Fitness \n'+convmatstr(op[0,:,0,:])
                comsg = opmsg
            else:
                op = np.zeros((m,int(num_col),m,int(num_col)))
                comsg = 'State and fitness \n   x   '
                opmsg = ''
                for i in range(m):
                    for j in range(int(num_col)):
                        comsg = comsg + '('+str(i)+','+str(j)+') '
                        opmsg = opmsg + '\n('+str(i)+','+str(j)+') '
                        for k in range(m):
                            for l in range(int(num_col)):
                                a=askinteger('Crossover Matrix',\
                                             'Insert the result of the interaction\n'\
                                             'between pairs ('+str(i)+', '+str(j)+') and ('+str(k)+', '+str(l)+').',\
                                             parent = crossover, minvalue=0, maxvalue=m-1)
                                if a is None:
                                    CMesc=True
                                    break
                                else:
                                    op[i,j,k,l]=int(a)
                                    opmsg = opmsg+'   '+str(a)+'   '
                    else:
                        continue
                    break
                comsg = comsg + opmsg
                opmsg = comsg
            if CMesc==False:
                tkMessageBox.showinfo('Crossover Matrix', 'The crossover matrix will be:\n'\
                                          +opmsg, parent=crossover)
                crossover.destroy()
                CMcheck.select()
                check[1] = 1
                IPbutton2.config(state='normal')
        else:
            tkMessageBox.showwarning('Crossover Matrix', 'Complete the missing fields.',\
                                     parent=crossover)

    Crossoverbutton = tk.Button(cmframe, text='Generate matrix', width=30,\
                            command=crossoverf)
    Crossoverbutton.grid(row=10, column=0, columnspan=3)

# INITIAL POPULATION FUNCTIONS

def IPinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'The initial population gives us cells \n'\
                         'number, disposition and initial states \n'\
                         '(Crossover Matrix required).')

def IP():

    global pt
    pt = 1

    population = tk.Toplevel(main)

    population.wm_title('Initial Population')
    popframe = tk.Frame(population, width = 330, height = 245)
    popframe.pack(expand='true')
    center(population)

    IPcheck.deselect()
    check[2] = 0
    
    IPintrolabel = tk.Label(popframe, justify='left',\
    text='The initial population is a matrix of defined\n'\
         'dimensions with values within the possible states.\n\n'\
         'Choose one of the following possibilities:')
    IPintrolabel.grid(row=0, column=0, sticky='W')

    def randomsel():
        global pt
        pt = 1
        
    Randombutton = tk.Radiobutton(popframe, text='Totally random values',\
                                   value = 1, command=randomsel)
    Randombutton.grid(row=1, column =0, sticky='W')
    Randombutton.select()
    
    def fixransel():
        global pt
        pt = 2
        
    Fixranbutton = tk.Radiobutton(popframe, text='Fixed value in all edge positions\n'\
                                                   'and random values elsewheres',\
                                   value = 2, command=fixransel)
    Fixranbutton.grid(row=2, column =0, sticky='W')

    def insertsel():
        global pt
        pt = 3
        
    Insertbutton = tk.Radiobutton(popframe, text='Insert matrix values',\
                                   value = 3, command=insertsel)
    Insertbutton.grid(row=3, column =0, sticky='W')

    def populationf():
        global pop
        global ipmsg
        IPesc = False
        x = askinteger('Initial Population',\
                                'Insert matrix height.',\
                                parent = population, minvalue=1)
        if x is None:
                IPesc=True
        else:
            y=askinteger('Initial Population',\
                                        'Insert matrix width.',\
                                        parent = population, minvalue=1)
            if y is None:
                IPesc=True
            else:
                if pt==1:
                    s=askinteger('Initial Population',\
                                                'Insert a numeric seed for\n'\
                                                'the random generation.',\
                                                parent = population)
                    if s is None:
                        IPesc=True
                    else:
                        np.random.seed(s)
                        pop=np.random.randint(op.shape[0], size=(x,y))
                        ipmsg='Random of seed '+str(s)+'\n  dimensions '+str(x)+' x '+str(y)
                elif pt==2:
                    fv=askinteger('Initial Population',\
                                                 'Insert the fixed value\n'\
                                                 'for edge positions.',\
                                                 parent = population, minvalue=0,\
                                                 maxvalue=op.shape[0]-1)
                    if fv is None:
                        IPesc=True
                    else:
                        s=askinteger('Initial Population',\
                                                    'Insert a numeric seed for\n'\
                                                    'the random generation.',\
                                                    parent = population)
                        if s is None:
                            IPesc=True
                        else:
                            np.random.seed(s)
                            pop=np.random.randint(op.shape[0], size=(x,y))
                            pop[0,:]=np.full(y, fv)
                            pop[x-1,:]=np.full(y, fv)
                            pop[:,0]=np.full(x, fv)
                            pop[:,y-1]=np.full(x, fv)
                            ipmsg='Random of seed '+str(s)+' with border value '+str(fv)+\
                                   '\n  dimensions '+str(x)+' x '+str(y)
                else:
                    pop=np.zeros((x,y))
                    for i in range(x):
                        for j in range(y):
                            a=askinteger('Initial Population',\
                                'Insert the value in position ('+str(i+1)+','+str(j+1)+').',\
                                parent = population, minvalue=0, maxvalue=op.shape[0]-1)
                            if a is None:
                                IPesc=True
                                break
                            else:
                                pop[i,j]=int(a)
                        else:
                            continue
                        break
                    ipmsg='Personal\n'+convmatstr(pop)
        if IPesc==False:
            IPcheck.select()
            check[2] = 1
            population.destroy()
        
    Populationbutton = tk.Button(popframe, text='Generate matrix', width=30,\
                            command=populationf)
    Populationbutton.grid(row=10, column=0, columnspan=3)
    
# FIXED NODES GRID FUNCTIONS

def FGinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'Insert in the population a grid of fixed state vertices\n' \
                         'with a specific distance between them.')

def FGn():
    FGcheck.select()
    global grid
    global fgmsg
    fgmsg = 'no'
    grid = 0
    check[3]=1
    
def FGy():
    FGcheck.deselect()
    check[3]=0
    a=askinteger('Fixed Nodes Grid',\
                                'Insert the vertical distance.',\
                                parent = main, minvalue=1)
    if a is not None:
        global r
        r=int(a)
        a=askinteger('Fixed Nodes Grid',\
                                'Insert the horizontal distance.',\
                                parent = main, minvalue=1)
        if a is not None:
            global c
            c=int(a)
            global grid
            global fgmsg
            fgmsg = 'yes, distances '+str(r)+' x '+str(c)
            grid=1
            check[3]=1
            FGcheck.select()

# WORLD SHAPE FUNCTIONS

def WSinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                'The world shape characterizes edge cells neightborhood:\n'\
                '- Torus = up is linked to down and left to right;\n'\
                '- Closed = matrix edges are the limits of the world;\n'\
                '- Open Left/Right = left is linked to right, up and down are limits;\n'\
                '- Open Up/Down = up is linked to down, left and right are limits.')

def WS(event):
    global t
    t = WSbutton2.current()
    WScheck.select()
    check[4] = 1

# WORLD LIFESPAN FUNCTIONS

def WLinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'The world lifespan is the total number of steps.')

def WL(event):
    if WLentry.get() != '' and int(WLentry.get())>0:
        global num_gen
        num_gen = int(WLentry.get())
        WLcheck.select()
        check[5] = 1
        MLentry.config(state='normal')
    else:
        WLentry.delete(0, 'end')
        WLcheck.deselect()
        check[5] = 0
        MLentry.config(state='readonly')

# MEMORY LENGHT FUNCTIONS

def MLinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'How many last steps the program will save:\n' \
                         'every saved step consists in state and fitness matrices\n' \
                         '(World Lifespan required).')

def ML(event):
    if MLentry.get() != '' and int(MLentry.get())<=num_gen and int(MLentry.get())>0:
        global memory
        memory = int(MLentry.get())
        MLcheck.select()
        check[6] = 1
    else:
        MLentry.delete(0, 'end')
        MLcheck.deselect()
        check[6] = 0

# MUTATION PERIOD FUNCTIONS

def MPinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'Set the number of steps between a mutation and another\n' \
                         '(if it\'s 0 there will be no mutations).')

def MP(event):
    if MPentry.get() != '':
        global mutation_n
        mutation_n = int(MPentry.get())
        MPcheck.select()
        check[7] = 1
        if mutation_n == 0:
            global mutation_perc
            mutation_perc=0
            MPRentry.delete(0, 'end')
            MPRentry.config(state='disabled')
            MPRcheck.select()
            check[8] = 1
        else:
            MPRentry.config(state='normal')
            MPRcheck.deselect()
            check[8] = 0
    else:
        MPcheck.deselect()
        check[7] = 0
        MPRentry.config(state='normal')
        MPRcheck.deselect()
        check[8] = 0

# MUTATION PROBABILITY FUNCTIONS

def MPRinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'Set the probability of mutation, if it has period not null:\n' \
                         'insert a non-zero percentual (also with decimals). ')

def MPR(event):
    if MPRentry.get() != '' and float(MPRentry.get())<=100 and float(MPRentry.get())>0:
        global mutation_perc
        mutation_perc = float(MPRentry.get())
        MPRcheck.select()
        check[8] = 1
    else:
        MPRentry.delete(0,'end')
        MPRcheck.deselect()
        check[8] = 0
   
# PAUSED FUNCTIONS

def Pinfo():
   tkMessageBox.showinfo('Cellular Evolution', \
                         'You can stop the iteration every specified number of steps.')

def P(event):
    if Pentry.get() != '' and float(Pentry.get())>-1:
        global steps
        steps = float(Pentry.get())
        Pcheck.select()
        check[9] = 1
    else:
        Pentry.delete(0,'end')
        Pcheck.deselect()
        check[9] = 0
 
# COLOR SCALE FUNCTIONS

def CSinfo():
    fig, col = plt.subplots(nrows=3)
    col[0].set_title('Choose the color scale used for the population between these cases:'\
                      '\n\njet')
    col[0].imshow([[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]], cmap=plt.cm.jet)
    col[0].axis('off')
    col[1].set_title('gist_rainbow')
    col[1].imshow([[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]], cmap=plt.cm.gist_rainbow)
    col[1].axis('off')
    col[2].set_title('nipy_spectral')
    col[2].imshow([[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]], cmap=plt.cm.nipy_spectral)
    col[2].axis('off')
    x = main.winfo_screenwidth()
    y = main.winfo_screenheight()
    win = plt.get_current_fig_manager()
    win.canvas.set_window_title('Cellular Evolution')
    win.window.wm_geometry('650x650+'+str((x//2)-325)+'+'+str((y//2)-200))    
    plt.show()

def CS(event):
    global color_scale
    color_scale = CSbutton2.get()
    CScheck.select()
    check[10] = 1

# START FUNCTIONS

def graphics():
    
    if (check==np.full(12,1)).all():

        global ff
        global par
        global num_col
        global fitmsg
        global op
        global pop
        global grid
        global r
        global c
        global t
        global num_gen
        global memory
        global mutation_n
        global mutation_perc
        global steps
        global color_scale
        global s
                
        m, n = pop.shape
        n_states = op.shape[0]
        N = np.roll(range(m), 1)
        S = np.roll(range(m), -1)
        W = np.roll(range(n), 1)
        E = np.roll(range(n), -1)
        
        ran=range(9)
        
        rm=np.repeat(np.asmatrix(range(m)).transpose(),n,axis=1)
        cm=np.repeat(np.asmatrix(range(n)),m,axis=0)

        savedpop=np.zeros((memory,m,n))
        savedfit=np.zeros((memory,m,n))

        fig = plt.figure()
        x = main.winfo_screenwidth()
        y = main.winfo_screenheight()
        win = plt.get_current_fig_manager()
        win.window.wm_geometry(str(n*14)+'x'+str(m*6)+'+'+str((x//2)-(n*7))+'+'+str((y//2)-(m*3)))    

        main.withdraw()
        
        for i in range(num_gen):

            fit = fitmat(ff,par,pop)
            
            popgr = plt.subplot2grid((1,2),(0,0))
            popgr.set_title('Population')
            popgr.matshow(pop, cmap=plt.get_cmap(color_scale))
            popgr.axis('off')
            fitgr = plt.subplot2grid((1,2),(0,1))
            fitgr.set_title('Fitness')
            fitgr.matshow(fit, cmap=plt.cm.jet,vmin=0, vmax=num_col-1)
            fitgr.axis('off')
            fig.canvas.set_window_title('Cellular Evolution - Generation '+str(i+1))
            plt.draw()
            plt.pause(0.000000000001)            
            
            if i>=(num_gen-memory):
                savedpop[i-num_gen+memory,:,:]=pop
                savedfit[i-num_gen+memory,:,:]=fit

            random.seed(s)
            random.shuffle(ran)
            p = np.zeros((9,m,n))
            p[ran[0],:,:]=pop
            p[ran[1],:,:]=pop[N,:]
            p[ran[2],:,:]=pop[N,:][:,E]
            p[ran[3],:,:]=pop[:,E]
            p[ran[4],:,:]=pop[S,:][:,E]
            p[ran[5],:,:]=pop[S,:]
            p[ran[6],:,:]=pop[S,:][:,W]
            p[ran[7],:,:]=pop[:,W]
            p[ran[8],:,:]=pop[N,:][:,W]
            f = np.zeros((9,m,n))
            f[ran[0],:,:]=fit
            f[ran[1],:,:]=fit[N,:]
            f[ran[2],:,:]=fit[N,:][:,E]
            f[ran[3],:,:]=fit[:,E]
            f[ran[4],:,:]=fit[S,:][:,E]
            f[ran[5],:,:]=fit[S,:]
            f[ran[6],:,:]=fit[S,:][:,W]
            f[ran[7],:,:]=fit[:,W]
            f[ran[8],:,:]=fit[N,:][:,W]

            g=f.argmax(0)
            selp=p[g,rm,cm]
            self=f[g,rm,cm]

            if t==0 and grid==0:
                
                pop=op[pop.astype(int),fit.astype(int),selp.astype(int),self.astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m,n),mutation_perc),\
                                       np.random.rand(m,n)*100)
                        pop = (pop - P*(pop - np.random.rand(m,n)*(n_states-1))).astype(int)
                        
            if t==0 and grid==1:

                F = pop[r-1:m:r,c-1:n:c]
                pop=op[pop.astype(int),fit.astype(int),selp.astype(int),self.astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m,n),mutation_perc),\
                                       np.random.rand(m,n)*100)
                        pop = (pop - P*(pop - \
                               np.random.rand(m,n)*(n_states-1))).astype(int)

                pop[r-1:m:r,c-1:n:c] = F

            if t==1 and grid==0:

                R = np.repeat(np.asmatrix(range(1,m-1)).transpose(),n-2,axis=1)
                C = np.repeat(np.asmatrix(range(1,n-1)),m-2,axis=0)
                pop[R,C]=op[pop[R,C].astype(int),fit[R,C].astype(int),selp[R,C].astype(int),self[R,C].astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m-2,n-2),mutation_perc),\
                                       np.random.rand(m-2,n-2)*100)
                        pop[R,C] = (pop[R,C] - P*(pop[R,C] - \
                                    np.random.rand(m-2,n-2)*(n_states-1))).astype(int)

            if t==1 and grid==1:

                R = np.repeat(np.asmatrix(range(1,m-1)).transpose(),n-2,axis=1)
                C = np.repeat(np.asmatrix(range(1,n-1)),m-2,axis=0)
                F = pop[r-1:m:r,c-1:n:c]
                pop[R,C]=op[pop[R,C].astype(int),fit[R,C].astype(int),selp[R,C].astype(int),self[R,C].astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m-2,n-2),mutation_perc),\
                                       np.random.rand(m-2,n-2)*100)
                        pop[R,C] = (pop[R,C] - P*(pop[R,C] - \
                                    np.random.rand(m-2,n-2)*(n_states-1))).astype(int)

                pop[r-1:m:r,c-1:n:c] = F

            if t==2 and grid==0:

                R = np.repeat(np.asmatrix(range(1,m-1)).transpose(),n,axis=1)
                C = np.repeat(np.asmatrix(range(n)),m-2,axis=0)
                pop[R,C]=op[pop[R,C].astype(int),fit[R,C].astype(int),selp[R,C].astype(int),self[R,C].astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m-2,n),mutation_perc),\
                                       np.random.rand(m-2,n)*100)
                        pop[R,C] = (pop[R,C] - P*(pop[R,C] - \
                                    np.random.rand(m-2,n-2)*(n_states-1))).astype(int)
            
            if t==2 and grid==1:

                R = np.repeat(np.asmatrix(range(1,m-1)).transpose(),n,axis=1)
                C = np.repeat(np.asmatrix(range(n)),m-2,axis=0)
                F = pop[r-1:m:r,c-1:n:c]
                pop[R,C]=op[pop[R,C].astype(int),fit[R,C].astype(int),selp[R,C].astype(int),self[R,C].astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m-2,n),mutation_perc),\
                                       np.random.rand(m-2,n)*100)
                        pop[R,C] = (pop[R,C] - P*(pop[R,C] - \
                                    np.random.rand(m-2,n-2)*(n_states-1))).astype(int)

                pop[r-1:m:r,c-1:n:c] = F

            if t==3 and grid==0:

                R = np.repeat(np.asmatrix(range(m)).transpose(),n-2,axis=1)
                C = np.repeat(np.asmatrix(range(1,n-1)),m,axis=0)
                pop[R,C]=op[pop[R,C].astype(int),fit[R,C].astype(int),selp[R,C].astype(int),self[R,C].astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m,n-2),mutation_perc),\
                                       np.random.rand(m,n-2)*100)
                        pop[R,C] = (pop[R,C] - P*(pop[R,C] - \
                                    np.random.rand(m-2,n-2)*(n_states-1))).astype(int)

            if t==3 and grid==1:

                R = np.repeat(np.asmatrix(range(m)).transpose(),n-2,axis=1)
                C = np.repeat(np.asmatrix(range(1,n-1)),m,axis=0)
                F = pop[r-1:m:r,c-1:n:c]
                pop[R,C]=[pop[R,C].astype(int),fit[R,C].astype(int),selp[R,C].astype(int),self[R,C].astype(int)]

                if mutation_perc>0:
                    if (i+1)%mutation_n==0:
                        P = np.greater(np.full((m,n-2),mutation_perc),\
                                       np.random.rand(m,n-2)*100)
                        pop[R,C] = (pop[R,C] - P*(pop[R,C] - \
                                    np.random.rand(m-2,n-2)*(n_states-1))).astype(int)

                pop[r-1:m:r,c-1:n:c] = F
                
            if steps>0 and (i+1)%steps==0:
                tkMessageBox.showinfo('Cellular Evolution', \
                                 'Click OK to continue.',parent=None)
        
        tkMessageBox.showinfo('Cellular Evolution', \
                              'This was Cellular Evolution with:\n'\
                              '- fitness function: '+fitmsg+\
                              '\n- crossover matrix: '+comsg+\
                              '\n- initial population: '+ipmsg+\
                              '\n- fixed grid: ' +fgmsg,parent=None)
        plt.close()
        main.deiconify()
        
    else:
        tkMessageBox.showwarning('Cellular Evolution', \
                                 'Insert missing parameters.')



                        
# MAIN WINDOW

main = tk.Tk()

main.wm_title('Cellular Evolution')
mainframe = tk.Frame(main, width = 430, height = 520)
mainframe.pack(expand='true')
center(main)

check = [0,0,0,0,0,0,0,0,0,0,0,0]

introlabel = tk.Label(mainframe, justify='left', text='Welcome! \n'\
                   'Please, enter the following data to start running your system.')
introlabel.grid(row=0, column=0, sticky='W', columnspan=7)

# PARTICULAR CASES

PClabel = tk.Label(mainframe, width=20, anchor='center', text='Choose a case')
PClabel.grid(row=1, column=0)

PCbutton1 = tk.Button(mainframe, text ='?', width=3, command = PCinfo)
PCbutton1.grid(row=1, column=1)
            
PCcombo = Combobox(mainframe, width=18, justify='center', state='readonly', \
                   value=('Game of Life',\
                          'Game of Life (3 col.)',\
                          'Game of Life (4 col.)',\
                          'Insert your parameters'))
PCcombo.grid(row=1, column=2, columnspan=2)
PCcombo.bind('<<ComboboxSelected>>', cases)

PCcheck = tk.Checkbutton(mainframe, state='disabled')
PCcheck.grid(row=1, column=4)

# FITNESS FUNCTION

FFlabel = tk.Label(mainframe, width=20, anchor='center', text='Fitness Function')
FFlabel.grid(row=2, column=0)

FFbutton1 = tk.Button(mainframe, text ='?', width=3, command = FFinfo)
FFbutton1.grid(row=2, column=1)

FFbutton2 = tk.Button(mainframe, text ='Insert', width=20, command=FF, state='disabled')
FFbutton2.grid(row=2, column=2, columnspan=2)

FFcheck = tk.Checkbutton(mainframe, state='disabled')
FFcheck.grid(row=2, column=4)

# CROSSOVER MATRIX

CMlabel = tk.Label(mainframe, width=20, anchor='center', text='Crossover Matrix')
CMlabel.grid(row=3, column=0)

CMbutton1 = tk.Button(mainframe, text ='?', width=3, command = CMinfo)
CMbutton1.grid(row=3, column=1)

CMbutton2 = tk.Button(mainframe, text ='Insert', width=20, command=CM, state='disabled')
CMbutton2.grid(row=3, column=2, columnspan=2)

CMcheck = tk.Checkbutton(mainframe, state='disabled')
CMcheck.grid(row=3, column=4)

# INITIAL POPULATION

IPlabel = tk.Label(mainframe, width=20, anchor='center', text='Initial Population')
IPlabel.grid(row=4, column=0)

IPbutton1 = tk.Button(mainframe, width=3, text ='?', command = IPinfo)
IPbutton1.grid(row=4, column=1)

IPbutton2 = tk.Button(mainframe, text ='Insert', width=20, command=IP, state='disabled')
IPbutton2.grid(row=4, column=2, columnspan=2)

IPcheck = tk.Checkbutton(mainframe, state='disabled')
IPcheck.grid(row=4, column=4)

# FIXED NODES GRID

FGlabel1 = tk.Label(mainframe, width=20, anchor='center', text='Fixed Nodes Grid')
FGlabel1.grid(row=5, column=0)

FGbutton1 = tk.Button(mainframe, text ='?', width=3, command = FGinfo)
FGbutton1.grid(row=5, column=1)
            
FGbutton2 = tk.Button(mainframe, text='Yes', command=FGy)
FGbutton2.grid(row=5, column=2, sticky='E'+'W')

FGbutton3= tk.Button (mainframe, text='No', command=FGn)
FGbutton3.grid(row=5, column=3, sticky='E'+'W')

FGcheck = tk.Checkbutton(mainframe, state='disabled')
FGcheck.grid(row=5, column=4, sticky='E'+'W')

# WORLD SHAPE

WSlabel = tk.Label(mainframe, width=20, anchor='center', text='World Shape')
WSlabel.grid(row=6, column=0)

WSbutton1 = tk.Button(mainframe, text ='?', width=3, command = WSinfo)
WSbutton1.grid(row=6, column=1)

WSbutton2 = Combobox (mainframe, width=18, justify='center', state='readonly', \
                      value=('Torus','Closed','Open Left/Right','Open Up/Down'))
WSbutton2.grid(row=6, column=2, columnspan=2)
WSbutton2.bind('<<ComboboxSelected>>', WS)

WScheck = tk.Checkbutton(mainframe, state='disabled')
WScheck.grid(row=6, column=4)

# WORLD LIFESPAN

WLlabel = tk.Label(mainframe, width=20, anchor='center', text='World Lifespan')
WLlabel.grid(row=7, column=0)

WLbutton = tk.Button(mainframe, text ='?', width=3, command = WLinfo)
WLbutton.grid(row=7, column=1)

WLval = (mainframe.register(int_input), '%S')
WLentry= tk.Entry (mainframe, width=20, justify='center', validate='key', validatecommand=WLval)
WLentry.grid(row=7, column=2, columnspan=2)
WLentry.bind('<FocusOut>',WL)

WLcheck = tk.Checkbutton(mainframe, state='disabled')
WLcheck.grid(row=7, column=4)

# MEMORY LENGHT

MLlabel = tk.Label(mainframe, width=20, anchor='center', text='Memory Lenght')
MLlabel.grid(row=8, column=0)

MLbutton = tk.Button(mainframe, text ='?', width=3, command = MLinfo)
MLbutton.grid(row=8, column=1)

MLval = (mainframe.register(int_input), '%S')
MLentry= tk.Entry (mainframe, width=20, state='disabled', justify='center', validate='key',\
                validatecommand=MLval)
MLentry.grid(row=8, column=2, columnspan=2)
MLentry.bind('<FocusOut>',ML)

MLcheck = tk.Checkbutton(mainframe, state='disabled')
MLcheck.grid(row=8, column=4)

# MUTATION PERIOD

MPlabel = tk.Label(mainframe, width=20, anchor='center', text='Mutation Period')
MPlabel.grid(row=9, column=0)

MPbutton = tk.Button(mainframe, text ='?', width=3, command = MPinfo)
MPbutton.grid(row=9, column=1)

MPval = (mainframe.register(int_input), '%S')
MPentry= tk.Entry (mainframe, width=20, justify='center', validate='key', validatecommand=MPval)
MPentry.grid(row=9, column=2, columnspan=2)
MPentry.bind('<FocusOut>',MP)

MPcheck = tk.Checkbutton(mainframe, state='disabled')
MPcheck.grid(row=9, column=4)

# MUTATION PROBABILITY

MPRlabel = tk.Label(mainframe, width=20, anchor='center', text='Mutation Probability')
MPRlabel.grid(row=10, column=0)

MPRbutton = tk.Button(mainframe, text ='?', width=3, command = MPRinfo)
MPRbutton.grid(row=10, column=1)
         
MPRval = (mainframe.register(num_input), '%P')
MPRentry= tk.Entry (mainframe, width=20, justify='center', validate='key', validatecommand=MPRval)
MPRentry.grid(row=10, column=2, columnspan=2)
MPRentry.bind('<FocusOut>',MPR)

MPRcheck = tk.Checkbutton(mainframe, state='disabled')
MPRcheck.grid(row=10, column=4)

# PAUSED

Plabel = tk.Label(mainframe, width=20, anchor='center', text='Paused')
Plabel.grid(row=11, column=0)

Pbutton1 = tk.Button(mainframe, text ='?', width=3, command = Pinfo)
Pbutton1.grid(row=11, column=1)

Pval = (mainframe.register(num_input), '%P')
Pentry= tk.Entry (mainframe, width=20, justify='center', validate='key', validatecommand=MPRval)
Pentry.grid(row=11, column=2, columnspan=2)
Pentry.bind('<FocusOut>',P)       

Pcheck = tk.Checkbutton(mainframe, state='disabled')
Pcheck.grid(row=11, column=4)

# COLOR SCALE

CSlabel = tk.Label(mainframe, width=20, anchor='center', text='Color Scale')
CSlabel.grid(row=12, column=0)

CSbutton1 = tk.Button(mainframe, text ='?', width=3, command = CSinfo)
CSbutton1.grid(row=12, column=1)
 
CSbutton2 = Combobox (mainframe, width=18, justify='center', state='readonly',\
                     value=('jet','gist_rainbow','nipy_spectral'))
CSbutton2.grid(row=12, column=2, columnspan=2)
CSbutton2.bind('<<ComboboxSelected>>', CS)

CScheck = tk.Checkbutton(mainframe, state='disabled')
CScheck.grid(row=12, column=4)

# START
       
STARTbutton = tk.Button(mainframe, text='START', width=30, command=graphics)
STARTbutton.grid(row=13, column=0, columnspan=5, pady=5)

main.mainloop()

