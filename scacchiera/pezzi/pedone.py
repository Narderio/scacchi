"""
@authors: Dario/Sofia/Maria/Alessandro
"""

from scacchiera.pezzi.alfiere import Alfiere
from scacchiera.pezzo import Pezzo
from scacchiera.pezzi.torre import Torre
from scacchiera.pezzi.cavallo import Cavallo


class Pedone(Pezzo):
    """
    implementa il Pedone
    """
    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Pedone')
        self.graphic_rep = '\u265F' if self.colore == 'W' else '\u2659'
        self.ha_fatto_doppio_passo = False

    def verifica_mossa(self, destinazione):
        """
        Verifica se il pedone può essere mosso alla destinazione

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
            return False

        r0, c0 = self.posizione
        r1, c1 = destinazione

        delta_riga = ord(r1) - ord(r0)
        delta_col = c1 - c0

        direzione = +1 if self.colore == "W" else -1

        pezzo_dest = self.scacchiera.get_pezzo(destinazione)

        # Movimento verticale senza cattura
        if delta_col == 0:

            if pezzo_dest is not None:
                print("Il pedone non può avanzare su casella occupata.")
                return False

            # passo singolo
            if delta_riga == direzione:
                self.ha_fatto_doppio_passo = False
                return True

            # doppio passo
            if delta_riga == 2 * direzione:
                riga_iniziale = 'B' if self.colore == "W" else 'G'

                if r0 != riga_iniziale:
                    return False

                # controllo casella intermedia
                casella_intermedia = [chr(ord(r0) + direzione), c0]
                if self.scacchiera.get_pezzo(casella_intermedia) is not None:
                    return False

                self.ha_fatto_doppio_passo = True
                return True

            return False

        # Cattura diagonale o en passant
        if abs(delta_col) == 1 and delta_riga == direzione:

            # cattura normale
            if pezzo_dest is not None:
                return pezzo_dest.colore != self.colore

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

        return False

    def promuovi(self, scelta):
        """Restituisce il pezzo risultante dalla promozione."""
        """
        if scelta == "Q":
            #return Regina(self.colore, self.posizione)
        """
        if scelta == "R":
            return Torre(self.colore, self.posizione)
        elif scelta == "N":
            return Cavallo(self.colore, self.posizione)
        elif scelta == "B":
            return Alfiere(self.colore, self.posizione)
        else:
            raise ValueError("Scelta promozione non valida.")


