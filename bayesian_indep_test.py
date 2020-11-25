# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:56:20 2020

@author: Filippo
"""

import numpy as np
from scipy.special import loggamma
from scipy.stats import norm, pearsonr
import matplotlib.pyplot as plt


def independence_tester(x, y, c=5):
    '''

    Parameters
    ----------
    x : 1D array
    y : 1D array, same size as x
    c : float, optional
        The default is 5.

    Returns
    -------
    float between 0 and 1
        probability of dependence between x and y

    '''
    
    N = x.shape[0]
    mu_x = np.mean(x)
    mu_y = np.mean(y)
    sigma_x = np.var(x)**(1/2)
    sigma_y = np.var(y)**(1/2)
    
    x_normalized = (x-mu_x)/sigma_x
    y_normalized = (y-mu_y)/sigma_y
    
    x_scaled = norm.cdf(x_normalized)
    y_scaled = norm.cdf(y_normalized)
     
    
    def count_data(xx, yy, l):
        count = 0
        ax = l[0][0]
        bx = l[0][1]
        ay = l[1][0]
        by = l[1][1]
        for i in range(N):
            if (ax< xx[i]) and (xx[i] <= bx) and (ay< yy[i]) and (yy[i] <= by):
                count += 1  
        # print('count:', count)
        return count
    
    def partition_square(l):
        ax = l[0][0]
        bx = l[0][1]
        ay = l[1][0]
        by = l[1][1]
        p0 = [[[ax, (ax+bx)/2], [ay, (ay+by)/2]]]
        p1 = [[[(ax+bx)/2, bx], [ay, (ay+by)/2]]]
        p2 = [[[ax, (ax+bx)/2], [(ay+by)/2, by]]]
        p3 = [[[(ax+bx)/2, bx], [(ay+by)/2, by]]]
        
        # print('input partition_square:', l)
        # print('output partition_square:', [p0, p1, p2, p3])
        return [p0, p1, p2, p3]
    
    partition_old = [[[0,1], [0,1]]]
    b = []
    k = 0
    still_to_do = True
    
    while still_to_do==True:
        print(k)
        k += 1
        if k==7:
            break
        n = [0, 0, 0, 0]
        a = c * k**2
        partition_new = []
        for i in range(4**k):
            check = 1
            # print('partition old:', partition_old)
            current_partition = partition_square(partition_old[i//4])[i%4]
            # print('current partition[0]:', current_partition[0])
            partition_new += current_partition
            # print('partition_new:', partition_new)
            n[i%4] = count_data(x_scaled, y_scaled, current_partition[0])
            
            if i%4==3:
                # print('n:', n)
                # print(gamma(n[0]+n[2]+2*a))
                # print(gamma(n[1]+n[3]+2*a))
                # print(gamma(n[0]+n[1]+2*a))
                # print(gamma(n[2]+n[3]+2*a))
                # print(gamma(4*a))
                # print(gamma(a)**4)
                # print('-------------------------')
                # print(loggamma(n[0]+n[1]+n[2]+n[3]+4*a))
                # print(loggamma(n[0]+a))
                # print(loggamma(n[1]+a))
                # print(loggamma(n[2]+a))
                # print(loggamma(n[3]+a))
                # print(4*loggamma(2*a))
                if n[0]+n[1]+n[2]+n[3] > 1:
                    num = loggamma(n[0]+n[2]+2*a) + loggamma(n[1]+n[3]+2*a) + loggamma(n[0]+n[1]+2*a) + loggamma(n[2]+n[3]+2*a) + loggamma(4*a) + 4*loggamma(a)
                    den = loggamma(n[0]+n[1]+n[2]+n[3]+4*a) + loggamma(n[0]+a) + loggamma(n[1]+a) + loggamma(n[2]+a) + loggamma(n[3]+a) + 4*loggamma(2*a)
                    # print('den:', den)
                    # print('lognum:', num)
                    # print('logden:', den)
                    bj = np.exp(num-den)
                    b.append(bj)
                # print('b:', b)
                if (n[0]>1) or (n[1]>1) or (n[2]>1) or (n[3]>1):
                    check = check * 0
        if check == 1:
            still_to_do==False
        partition_old = partition_new
    b_prod = np.prod(b)
    
    return 1/(1+b_prod)
        

        
if __name__ == '__main__':
    # generate x and y with a strong linear dependence
    x = np.random.normal(0, 1, 2000)
    y = np.random.normal(0, 2, 2000) + x
    # plot x and y
    plt.scatter(x,y)
    # The output of the function is the posterior probability of x and y being dependent
    print('Dependence probability:', independence_tester(x, y))
    # Compare with correlation
    print('Correlation: ', pearsonr(x,y))
    
    
    
    