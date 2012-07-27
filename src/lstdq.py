#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: LSTDQ.PY
Date: Wednesday, December 16 2009
Description: LSTDQ implementation from Lagoudakis and Parr. 2003. Least-Squares Policy Iteration. Journal of Machine Learning Research.
"""

import os, sys, getopt, pdb, string

import numpy as np
import numpy.random as npr
import random as pr
import numpy.linalg as la
from utils import debugflag, timerflag


@debugflag
@timerflag
def LSTDQ(D,env,w):
    """
    D : source of samples (s,a,r,s',a')
    env: environment contianing k,phi,gamma
    w : weights for the linear policy evaluation
    """

    k = -1
    k = len(w)

    A = np.zeros((k,k))
    b = np.zeros(k)

    i = 0
    for (s,a,r,ns,na) in D:

        #print i
        i += 1

        features = env.phi(s,a)

        # we may want to evaluate policies whose features are
        # different from ones that can express the true value
        # function, e.g. tabular

        next = env.linear_policy(w, ns)
        newfeatures = env.phi(ns, next)

        A = A + np.outer(features, features - env.gamma * newfeatures)
        b = b + features * r

    return np.dot(la.pinv(A), b)

import scipy.sparse as sp
import scipy.sparse.linalg as spla

@debugflag
@timerflag
def FastLSTDQ(D,env,w):
    """
    Employ as many tricky speedups as I can for large (sparse) phi.
    
    D : source of samples (s,a,r,s',a')
    env: environment contianing k,phi,gamma
    w : weights for the linear policy evaluation
    """

    k = -1
    k = len(w)

    A = sp.csr_matrix((k,k), dtype=float)
    b = sp.csr_matrix((k,1), dtype=float)


    i = 0
    for (s,a,r,ns,na) in D:

        i += 1

        features = sp.csr_matrix(env.phi(s,a))

        # we may want to evaluate policies whose features are
        # different from ones that can express the true value
        # function, e.g. tabular

        next = env.linear_policy(w, ns)
        newfeatures = sp.csr_matrix(env.phi(ns, next))

        A = A + np.dot(features.T,features - env.gamma * newfeatures)
        b = b + features.T * r

    # TODO : Not sure what solver method to use here.
    #return spla.spsolve(A,b)
    stuff = spla.lsqr(A,b.toarray())
    return stuff[0]


if __name__ == '__main__':

    pass
