#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:10:02 2022

@author: iannello
"""
from scacchiera.pezzo import Pezzo


class Regina(Pezzo):
    """
    implementa la Regina
    """

    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Regina')
        self.graphic_rep = '\u265b' if self.colore == 'W' else '\u2655'

    def verifica_mossa(self, destinazione):
        """
        Verifica se la Regina può essere mossa alla destinazione.

        La Regina può muovere:
        - lungo la stessa colonna (movimento verticale)
        - lungo la stessa riga (movimento orizzontale)
        - lungo una diagonale (movimento diagonale)

        La funzione verifica inoltre che non ci siano pezzi intermedi
        tra la posizione di partenza e quella di arrivo.
        """

        if super().verifica_mossa(destinazione):  # le condizioni generiche sono verificate

            # MOVIMENTO VERTICALE
            if self.posizione[0] == destinazione[0]:

                # devo verificare che non ci siano pezzi tra la partenza e l'arrivo
                # per farlo devo distinguere se il movimento avviene verso l'alto o verso il basso
                first = self.posizione[1] + 1 if self.posizione[1] + 1 < destinazione[1] else destinazione[1] + 1  # prima riga da controllare
                last = destinazione[1] if self.posizione[1] + 1 < destinazione[1] else self.posizione[1]  # ultima riga da controllare

                for riga in range(first, last):  # controllo caselle intermedie
                    if not self.scacchiera.get_pezzo([destinazione[0], riga]) == None:
                        print(f"La mossa non è legale perché è presente un pezzo ({self.scacchiera.get_pezzo([destinazione[0], riga]).nome}) nella casella {destinazione[0]}{riga}")
                        return False

                return True

            # MOVIMENTO ORIZZONTALE
            elif self.posizione[1] == destinazione[1]:

                # distinguo il caso di movimento verso destra o verso sinistra
                first = ord(self.posizione[0]) + 1 if ord(self.posizione[0]) + 1 < ord(destinazione[0]) else ord(destinazione[0]) + 1  # prima colonna da controllare
                last = ord(destinazione[0]) if ord(self.posizione[0]) + 1 < ord(destinazione[0]) else ord(self.posizione[0])  # ultima colonna da controllare

                for col in range(first, last):
                    if not self.scacchiera.get_pezzo([chr(col), destinazione[1]]) == None:
                        print(f"La mossa non è legale perché è presente un pezzo ({self.scacchiera.get_pezzo([chr(col), destinazione[1]]).nome}) nella casella {chr(col)}{destinazione[1]}")
                        return False

                return True

            # MOVIMENTO DIAGONALE
            else:
                # devo controllare che si tratti di una vera diagonale
                diff_col = abs(ord(destinazione[0]) - ord(self.posizione[0]))  # quanto cambia la colonna
                diff_riga = abs(destinazione[1] - self.posizione[1])  # quanto cambia la riga

                if diff_col != diff_riga or diff_col == 0:  # non è una diagonale valida
                    print(f"La mossa {self.posizione[0]}{self.posizione[1]} -> {destinazione[0]}{destinazione[1]} non è legale per la Regina")
                    return False

                # stabilisco la direzione del movimento
                passo_col = 1 if ord(destinazione[0]) > ord(self.posizione[0]) else -1
                passo_riga = 1 if destinazione[1] > self.posizione[1] else -1

                # controllo tutte le caselle intermedie lungo la diagonale
                for i in range(1, diff_col):
                    col_attuale = chr(ord(self.posizione[0]) + passo_col * i)
                    riga_attuale = self.posizione[1] + passo_riga * i

                    if not self.scacchiera.get_pezzo([col_attuale, riga_attuale]) == None:
                        print(f"La mossa non è legale perché è presente un pezzo ({self.scacchiera.get_pezzo([col_attuale, riga_attuale]).nome}) nella casella {col_attuale}{riga_attuale}")
                        return False

                return True

        else:
            # la mossa non soddisfa le condizioni generiche
            print(f"La mossa {self.posizione[0]}{self.posizione[1]}, {destinazione[0]}{destinazione[1]} non è legale per la Regina")
            return False
