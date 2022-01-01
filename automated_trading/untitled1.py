# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 12:08:54 2022

@author: Randy666
"""

import time
import numpy as np
import datetime as dt


def fibonacci(n):
    if n<=1:
        return n
    else:
        return (fibonacci(n-1)+fibonacci(n-2))
    

def main():
    num = np.random.randint(1,25)
    
    print("%dth fibonnaci number is %d"%(num,fibonacci(num)))
    
starttime = time.time()
timeout = starttime + 60*2;

while starttime<=timeout:
    try:
        main()
        time.sleep(5-(time.time()-starttime)%5)
    except KeyboardInterrupt:
        print("exiting")
        exit() 
        