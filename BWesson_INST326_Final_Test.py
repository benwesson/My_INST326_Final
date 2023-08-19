from BWesson_INST326_Final import *
import pytest
import random
import pandas as pd

#Test classes to make sure they are returning correct values
def test_Deck():
    d = Deck()
    d.__init__()
    d.shuffle()
    x = d.draw()
    y = d.draw()
    #Make sure a list is being returned
    assert type(x) is list
    #Make sure when called again it produces a different card
    assert x != y

def test_Card():
    myValue = random.randint(2,14)
    suitNum = random.randint(1,4)
    if suitNum == 1:
        suit = "Hearts"
    elif suitNum == 2:
        suit = "Clubs"
        
    elif suitNum == 3:
        suit = "Spades"
    else:
        suit = "Diamonds"

    c =  Card(myValue,suit)
    c.__init__(myValue,suit) 
    c.highCard()
    x = c.finalCard()
    #High cards should now have names
    assert x != 11
    assert x != 12
    assert x != 13
    assert x != 14

def test_Player():
        myNum1 = random.randint(2,10)
        myNum2 = random.randint(2,11)

        myNum = myNum1 + myNum2
        myList = [myNum1,myNum2]

        p = Player(myNum,myList)
        p.__init__(myNum,myList)
        x = p.action()
        assert type(x) is tuple

def test_Dealer():
    dealerChoice = random.randint(1,3)
    myNum1 = random.randint(2,10)
    myNum2 = random.randint(2,11)

    dealerNum = myNum1 + myNum2
    dealerList = [myNum1,myNum2]

    de = Dealer(dealerNum,dealerList,dealerChoice)
    de.__init__(dealerNum,dealerList,dealerChoice)
    x = de.action()
    assert type(x) is tuple
    assert type(x[0]) is pd.DataFrame
    




test_Deck()
test_Card()
test_Player()





