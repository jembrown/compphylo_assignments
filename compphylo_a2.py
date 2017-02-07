# -*- coding: utf-8 -*-
"""
ZacCarver
02-06-17
CompPhylo assignment 2
"""
#import timeit as timeit
import random

def factori(prod, mn, mx):
	for i in range(mn,mx+1):#for i in range(mn,mx):
		prod = prod*i
	return prod#return prod*mx

#def coef_1(prod, f, mn, mx, k):
    #coef_1 = f/(factori(prod,1,(mx-mn))*k)
    #return coef_1
'''
Ok, so for whatever reason the alternative binomial function was not cooperating.
I believe that a range() should be set to then multiply consecutively in decreasing order?
But this resembles the following function rather closely....
'''  

def coef_2(mn,mx,k):
	#stackoverflow posting help http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
	coef_2 =1#start off the values in a given range at 1
	for n in range(mx, mx-mn, -1):
		coef_2 = coef_2*n#multiply each value in the range to the previous and return
	return coef_2/k#divide the end product by factorial of the mn to obtain the coefficient value
	
def prob_knp(mn, mx, k, p):
    k = int(k)#because the binomial function cannot divide an integer by a float, convert k to integer
    P = coef_2(mn,mx,k)*pow(p,mn)*pow((1-p),(mx-mn))#calculate pmf to return the probability
    return P

def smpl_rand(l, px):
    # posting help: https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch04s22.html
    x = random.uniform(0,1)
    prob_tot = 0.0
    for item, prob_indi in zip(l, px):#for each item and its probability 
        prob_tot += prob_indi
        if x < prob_tot:
            break
    return item

def ML_hill(diff, mn, mx, k, p):
    pCurr = p
    #likeCurr = prob_knp(mn, mx, k, pCurr)
    #like_R = prob_knp(mn, mx, k, pRight)
    #like_L = prob_knp(mn, mx, k, pLeft)
    #print(likeCurr, like_R, like_L, pCurr, pRight, pLeft)
    while diff > 0.000001:
        pUp = pCurr + diff#set the upper parameter 0.1 above the current probability
        pDwn = pCurr - diff#set the lower parameter 0.1 below the current probability
        like_pCurr = prob_knp(mn, mx, k, pCurr)#get the current likelihood of the probability (pmf)
        like_pUp = prob_knp(mn, mx, k, pUp)#get the upper likelihood of the upper parameter
        like_pDwn = prob_knp(mn, mx, k, pDwn)#get the lower likelihood of the lower parameter
        if like_pUp > like_pCurr:
            pCurr = pUp
            #pUp = pCurr + diff #variables in this instance have to be outside of loop
            continue #continues to the next statement
        if like_pDwn > like_pCurr:
            pCurr = pDwn
            #pDwn = pCurr - diff
            continue
        if like_pUp < like_pCurr or like_pDwn < like_pCurr:#once the 'max' has been overshot...
            diff = diff*0.5#change the 'window' and reverse direction
            continue
        if diff < 0.0001:#loop until this threshold is passed, break out of loop and return the desired likelihood.. 
            break
    return like_pCurr        
    
#def sim_likeRatio():
    '''
    Unsure on how to simulate 100 trials using the smpl_rand function from above, if is even possible.
    A range would have to be set in this case for sure...
    After the new list of probabilities are returned from the 100 trials, each would have to be entered 
    into the hill climbing function? After which are divided by p to get the ratios?
    '''
    
def main():
    mn = 6
    mx = 35
    #prod = 1
    #f = factori(prod, mn, mx)
    #f_mn = factori(prod, 1, mn)
    #print(f)
    k = factori(1, 1, mn)
    #n = factori(1, 1, mx)
    print("k =", k)
    p = 0.2
    l = [1,2,3,4]
    px = [0.2, 0.3, 0.1, 0.4]
    diff = 0.1
    #print(coef_1(prod, f, mn, mx, k))
    print(mx, "choose", mn, "=", coef_2(mn,mx,k))
    print(prob_knp(mn, mx, k , p))
    print(smpl_rand(l, px))
    print(ML_hill(diff, mn, mx, k, p))
    
if __name__ == '__main__':
	main()

