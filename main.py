#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 10:42:39 2022

@author: iannello

"""

from Scacchiera import Scacchiera
from Torre import Torre
from Alfiere import Alfiere
from pedone import Pedone

def metti_alfiere(scacchiera: Scacchiera):
    #bianchi
    alfiere1= Alfiere("W")
    scacchiera.metti(alfiere1, ['H', 3])
    alfiere2= Alfiere("W")
    scacchiera.metti(alfiere2, ['H', 6])

    #neri
    alfiere3= Alfiere("B")
    scacchiera.metti(alfiere3, ['A', 3])
    alfiere4= Alfiere("B")
    scacchiera.metti(alfiere4, ['A', 6])

def metti_torre(scacchiera: Scacchiera):
    #bianchi
    torre1= Torre("W")
    scacchiera.metti(torre1, ['H', 1])
    torre2= Torre("W")
    scacchiera.metti(torre2, ['H', 8])

    #neri
    torre3= Torre("B")
    scacchiera.metti(torre3, ['A', 1])
    
    torre4= Torre("B")
    scacchiera.metti(torre4, ['A', 8])

def metti_cavallo():
    pass


def metti_pedone(scacchiera: Scacchiera):
    for col in "ABCDEFGH":
        scacchiera.metti(Pedone("W"), [col, 2])
    for col in "ABCDEFGH":
        scacchiera.metti(Pedone("B"), [col, 7])

def metti_re():
    pass

def metti_regina():
    pass


def in_board(posizione):
    """
    verifica che la posizione sia all'intgerno della scacchiera
    Parameters
    ----------
    posizione: coppia di coordinate

    Returns
    -------
    bool
        True se le coordinate corrispondono a una casella della
        scacchiera, False altrimenti
    """
    return posizione[0] in {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'} and \
           posizione[1] in range(1, 9)


def get_mossa():
    """
    acquisisce una mossa dallo standard input o termina il programma
    La mossa deve essere fornita nel formato:
        
        posizione_di_partenza posizione_di_destinazione
        
    dove una posizione è una coppia formata da una lettera
    in ['A', 'H'] e da una cifra in [1, 8]
    le due posizioni devono essere separate da un solo spazio

    se la lunghezza della stringa fornita in input è diversa
    da 5 il programma viene terminato

    Returns
    -------
    list
        posizione di partenza
    list
        posizione di destinazione

    """
    while True:
        mossa = input("Dammi la mossa: ")
        if not len(mossa) == 5:  # l'input non è una mossa
            exit(0)              # termina il programma
        partenza = [mossa[0].upper(), int(mossa[1])]
        destinazione = [mossa[3].upper(), int(mossa[4])]
        if in_board(partenza) and in_board(destinazione):
            return partenza, destinazione
        else:
            print(f'La partenza e/o la destinazione della mossa {mossa} non corrispondono a caselle della scacchiera')


if __name__ == "__main__":
    # setup del gioco
    scacchiera = Scacchiera()
    # posizione 4 pezzi bianchi nelle prime 4 righe della colonna A
    
    metti_alfiere(scacchiera)
    
    metti_torre(scacchiera)
    
    metti_pedone(scacchiera)

    #metti_re(scacchiera)

    #metti_regina(scacchiera)

    #metti_cavallo(scacchiera)

    scacchiera.visualizza()
    print()

    # inizia il gioco
    while True:
        while True:
            # acquisisce mossa da fare
            (partenza, destinazione) = get_mossa()
            # recupera il pezzo da muovere
            pezzo = scacchiera.get_pezzo(partenza)
            if pezzo is None:  # la mossa parte da una casella vuota
                print(f'La mossa non è valida: la casella di partenza è vuota')
            elif pezzo.verifica_mossa(destinazione):  # la mossa è legale
                break
        # 2) EN PASSANT
        if isinstance(pezzo, Pedone):
            col_o, row_o = partenza
            col_d, row_d = destinazione
            diagonale = abs(ord(col_d) - ord(col_o)) == 1 and (row_d - row_o != 0)

            if diagonale and scacchiera.get_pezzo(destinazione) is None:
                casella_vicino = [col_d, row_o]
                pedone_vicino = scacchiera.get_pezzo(casella_vicino)
                if (
                    pedone_vicino is not None
                    and isinstance(pedone_vicino, Pedone)
                    and pedone_vicino.colore != pezzo.colore
                    and pedone_vicino.ha_fatto_doppio_passo
                ):
                    print("Cattura en passant!")
                    scacchiera.togli(casella_vicino)

        # esegui mossa sulla scacchiera
        if not scacchiera.get_pezzo(destinazione) is None:  # la casella è occupata
            scacchiera.togli(destinazione)  # "mangia" il pezzo che occupa la casella
        scacchiera.togli(partenza)
        scacchiera.metti(pezzo, destinazione)

        # 5) PROMOZIONE CON SCELTA
        if isinstance(pezzo, Pedone):
            col, row = destinazione
            if (pezzo.colore == "W" and row == 8) or (pezzo.colore == "B" and row == 1):
                print("Promozione del pedone!")
                while True:
                    scelta = input("Scegli la nuova pedina (Q=Regina, R=Torre, B=Alfiere, N=Cavallo): ").upper()
                    if scelta in {"Q", "R", "B", "N"}:
                        break
                    print("Scelta non valida.")

                nuovo = pezzo.promuovi(scelta)
                scacchiera.togli(destinazione)
                scacchiera.metti(nuovo, destinazione)
                print(f"Il pedone è stato promosso a {nuovo.nome}!")

        scacchiera.visualizza()
        print()

