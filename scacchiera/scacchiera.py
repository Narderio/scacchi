"""
@authors: Dario/Sofia/Maria/Alessandro
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from scacchiera.pezzi.re import Re


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
        self.pezzi = {'A': [None] * 8,  # memorizza gli oggetti
                      'B': [None] * 8,  # posizionati sulla scacchiera
                      'C': [None] * 8,
                      'D': [None] * 8,
                      'E': [None] * 8,
                      'F': [None] * 8,
                      'G': [None] * 8,
                      'H': [None] * 8}
        self.piano = {'A': [' '] * 8,  # memorizza il contenuto delle casella
                      'B': [' '] * 8,  # della scacchiera in forma visualizzabile
                      'C': [' '] * 8,
                      'D': [' '] * 8,
                      'E': [' '] * 8,
                      'F': [' '] * 8,
                      'G': [' '] * 8,
                      'H': [' '] * 8}

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
        self.pezzi[posizione[0]][posizione[1] - 1] = None
        self.piano[posizione[0]][posizione[1] - 1] = ' '

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
        self.pezzi[posizione[0]][posizione[1] - 1] = pezzo
        self.piano[posizione[0]][posizione[1] - 1] = pezzo.get_graphic_rep()

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
        return self.pezzi[posizione[0]][posizione[1] - 1]

    def visualizza(self, on_click=None):
        """
        Visualizza la scacchiera e i pezzi su matplotlib.
        Se on_click è fornito, lo usa come callback per i click.
        """
        board = np.tile((1, 0), (8, 4))
        for pos in range(board.shape[0]):
            board[pos] = np.roll(board[pos], pos % 2)
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
                    ax.text(col_idx, 7 - row_idx, pezzo, ha='center', va='center', fontsize=32)
        # Griglia
        ax.set_xlim(-0.5, 7.5)
        ax.set_ylim(-0.5, 7.5)
        ax.grid(False)
        # Gestione click
        if on_click:
            fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()

    def re_sotto_scacco(self, colore_re):
        """
        Controlla se il re del colore specificato è sotto scacco

        Parameters
        ----------
        colore_re : str
            Colore del re da controllare ('W' o 'B')

        Returns
        -------
        bool
            True se il re è sotto scacco, False altrimenti
        """
        # Trova la posizione del re
        posizione_re = None
        for col in 'ABCDEFGH':
            for riga in range(1, 9):
                pezzo = self.get_pezzo([col, riga])
                if pezzo and isinstance(pezzo, Re) and pezzo.colore == colore_re:
                    posizione_re = [col, riga]
                    break
            if posizione_re:
                break

        if not posizione_re:
            return False  # Re non trovato (caso anomalo)

        # Colore avversario
        colore_avversario = 'B' if colore_re == 'W' else 'W'

        # Controlla se qualche pezzo avversario può raggiungere il re
        for col in 'ABCDEFGH':
            for riga in range(1, 9):
                pezzo = self.get_pezzo([col, riga])
                if pezzo and pezzo.colore == colore_avversario:
                    # Verifica se il pezzo può raggiungere la posizione del re
                    if pezzo.verifica_mossa(posizione_re):
                        return True

        return False

    def re_sotto_scacco_matto(self, colore_re):
        """
        Controlla se il re del colore specificato è sotto scacco matto

        Parameters
        ----------
        colore_re : str
            Colore del re da controllare ('W' o 'B')

        Returns
        -------
        bool
            True se il re è sotto scacco matto, False altrimenti
        """
        if not self.re_sotto_scacco(colore_re):
            return False

        # Trova la posizione del re
        posizione_re = None
        for col in 'ABCDEFGH':
            for riga in range(1, 9):
                pezzo = self.get_pezzo([col, riga])
                if pezzo and isinstance(pezzo, Re) and pezzo.colore == colore_re:
                    posizione_re = [col, riga]
                    break
            if posizione_re:
                break

        if not posizione_re:
            return False

        # Controlla se il re può muoversi in una posizione sicura
        col_re = ord(posizione_re[0])
        riga_re = posizione_re[1]

        # Tutte le possibili posizioni adiacenti al re
        possibili_posizioni = []
        for dc in [-1, 0, 1]:
            for dr in [-1, 0, 1]:
                if dc == 0 and dr == 0:
                    continue
                nuova_col = chr(col_re + dc)
                nuova_riga = riga_re + dr
                if 'A' <= nuova_col <= 'H' and 1 <= nuova_riga <= 8:
                    possibili_posizioni.append([nuova_col, nuova_riga])

        # Verifica se il re può muoversi in almeno una posizione sicura
        for pos in possibili_posizioni:
            pezzo_destinazione = self.get_pezzo(pos)
            # La posizione deve essere vuota o occupata da pezzo avversario
            if pezzo_destinazione is None or pezzo_destinazione.colore != colore_re:
                # Simula la mossa del re
                re = self.get_pezzo(posizione_re)
                pezzo_catturato = self.get_pezzo(pos)

                # Muovi temporaneamente il re
                self.togli(posizione_re)
                if pezzo_catturato:
                    self.togli(pos)
                self.metti(re, pos)

                # Controlla se il re è ancora sotto scacco nella nuova posizione
                sotto_scacco_nuova_pos = self.re_sotto_scacco(colore_re)

                # Ripristina la posizione originale
                self.togli(pos)
                self.metti(re, posizione_re)
                if pezzo_catturato:
                    self.metti(pezzo_catturato, pos)

                # Se la nuova posizione è sicura, il re non è sotto scacco matto
                if not sotto_scacco_nuova_pos:
                    return False

        # Se siamo arrivati qui, il re non può muoversi in nessuna posizione sicura
        # Ora dobbiamo controllare se qualche pezzo amico può salvare il re

        # Trova tutti i pezzi amici
        pezzi_amici = []
        for col in 'ABCDEFGH':
            for riga in range(1, 9):
                pezzo = self.get_pezzo([col, riga])
                if pezzo and pezzo.colore == colore_re and not isinstance(pezzo, Re):
                    pezzi_amici.append((pezzo, [col, riga]))

        # Per ogni pezzo amico, controlla se può fare una mossa che salva il re
        for pezzo, pos_pezzo in pezzi_amici:
            # Trova tutte le possibili mosse per questo pezzo
            for col_dest in 'ABCDEFGH':
                for riga_dest in range(1, 9):
                    dest = [col_dest, riga_dest]
                    if pezzo.verifica_mossa(dest):
                        # Simula la mossa
                        pezzo_dest = self.get_pezzo(dest)

                        self.togli(pos_pezzo)
                        if pezzo_dest:
                            self.togli(dest)
                        self.metti(pezzo, dest)

                        # Controlla se il re è ancora sotto scacco
                        ancora_sotto_scacco = self.re_sotto_scacco(colore_re)

                        # Ripristina
                        self.togli(dest)
                        self.metti(pezzo, pos_pezzo)
                        if pezzo_dest:
                            self.metti(pezzo_dest, dest)

                        # Se la mossa salva il re, non è scacco matto
                        if not ancora_sotto_scacco:
                            return False

        # Se nessuna mossa può salvare il re, è scacco matto
        return True