"""
@authors: Dario/Sofia/Maria/Alessandro
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

class Scacchiera:
    """
    """
    def __init__(self):
        """
        la scacchiera è rappresentata da due dizionari di liste
        che rappresentano le 64 posizioni attraverso coordinate
        formate da una lettera in ['A', 'H'] e da un numero in [1, 8]
        il primo dizionario memorizza se una casella è non occupata 
        (None) o è occupata (riferimento al pezzo che la occupa)
        il secondo dizionario serve per memorizzare il contenuto
        delle caselle in una forma visualizzabile

        Nell'accesso alle liste che rappresentano le colonne
        della scacchiera bisogna sottrarre 1 perchè gli indici
        delle liste partono da 0
        
        INV: i due dizionari devono essere mantenuti coerenti

        Returns
        -------
        None.

        """
        self.pezzi = {'A': [None]*8,  # memorizza gli oggetti 
                      'B': [None]*8,  # posizionati sulla scacchiera
                      'C': [None]*8,
                      'D': [None]*8,
                      'E': [None]*8,
                      'F': [None]*8,
                      'G': [None]*8,
                      'H': [None]*8}
        self.piano = {'A': [' ']*8,   # memorizza il contenuto delle casella
                      'B': [' ']*8,   # della scacchiera in forma visualizzabile
                      'C': [' ']*8,
                      'D': [' ']*8,
                      'E': [' ']*8,
                      'F': [' ']*8,
                      'G': [' ']*8,
                      'H': [' ']*8}
         
        
    def togli(self, posizione):
        """
        toglie un pezzo dalla scacchiera e lo sostituisce con None

        Parameters
        ----------
        posizione : coppia di coordinate (list)
            posizione da liberare.

        Returns
        -------
        None.

        """
        self.pezzi[posizione[0]][posizione[1] - 1].togli()
        self.pezzi[posizione[0]][posizione[1]-1] = None
        self.piano[posizione[0]][posizione[1]-1] = ' '
    
    def metti(self, pezzo, posizione):
        """
        posiziona un pezzo sulla scacchiera
        e lo associa alla scacchiera

        Parameters
        ----------
        pezzo : pezzo
            pezzo da posizionare
        posizione : coppia di coordinate
            posizione in cui posizionare il pezzo

        Returns
        -------
        None.

        """
        pezzo.metti(posizione, self)  # associa il pezzo alla scacchiera
        self.pezzi[posizione[0]][posizione[1]-1] = pezzo
        self.piano[posizione[0]][posizione[1]-1] = pezzo.get_graphic_rep()
    
    def get_pezzo(self, posizione):
        """
        retituisce un riferimento al pezzo che si trova 
        nella posizione indicata

        Parameters
        ----------
        posizione : coppia di coordinate
            posizione del pezzo

        Returns
        -------
        TYPE Pezzo
            pezzo posizionato nella posizione indicata

        """
        return self.pezzi[posizione[0]][posizione[1]-1]
    
    def visualizza(self, on_click=None):
        """
        Visualizza la scacchiera e i pezzi su matplotlib.
        Se on_click è fornito, lo usa come callback per i click.
        """
        board = np.tile((1,0), (8,4))
        for pos in range(board.shape[0]):
            board[pos] = np.roll(board[pos], pos % 2 )
        cm = ListedColormap(["#0C6104", "#545459FF"])
        fig, ax = plt.subplots()
        ax.imshow(board, cmap=cm)
        # Coordinate corrette
        ax.set_xticks(np.arange(8))
        ax.set_yticks(np.arange(8))

        # Colonne A–H
        ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])

        # Righe 8–1 (invertite perché la grafica parte dall'alto)
        ax.set_yticklabels(['8', '7', '6', '5', '4', '3', '2', '1'])

        ax.tick_params(length=0)
        # Disegna i pezzi
        for col_idx, col in enumerate(self.piano.keys()):
            for row_idx in range(8):
                pezzo = self.piano[col][row_idx]
                if pezzo != ' ':
                    ax.text(col_idx, 7-row_idx, pezzo, ha='center', va='center', fontsize=32)
        # Griglia
        ax.set_xlim(-0.5,7.5)
        ax.set_ylim(-0.5,7.5)
        ax.grid(False)
        # Gestione click
        if on_click:
            fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()


