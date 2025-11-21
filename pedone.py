"""
Implementazione del Pedone con:
- movimento base
- doppio passo
- cattura in diagonale
- en passant (controllo nella verifica della mossa)
- promozione
"""

from Pezzo import Pezzo


class Pedone(Pezzo):
    """
    implementa il Pedone
    """

    def __init__(self, colore, posizione=None):
        super().__init__(colore, posizione, 'Pedone')
        self.graphic_rep = '\u2659' if self.colore == 'W' else '\u265F'

        # Indica se questo pedone ha fatto il doppio passo nell'ultima mossa
        self.ha_fatto_doppio_passo = False

    def verifica_mossa(self, destinazione):
        """
        Verifica se la mossa del pedone è legale.
        """

        # Controlli generici
        if not super().verifica_mossa(destinazione):
            print(f"La mossa {self.posizione[0]}{self.posizione[1]} -> {destinazione[0]}{destinazione[1]} non è legale per il Pedone")
            return False

        col_o = self.posizione[0]
        row_o = self.posizione[1]
        col_d = destinazione[0]
        row_d = destinazione[1]

        dcol = ord(col_d) - ord(col_o)
        drow = row_d - row_o

        direzione = 1 if self.colore == 'W' else -1

        pezzo_dest = self.scacchiera.get_pezzo(destinazione)

        # Movimento verticale
        if dcol == 0:

            if pezzo_dest is not None:
                print("Il pedone non può catturare muovendosi in avanti.")
                return False

            # passo singolo
            if drow == direzione:
                self.ha_fatto_doppio_passo = False
                return True

            # doppio passo
            if drow == 2 * direzione:

                riga_iniziale = 2 if self.colore == 'W' else 7
                if row_o != riga_iniziale:
                    print("Il doppio passo è consentito solo dalla riga iniziale.")
                    return False

                # casella intermedia vuota?
                casella_intermedia = [col_o, row_o + direzione]
                if self.scacchiera.get_pezzo(casella_intermedia) is not None:
                    print(f"La casella {casella_intermedia[0]}{casella_intermedia[1]} è occupata.")
                    return False

                self.ha_fatto_doppio_passo = True
                return True

            print("Mossa verticale non valida per il pedone.")
            return False

        # Cattura in diagonale
        if abs(dcol) == 1 and drow == direzione:

            # cattura normale
            if pezzo_dest is not None:
                if pezzo_dest.colore == self.colore:
                    print("Non puoi catturare un tuo pezzo.")
                    return False
                self.ha_fatto_doppio_passo = False
                return True

            # Implementazione en passant
            casella_vicino = [col_d, row_o]
            pedone_vicino = self.scacchiera.get_pezzo(casella_vicino)

            if (
                pedone_vicino is not None
                and isinstance(pedone_vicino, Pedone)
                and pedone_vicino.colore != self.colore
                and pedone_vicino.ha_fatto_doppio_passo
            ):
                # la rimozione effettiva viene fatta nel main
                return True

            print("La mossa diagonale non è valida senza catturare.")
            return False

        # Tutte le altre mosse sono illegali
        print(f"La mossa {col_o}{row_o} -> {col_d}{row_d} non è legale per il Pedone.")
        return False

    def promuovi(self, scelta):
        """
        Crea il pezzo risultante dalla promozione
        scelta: 'Q', 'R', 'B', 'N'
        """
        """if scelta == "Q":
            from Regina import Regina
            return Regina(self.colore, self.posizione)
        """
        if scelta == "R":
            from Torre import Torre
            return Torre(self.colore, self.posizione)
        if scelta == "B":
            from Alfiere import Alfiere
            return Alfiere(self.colore, self.posizione)
        """
        if scelta == "N":
            from Cavallo import Cavallo
            return Cavallo(self.colore, self.posizione)
        """
        # non dovrebbe mai succedere
        raise ValueError("Scelta di promozione non valida")