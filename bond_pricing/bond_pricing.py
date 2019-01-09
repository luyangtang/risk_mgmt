# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 16:30:05 2019

@author: lt36166
"""
import matplotlib.pyplot as plt
from math import floor



def calculate_value_at_time(v_0, payment_freq, time_elapsed = 1, y = 0.05):
    '''
    Calculates the value of the bond in time given its price at T = 0
    
    Parameters
    ==========
    
    v_0: float
        value at T = 0, i.e. price of the bond
        
    payment_freq: float/string
        number of payments per year
        2 for semiannual payment, 4 for quarterly payment etc
        0.5 for bi-annually
        Feature to be added later:
            'inf' for perpetual bonds that compounds instantaneously
        
    time_elapsed: float
        time (in years) since initialisation
        
    y: float
        yield of the bond (annually)
        
    Returns
    =======
    v_0: float
        accumulated value of the bond since bought at price v_0
    
    '''
    
    v_1 = v_0;
    
    # calculate the value at each payment
    for i in range(0,floor(time_elapsed * payment_freq)):
        v_1 *= (1 + y/payment_freq)
        
    return v_1


class Bond(object):
    def __init__(self, value, maturity, payment_freq, y, face_value = False):
        '''
        Parameters:
        ===========
        value: float
            can be one of the following:
                price (v_0) [when face_value = False]
                face value (v_t) [when face_value = True]
        
        face_value: bool
            categories the value input
            default false so the value is defaulted to be the price
            
        maturity: int
            unit is in years
        
        payment_freq: float/string
            number of payments per year
            2 for semiannual payment, 4 for quarterly payment etc
            0.5 for bi-annually
            Feature to be added later:
                'inf' for perpetual bonds that compounds instantaneously
                
        y: float
            yield of the bond (annually)
        '''
        if face_value:
            # add code to this section later
            pass
        else:
            self.v_0 = value
            self.payment_freq = payment_freq
            self.maturity = maturity
            self.y = y
            self.v_t = calculate_value_at_time(self.v_0, 
                                          self.payment_freq, 
                                          self.maturity, 
                                          self.y)
            
            
    def value(self,time):
        '''
        Calculate the value of the bond at time t
        
        Parameters
        ==========
        time: float
            between 0 and maturity
            
        Returns
        v: float
            value of the bond at time t
        '''
        if time <= self.maturity:
            return calculate_value_at_time(self.v_0, 
                                              self.payment_freq, 
                                              time, 
                                              self.y)
        else:
            return self.v_t
            
        
    def plot_value(self, time = None, ax = None, show_maturity = True):
        '''
        Plot the value of the bond at time t
        
        Parameters
        ==========
        time: int
            between 0 and maturity
            Default to none so that the code will assume to plot until maturity
            
        ax: matplotlib.pyplot.Axes
            defaulted to none so that a new ax will be created
            if ax is found the plot will be put on the assigned object
        
        show_maturity: bool:
            if a vertical mark will be shown on the maturity date
            
        Returns
        =======
        ax: matplotlib.pyplot.Axes
        '''
        # if a time is not given set it to be maturity
        if not time:
            time = self.maturity
            
        # define the vectors  
        t = [i for i in range(0,time)]
        v = [self.value(i) for i in t]
        
        try: # in case ax cannot be used
            ax.plot(t,v)
        except:
            ax = plt.subplot(111)
            ax.plot(t,v)
            
        ax.set_ylabel('Time')
        
        # maturity mark
        if show_maturity:
            ax.axvline(self.maturity,c = 'r')
        return ax
    
class BondGroup(object):
    pass
            
def test_bond(): 
    # test basic bond
    d1 = Bond(100,10,2,0.08)
    d1.plot_value(15)
    
    # test ax
    fig,ax = plt.subplots(nrows = 1, ncols = 2)
    d1.plot_value(ax = ax[0])
    d1.plot_value(ax = ax[1])
   
    
test_bond()