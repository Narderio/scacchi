#!/usr/bin/env python3
from scacchiera.pezzo import Pezzo


class Re(Pezzo):
    """
    Implementa il Re (King).
    Movimento: massimo una casella in qualsiasi direzione.
    (Arrocco non gestito in questa versione.)
    """
    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Re')
        # Seguire la convenzione usata nel progetto per le rappresentazioni
        self.graphic_rep = '\u265A' if self.colore == 'W' else '\u2654'

    def verifica_mossa(self, destinazione):
        """
        Verifica che il Re si muova di al massimo una casella
        in orizzontale, verticale o diagonale.
        """
        if not super().verifica_mossa(destinazione):
            return False

        col_from = ord(self.posizione[0])
        row_from = self.posizione[1]
        col_to = ord(destinazione[0])
        row_to = destinazione[1]

        dc = abs(col_to - col_from)
        dr = abs(row_to - row_from)

        # nessun movimento non valido (stessa casella)
        if dc == 0 and dr == 0:
            print(f'La mossa {self.posizione[0]}{self.posizione[1]} -> {destinazione[0]}{destinazione[1]} non è legale per il Re')
            return False

        # al massimo una casella in qualsiasi direzione
        if dc <= 1 and dr <= 1:
            return True

        print(f'La mossa {self.posizione[0]}{self.posizione[1]} -> {destinazione[0]}{destinazione[1]} non è legale per il Re')
        return False
