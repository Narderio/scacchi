#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Dario/Sofia/Maria/Alessandro
"""

from scacchiera.pezzo import Pezzo

class Cavallo(Pezzo):
    """
    Implementa il Cavallo
    """

    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Cavallo')
        # Imposta la rappresentazione Unicode del cavallo bianco (♘) o nero (♞)
        self.graphic_rep = '\u2658' if self.colore == 'W' else '\u265e'

    def verifica_mossa(self, destinazione):
        """
        Verifica se il Cavallo può essere mosso alla destinazione

        Parameters
        ----------
        destinazione : coppia di coordinate (list)
            posizione di destinazione della mossa

        Returns
        -------
        bool
            indica se la mossa è legale o no
        """
        # Verifica prima le condizioni generali del pezzo (posizione valida, turno, ecc.)
        if not super().verifica_mossa(destinazione):
            print(f'La mossa {self.posizione} -> {destinazione} non è legale per il Cavallo')
            return False

        # Estrae colonna e riga della posizione corrente
        col_from = ord(self.posizione[0])  # Converte lettera colonna in numero ASCII
        row_from = self.posizione[1]
        # Estrae colonna e riga della destinazione
        col_to = ord(destinazione[0])
        row_to = destinazione[1]

        # Calcola la differenza assoluta tra colonne e righe
        dc = abs(col_from - col_to)
        dr = abs(row_from - row_to)

        # Il cavallo si muove in L: 2 passi in una direzione e 1 nell'altra
        # Controlla se la mossa forma una L (2+1 o 1+2)
        if (dc == 2 and dr == 1) or (dc == 1 and dr == 2):
            return True
        else:
            print(f'La mossa {self.posizione} -> {destinazione} non è legale per il Cavallo')
            return False