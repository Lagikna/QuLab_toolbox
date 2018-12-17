import numpy as np

clifford_group_singlequbit=np.array([
    [ [1,0] , [0,1] ],
    [ [0,-1j] , [-1j,0] ],
    [ [0,-1] , [1,0] ],
    [ [-1j,0] , [0,1j] ],

    [ [1/np.sqrt(2),-1j/np.sqrt(2)] , [-1j/np.sqrt(2),1/np.sqrt(2)] ],
    [ [1/np.sqrt(2),1j/np.sqrt(2)] , [1j/np.sqrt(2),1/np.sqrt(2)] ],
    [ [1/np.sqrt(2),-1/np.sqrt(2)] , [1/np.sqrt(2),1/np.sqrt(2)] ],
    [ [1/np.sqrt(2),1/np.sqrt(2)] , [-1/np.sqrt(2),1/np.sqrt(2)] ],
    [ [1/np.sqrt(2)-1j/np.sqrt(2),0] , [0,1/np.sqrt(2)+1j/np.sqrt(2)] ],
    [ [1/np.sqrt(2)+1j/np.sqrt(2),0] , [0,1/np.sqrt(2)-1j/np.sqrt(2)] ],

    [ [-1j/np.sqrt(2),-1j/np.sqrt(2)] , [-1j/np.sqrt(2),+1j/np.sqrt(2)] ],
    [ [1j/np.sqrt(2),-1j/np.sqrt(2)] , [-1j/np.sqrt(2),-1j/np.sqrt(2)] ],
    [ [-1j/np.sqrt(2),-1/np.sqrt(2)] , [1/np.sqrt(2),1j/np.sqrt(2)] ],
    [ [1j/np.sqrt(2),-1/np.sqrt(2)] , [1/np.sqrt(2),-1j/np.sqrt(2)] ],
    [ [0,-1/np.sqrt(2)-1j/np.sqrt(2)] , [1/np.sqrt(2)-1j/np.sqrt(2),0] ],
    [  [0,-1/np.sqrt(2)+1j/np.sqrt(2)] , [1/np.sqrt(2)+1j/np.sqrt(2),0] ],

    [ [ 0.5-0.5j, -0.5-0.5j] , [ 0.5-0.5j,  0.5+0.5j] ],
    [ [ 0.5+0.5j, -0.5+0.5j] , [ 0.5+0.5j,  0.5-0.5j] ],
    [ [ 0.5+0.5j, 0.5-0.5j] , [ -0.5-0.5j,  0.5-0.5j] ],
    [ [ 0.5-0.5j, 0.5+0.5j] , [ -0.5+0.5j,  0.5+0.5j] ],
    [ [ 0.5+0.5j, 0.5+0.5j] , [ -0.5+0.5j,  0.5-0.5j] ],
    [ [ 0.5-0.5j, 0.5-0.5j] , [ -0.5-0.5j,  0.5+0.5j] ],
    [ [ 0.5-0.5j, -0.5+0.5j] , [ 0.5+0.5j,  0.5+0.5j] ],
    [ [ 0.5+0.5j, -0.5-0.5j] , [ 0.5-0.5j,  0.5-0.5j] ],
])

clifford_group_singlequbit_index=[    ['I'],
                                      ['X'],
                                      ['Y'],
                                      ['Y','X'],

                                      ['X2p'],
                                      ['X2n'],
                                      ['Y2p'],
                                      ['Y2n'],
                                      ['X2n','Y2p','X2p'],
                                      ['X2n','Y2n','X2p'],

                                      ['X','Y2n'],
                                      ['X','Y2p'],
                                      ['Y','X2p'],
                                      ['Y','X2n'],
                                      ['X2p','Y2p','X2p'],
                                      ['X2n','Y2p','X2n'],

                                      ['Y2p','X2p'],
                                      ['Y2p','X2n'],
                                      ['Y2n','X2p'],
                                      ['Y2n','X2n'],
                                      ['X2p','Y2n'],
                                      ['X2n','Y2n'],
                                      ['X2p','Y2p'],
                                      ['X2n','Y2p'],
                                 ]

def find_reversal(a,b):
    for i in np.arange(len(b)):
        if matrix_compare(a,b[i]) or matrix_compare(-a,b[i])\
         or matrix_compare(1j*a,b[i]) or matrix_compare(-1j*a,b[i]):
            return i

def matrix_compare(a,b):
    row,column=a.shape
    for i in np.arange(row):
        for j in np.arange(column):
            if np.abs(np.real(a[i][j]-b[i][j]))>1e-5 or np.abs(np.imag(a[i][j]-b[i][j]))>1e-5:
                return False
    return True
