import itertools as it
import numpy as np

def main_program():
    ''' This is where I will implement the main method.'''
    S_0 = input("Please enter the initial stock price: ")
    S_0 = float(S_0)
    r = input("Please enter the interest rate: ")
    r = float(r)
    u = input("Please enter a value for 'u' (up factor): ")
    u = float(u)
    d = input("Please enter a value for 'd' (down factor)): ")
    d = float(d)
    type = input("What type of option are you pricing? This program can handle put and call options. For a call option enter 1. For a put option enter 2: ")
    type = int(type)
    if (type==1) | (type==2):
        K = input("Please enter the strike price for the option: ")
        K = float(K)
        T = input("Please enter the maturity date of the option (T=?): ")
        T = int(T)
    else:
        print("INVALID INPUT")

    V_T = define_final_Vs(S_0, u, d, T, K, type)
    V_second_to_last = np.zeros(2)

    stock_matrix = get_stock_price_matrix(S_0,u,d,T)
    #print(stock_matrix)
    #print(V_T)

    for i in range(1, T+1):
        if (len(V_T)==2):
            V_second_to_last = V_T
            #print("Printing second to last V vector")
            #print(V_second_to_last)
        V_Tm1 = np.zeros(2**(T-i))
        for k in range(0, 2**(T-i)):
            V_Tm1[k] = v_prev(V_T[2*k], V_T[2*k+1], u, d, r)
        V_T = V_Tm1

        #print(V_T)

    #print(V_second_to_last)
    print("To replaicate the option, you should purchase " + str(delta_0(stock_matrix[:,1],V_second_to_last)) + " shares.")
    print("The price of the option at time 0 is: $" + str(V_Tm1[0]))
    return V_Tm1[0]


def get_stock_price_matrix(S_0,u,d,T):
    States = np.array(list(it.product([u, d], repeat=T)), dtype=float)

    S = np.zeros_like(States, dtype=float)
    S_0col = np.array([S_0]*(2**T))
    S_0col.shape = (2**T, 1)
    S = np.hstack((S_0col, S))

    for i in range(1, T+1):
        S[:,i] = S[:,i-1] * States[:,i-1]

    return S

def define_final_Vs(S_0, u, d, T, K, type):
    ''' This subprogram defines the final values that the option can take.
    S_0, u, and d are required to show how the stock price evolves. T tells
    us how many possibilities there are for the different prices. type determines
    the procedure for actually computing the Vs (Put, Call, or Exotic).'''


    S = get_stock_price_matrix(S_0,u,d,T)


    ''' Now, determine the option value for each type of option!
    Call Option: V = S_T - K, where this is positive
    Put Option: V = K - S_T, where this is positive
    Exotic Option: ??? '''

    if type == 1:
        V_T = S[:,T] - K
        # Some fancy indexing...
        mask = V_T[V_T<0]
        V_T[V_T<0] = 0
    if type == 2:
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

def delta_0(stock_values_year_1, V_second_to_last):
    '''
    This function returns delta_0 from as from eqn (3.13).
    '''

    #print(stock_values_year_1)

    length_col = len(stock_values_year_1)

    location_H = (length_col/2)-1
    location_T = (length_col/2)

    denom = stock_values_year_1[int(location_H)] - stock_values_year_1[int(location_T)]
    numer = V_second_to_last[0] - V_second_to_last[1]

    #print(numer)
    #print(denom)

    return numer/denom
    


    #delta_0 = (V_second_to_last[0]-V_second_to_last[1])/(stock_matrix[:,1][middle_entry-1]-stock_matrix[:,1][middle_entry])

    #return delta_0


#test
#print(define_final_Vs(50,2,.5,2,9,"Call"))

#test_matrix = get_stock_price_matrix(8,2,.5,2)
#print(test_matrix)

#delta_0 = 1/((test_matrix[:,1][2-1])-(test_matrix[:,1][2]))
#print(delta_0)
#print(delta_prev())
#print(" ------------------------- ")
main_program()
#print(v_prev(1, 0, 2, .5, .02))
#main_program()
