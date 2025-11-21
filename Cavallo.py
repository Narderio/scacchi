#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 2025

@author: Sofia
"""

from Pezzo import Pezzo

class Cavallo(Pezzo):
    """
    Implementa il Cavallo
    """

    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Cavallo')
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
        if not super().verifica_mossa(destinazione):
            print(f'La mossa {self.posizione} -> {destinazione} non è legale per il Cavallo')
            return False

        col_from = ord(self.posizione[0])
        row_from = self.posizione[1]
        col_to = ord(destinazione[0])
        row_to = destinazione[1]

        dc = abs(col_from - col_to)
        dr = abs(row_from - row_to)

        if (dc == 2 and dr == 1) or (dc == 1 and dr == 2):
            return True
        else:
            print(f'La mossa {self.posizione} -> {destinazione} non è legale per il Cavallo')
            return False