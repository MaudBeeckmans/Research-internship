# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:58:08 2021

@author: maudb
"""

"""Script that nicely shows how we might implement the multiprocessing parts. The most interesting cell is cell 
'#%% 'Pool class: handle multiple outputs per worker'"""


import multiprocessing as mp
import numpy as np

cpu = mp.cpu_count()

def f(x):
    return x*x

if __name__ == '__main__':
    with mp.Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
        
#%%
import time
from multiprocessing import Pool


def cube(x):
    print(f"start process {x}")
    result = x * x * x
    time.sleep(1)
    print(f"end process {x}")
    return result


if __name__ == "__main__":
    tic = time.time()
    pool = Pool(processes=5)
    print(pool.map(cube, range(5)))
    pool.close()
    pool.join()
    
    toc = time.time()
    
    print('Done in {:.4f} seconds'.format(toc-tic))

#%% Pool class: handle multiple outputs per worker
import time
from multiprocessing import Pool
import numpy as np
import pandas as pd 

def sum_of_cubes(x, y):
    print(f"start process {x}, {y}")
    time.sleep(1)
    print(f"end process {x}, {y}")
    f = np.array([1, 2, 3])
    return x * x * x + y * y * y, x + y, f


if __name__ == "__main__":
    pool = Pool(processes=2)
    out = pool.starmap(sum_of_cubes, [(19, 19), (13, 19), (1, 5)])
    print("HERE!")
    print("HERE AGAIN!")
    pool.close()
    pool.join()

    total_output = pd.DataFrame(out, columns = ['sum_cubes', 'add', 'array'])
