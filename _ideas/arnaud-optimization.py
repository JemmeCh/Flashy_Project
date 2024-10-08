import numpy as np
import matplotlib.pyplot as plt

from timeit import default_timer as timer

def generateur(debut, fin, precision, nm) :
    """
    onde carrée
    """

    start = timer()
    sigma = ( fin - debut ) / 2
    delta = 2
    x, dx = np.linspace(debut, fin, precision, retstep=True)

    # doit être -1 ou 1
    switch = x / fin >= 0.5
    switch_int = switch.astype(int) * 2
    y = np.zeros_like(x) + np.ones_like(x) * delta/2 * ( np.ones_like(x) - switch_int  )

    # an
    # intégrale numérique
    # a0 équation différente

    frequence = 10
    w = 2*np.pi * frequence
    n = np.ones( (1, nm) ) * np.arange(nm)    # nous retourne une matrice de n par 1, nécéssaire pour prendre la transposé
    parr = y * np.cos( n.T * w * x )          # intérieure de l'intégrale de a_n, le résultat est une matrice de n par x
    inte = np.sum( parr * dx, axis=1 )        # l'intégrale, on somme tout les éléments selon l'axe 1, soit chaque x pour un n
                                              # nous retourne alors x terme
    a_n = 2 / (2*sigma) * inte                # finissions du calcul
    a_n[0] = 1 / (2*sigma) * np.sum( y * dx ) # a_0 est une exception 
    a_n = a_n * np.ones( (1, nm) )            # on met a_n sous forme matricielle, même principe que pour n

    # bn
    pars = y * np.sin(n.T * w * x)            # même chose que a_n, mais avec sin
    ints = np.sum( pars * dx, axis=1 )
    b_n = 2 / (2 * sigma) * ints * np.ones( ( 1, nm ) )

    # total
    
    #print(a_n)
    #print(b_n)

    y_2 = np.sum( a_n.T * np.cos( n.T * w * x ) + b_n.T * np.sin( n.T * w * x ), axis=0 )       # on met tout ensemble
                                        # l'intérieure de la somme est encore une matrice
                                        # on fait la somme pour avoir y pour chaque point de x, l'axe 0
    print(timer() - start)
    

    plt.plot(x, y_2, label="pog")
    plt.plot(x, y, label="og", ls="-.")
    plt.legend()
    plt.show()


if __name__ == "__main__" :
    p = 10000
    generateur(0, 0.1, p, 1000)
