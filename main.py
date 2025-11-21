import matplotlib.pyplot as plt
from Scacchiera import Scacchiera
from Torre import Torre
from Alfiere import Alfiere
from Cavallo import Cavallo
from pedone import Pedone

"""
@authors: Dario/Sofia/Maria/Alessandro
"""

# Variabili globali per la selezione
selezione = {'partenza': None, 'destinazione': None}
scacchiera = None  # sarà inizializzata nel main

def coord_da_click(event):
    """Traduce coordinate matplotlib in coordinate scacchiera."""
    if event.inaxes is None:
        return None
    col = int(round(event.xdata))
    row = int(round(event.ydata))
    if 0 <= col < 8 and 0 <= row < 8:
        colonna = list('ABCDEFGH')[col]
        riga = 8 - row
        return [colonna, riga]
    return None

def on_click(event):
    """Gestione click per selezionare e muovere pezzi."""
    global selezione, scacchiera
    pos = coord_da_click(event)
    if pos is None:
        return
    if selezione['partenza'] is None:
        pezzo = scacchiera.get_pezzo(pos)
        if pezzo is not None:
            selezione['partenza'] = pos
            print(f"Selezionata partenza: {pos}")
    else:
        selezione['destinazione'] = pos
        pezzo = scacchiera.get_pezzo(selezione['partenza'])
        if pezzo and pezzo.verifica_mossa(selezione['destinazione']):

            #gestione della mosssa del pedone "EN PASSANT"
            # --- EN PASSANT ---
            if isinstance(pezzo, Pedone):
                r0, c0 = selezione['partenza']
                r1, c1 = selezione['destinazione']
                if abs(c1 - c0) == 1 and r1 != r0:
                    if scacchiera.get_pezzo(selezione['destinazione']) is None:
                        casella_adiacente = [r0, c1]
                        pedone_vicino = scacchiera.get_pezzo(casella_adiacente)
                        if (
                            pedone_vicino is not None
                            and isinstance(pedone_vicino, Pedone)
                            and pedone_vicino.colore != pezzo.colore
                            and getattr(pedone_vicino, "ha_fatto_doppio_passo", False)
                        ):
                            print("Cattura en passant!")
                            scacchiera.togli(casella_adiacente)
            # --- FINE EN PASSANT ---

            if scacchiera.get_pezzo(selezione['destinazione']) is not None:
                scacchiera.togli(selezione['destinazione'])
            scacchiera.togli(selezione['partenza'])
            scacchiera.metti(pezzo, selezione['destinazione'])

            # Gestione della promozione del pedone
            # --- PROMOZIONE PEDONE ---
            if isinstance(pezzo, Pedone):
                r, c = selezione['destinazione']
                if (pezzo.colore == "W" and r == 'H') or (pezzo.colore == "B" and r == 'A'):
                    print("Promozione del pedone!")
                    while True:
                        scelta = input("Promuovi in (Q,R,B,N): ").upper()
                        if scelta in {"Q", "R", "B", "N"}:
                            break
                        print("Scelta non valida.")
                    nuovo = pezzo.promuovi(scelta)
                    scacchiera.togli(selezione['destinazione'])
                    scacchiera.metti(nuovo, selezione['destinazione'])
            # --- FINE PROMOZIONE ---

            print(f"Mossa: {selezione['partenza']} -> {selezione['destinazione']}")
        else:
            print("Mossa non valida")
        selezione = {'partenza': None, 'destinazione': None}
        plt.close()  # Chiudi la finestra per ridisegnare
        scacchiera.visualizza(on_click=on_click)

# Funzioni per posizionare i pezzi
def metti_alfiere(scacchiera: Scacchiera):
    '''
        Mette gli alfieri all'inizio della partita sulla scacchiera

        Parameters
        ----------
        scacchiera : Scacchiera
            scacchiera su cui mettere i pezzi

        Returns
        -------
        None.
    '''
    #bianchi
    scacchiera.metti(Alfiere("W"), ['H', 3])
    scacchiera.metti(Alfiere("W"), ['H', 6])
    #neri
    scacchiera.metti(Alfiere("B"), ['A', 3])
    scacchiera.metti(Alfiere("B"), ['A', 6])

def metti_torre(scacchiera: Scacchiera):
    '''
        Mette le torri all'inizio della partita sulla scacchiera

        Parameters
        ----------
        scacchiera : Scacchiera
            scacchiera su cui mettere i pezzi

        Returns
        -------
        None.
    '''
    #bianchi
    scacchiera.metti(Torre("W"), ['H', 1])
    scacchiera.metti(Torre("W"), ['H', 8])
    #neri
    scacchiera.metti(Torre("B"), ['A', 1])
    scacchiera.metti(Torre("B"), ['A', 8])

def metti_cavallo(scacchiera: Scacchiera):
    '''
        Mette i cavalli all'inizio della partita sulla scacchiera

        Parameters
        ----------
        scacchiera : Scacchiera
            scacchiera su cui mettere i pezzi

        Returns
        -------
        None.
    '''
    #bianchi
    scacchiera.metti(Cavallo("W"), ['H', 2])
    scacchiera.metti(Cavallo("W"), ['H', 7])
    #neri
    scacchiera.metti(Cavallo("B"), ['A', 2])
    scacchiera.metti(Cavallo("B"), ['A', 7])

def metti_pedone(scacchiera: Scacchiera):
    '''
        Mette i pedoni all'inizio della partita sulla scacchiera

        Parameters
        ----------
        scacchiera : Scacchiera
            scacchiera su cui mettere i pezzi

        Returns
        -------
        None.
    '''
    for col in range(1, 9):
        scacchiera.metti(Pedone("W"), ['B', col])
    for col in range(1, 9):
        scacchiera.metti(Pedone("B"), ['G', col])

def metti_re():
    pass

def metti_regina():
    pass

#TODO: gestire la mano
#TODO: fare le directory ordinate
#TODO: scrivere commenti
#TODO: scrivere README
if __name__ == "__main__":
    scacchiera = Scacchiera()
    metti_alfiere(scacchiera)
    metti_torre(scacchiera)
    metti_pedone(scacchiera)

    #metti_re(scacchiera)

    #metti_regina(scacchiera)
    metti_cavallo(scacchiera)
    scacchiera.visualizza(on_click=on_click)
