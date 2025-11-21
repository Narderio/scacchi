#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 10:10:02 2025

@authors: Dario/Sofia/Maria/Alessandro
"""

from Pezzo import Pezzo


class Alfiere(Pezzo):
    """
    implementa l'Alfiere
    """

    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Alfiere')
        self.graphic_rep = '\u2657' if self.colore == 'W' else '\u265d'

    def verifica_mossa(self, destinazione):
        """
        verifica se l'Alfiere può essere mosso alla destinazione

        Parameters
        ----------
        destinazione : coppia di coordinate (list)
            posizione di destinazione della mossa

        Returns
        -------
        bool
            indica se la mossa è legale o no

        """
        if super().verifica_mossa(destinazione):  # le condizioni generiche sono verificate
            # Calcola le differenze tra posizioni
            delta_riga = abs(ord(destinazione[0]) - ord(self.posizione[0]))
            delta_colonna = abs(destinazione[1] - self.posizione[1])
            
            if delta_riga == delta_colonna and delta_riga > 0:  # la mossa è lungo una diagonale
                # Determina la direzione del movimento
                dir_riga = 1 if ord(destinazione[0]) > ord(self.posizione[0]) else -1
                dir_colonna = 1 if destinazione[1] > self.posizione[1] else -1
                
                # Verifica che non ci siano pezzi tra la casella di partenza e quella di arrivo
                for i in range(1, delta_riga):
                    riga_corrente = chr(ord(self.posizione[0]) + i * dir_riga)
                    colonna_corrente = self.posizione[1] + i * dir_colonna
                    pezzo_intermedio = self.scacchiera.get_pezzo([riga_corrente, colonna_corrente])
                    if not pezzo_intermedio is None:  # la casella è occupata
                        print(f"La mossa non è legale perché è presente un pezzo ({pezzo_intermedio.nome}) nella casella {riga_corrente}{colonna_corrente}")
                        return False
                return True
            else:
                print(f'La mossa {self.posizione[0]}{self.posizione[1]} -> {destinazione[0]}{destinazione[1]} non è legale per l\'Alfiere')
                return False
        else:
            print(f'La mossa {self.posizione[0]}{self.posizione[1]} -> {destinazione[0]}{destinazione[1]} non è legale per l\'Alfiere')
            return False