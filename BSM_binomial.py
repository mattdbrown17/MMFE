import itertools as it
import numpy as np

def main_program():
    ''' This is where I will implement the main method.'''
    S_0 = input("Please enter the initial stock price:")
    S_0 = float(S_0)
    r = input("Please enter the interest rate:")
    r = float(r)
    d = input("Please enter a value for 'd' (down factor)):")
    d = float(d)
    u = input("Please enter a value for 'u' (up factor):")
    d = float(d)
    type = input("What type of option are you pricing? Please enter the one of the following strings: 'Put', 'Call', 'Exotic':")
    type = str(type)
    if (type=="Put") | (type=="Call"):
        K = input("Please enter the strike price for the option")
        K = float(K)
        T = input("Please enter the maturity date of the option (T=?)")
        T = int(T)
    if type=="Exotic":
        print("INVALID INPUT")

    print(S_0, u, d, T, K, type)
    V_T = define_final_Vs(S_0, u, d, T, K, type)
    return V_prev(V_T[0], V_T[1])


def define_final_Vs(S_0, u, d, T, K, type):
    ''' This subprogram defines the final values that the option can take.
    S_0, u, and d are required to show how the stock price evolves. T tells
    us how many possibilities there are for the different prices. type determines
    the procedure for actually computing the Vs (Put, Call, or Exotic).'''


    States = np.array(list(it.product([u, d], repeat=T)))

    S = np.zeros_like(States, dtype=float)
    S_0col = np.array([S_0]*(2**T))
    S_0col.shape = (2**T, 1)
    S = np.hstack((S_0col, S))

    T = int(T)
    for i in range(1, T+1):
        S[:,i] = S[:,i-1] * States[:,i-1]

    ''' Now, determine the option value for each type of option!
    Call Option: V = S_T - K, where this is positive
    Put Option: V = K - S_T, where this is positive
    Exotic Option: ??? '''

    if type == "Call":
        V_T = S[:,T] - K
        # Some fancy indexing...
        mask = V_T[V_T<0]
        V_T[V_T<0] = 0
    if type == "Put":
        V_T = K - S[:,T]
        # Some fancy indexing...
        mask = V_T[V_T<0]
        V_T[V_T<0] = 0
    return V_T

def v_prev(VH, VT, u, d, r):
    '''
    This function computes V_0 from equation (3.9). It requires as
    input the future V(H) and V(T) as well as parameters u, d, and r.
    It returns a scalar.
    '''
    V_0 = (1/(1+r))*(((1+r-d)/(u-d))*VH + ((u-(1+r))/(u-d))*VT)
    return V_0

#test
print(define_final_Vs(1.0, 2.0, .5, 1, 1.2, "Call"))
main_program()
