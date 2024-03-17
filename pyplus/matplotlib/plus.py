import matplotlib.pyplot as plt
from typing import Callable
import numpy as np

def show_fx(func:Callable):
    '''
    show function 
    ## Parameters:
    func : function of 1-dim
    like f(x)=x+1.
    ## Examples:
    import matplotlib.pyplot as plt
    fig,ax= plt.subplots(1,1)
    show_fx(lambda x : x+1)
    plt.show(fig)
    '''
    x_range=np.arange(-5,5,0.01)
    fx_range=func(x_range)
    plt.plot(x_range,fx_range)