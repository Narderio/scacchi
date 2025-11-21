#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pedone completo:
- Movimento base, doppio passo, cattura, en passant
- Promozione dinamica (Q, R, B, N)
"""

from Alfiere import Alfiere
from Pezzo import Pezzo
from Torre import Torre
# from Regina import Regina
#from Cavallo import Cavallo


class Pedone(Pezzo):

    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Pedone')
        self.graphic_rep = '\u2659' if self.colore == 'W' else '\u265F'
        self.ha_fatto_doppio_passo = False

    def verifica_mossa(self, destinazione):

        if not super().verifica_mossa(destinazione):
            return False

        r0, c0 = self.posizione
        r1, c1 = destinazione

        delta_riga = ord(r1) - ord(r0)
        delta_colonna = c1 - c0

        # direzione dei pedoni
        direzione = 1 if self.colore == 'W' else -1

        pezzo_dest = self.scacchiera.get_pezzo(destinazione)

        # Movimento verticale senza cattura
        if delta_colonna == 0:

            # casella occupata → non può avanzare
            if pezzo_dest is not None:
                print("Il pedone non può avanzare su una casella occupata.")
                return False

            # passo singolo
            if delta_riga == direzione:
                self.ha_fatto_doppio_passo = False
                return True

            # doppio passo
            if delta_riga == 2 * direzione:
                riga_iniziale = 'B' if self.colore == 'W' else 'G'

                if r0 != riga_iniziale:
                    print("Il doppio passo è consentito solo dalla riga iniziale.")
                    return False

                # verifica casella intermedia
                casella_intermedia = [chr(ord(r0) + direzione), c0]
                if self.scacchiera.get_pezzo(casella_intermedia) is not None:
                    print("La casella intermedia è occupata.")
                    return False

                self.ha_fatto_doppio_passo = True
                return True

            return False

        # Cattura diagonale
        if abs(delta_colonna) == 1 and delta_riga == direzione:

            # cattura normale
            if pezzo_dest is not None:
                if pezzo_dest.colore != self.colore:
                    self.ha_fatto_doppio_passo = False
                    return True
                else:
                    print("Non puoi catturare un tuo pezzo.")
                    return False

            # en passant
            casella_adiacente = [r0, c1]
            pedone_vicino = self.scacchiera.get_pezzo(casella_adiacente)

            if (
                pedone_vicino is not None
                and isinstance(pedone_vicino, Pedone)
                and pedone_vicino.colore != self.colore
                and pedone_vicino.ha_fatto_doppio_passo
            ):
                return True

            return False

        # mossa non valda
        return False

    def promuovi(self, scelta):
        """Restituisce il pezzo risultante dalla promozione."""
        """
        if scelta == "Q":
            #return Regina(self.colore, self.posizione)
        """
        if scelta == "R":
            return Torre(self.colore, self.posizione)
        """
        elif scelta == "N":
            #return Cavallo(self.colore, self.posizione)
        """
        if scelta == "B":
            return Alfiere(self.colore, self.posizione)
        else:
            raise ValueError("Scelta promozione non valida.")


