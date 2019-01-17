class Gamer:
    def __init__(self, username, deck, win):
        self.username = username
        self.deck = deck
        self.win = win

def game(gamer1, gamer2):
    class Round:
        def __init__(self, gagnant, nb):
            self.gagnant = gagnant
            self.nb = nb

    class Carte:
        def __init__(self, attack, life):
            self.attack = attack
            self.life = life

    deck1 = len(gamer1.deck)-1
    deck2 = len(gamer2.deck)-1
    round = Round("Nobody", 1)
    carte_p1 = Carte(gamer1.deck[deck1].card_ptattaque, gamer1.deck[deck1].card_ptvie)
    carte_p2 = Carte(gamer2.deck[deck2].card_ptattaque, gamer2.deck[deck2].card_ptvie)
    while deck1 > 0 and deck2 > 0:
        print(round.nb)
        if round.nb > 1 and round.gagnant != "Nobody":
            if round.winner == gamer1.username:
                carte_p2 = Carte(gamer2.deck[deck2].card_ptattaque, gamer2.deck[deck2].card_ptvie)
            else:
                carte_p1 = Carte(gamer1.deck[deck1].card_ptattaque, gamer1.deck[deck1].card_ptvie)

        carte_p1.life -= carte_p2.attack
        carte_p2.life -= carte_p1.attack
        if carte_p1.life < 0:
            if carte_p2.life < 0:
                deck1 -= 1
                deck2 -= 1
                print("Nobody win")
            else:
                gamer2.win += 1
                deck1 -= 1
                round.gagnant = gamer2.user.username
                print("The winner is", gamer2.user.username)
        else:
            if carte_p2.life < 0:
                gamer1.win += 1
                deck2 -= 1
                round.gagnant = gamer1.user.username
                print("The winner is", gamer1.user.username)
            else:
                print("No winner wet")
        round.nb += 1
        print("_______________________")
    print("gamer 1 : ", gamer1.win)
    print("gamer 2 : ", gamer2.win)

    if gamer1.win > gamer2.win:
        print("The winner of the game is", gamer1.user.username, "!!!!!!")
    elif gamer1.win < gamer2.win:
        print("The winner of the game is", gamer2.user.username, "!!!!!!")
    else:
        print("Nobody win the game -_-")