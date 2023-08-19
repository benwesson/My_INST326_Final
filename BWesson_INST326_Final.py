import random
import pandas as pd
import random
from argparse import ArgumentParser
import sys
import requests
from bs4 import BeautifulSoup 
import re
import sqlite3
#I changed my project slightly from proposal. One smart dealer no as opposed to mutiple players with fixed strats

#Classes
class Deck():
    """Deck class creates a deck, shuffles it, and then draws a card from it.  
    
    Attributes:
        self.values (int): The value of a card. For example, Jack = 11 and 3 = 3.
        self.suits (str): The suit of a card.
        self.cards (List): Used to make the deck.
        """
    def __init__(self):
        """This method intializes variables"""
        self.values = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.suits = ["Clubs","Diamonds","Hearts","Spades"]
        self.cards = []
    
    
    def shuffle(self):
        """This method creates and then shuffles a deck of cards"""
        for suit in self.suits:
            for value in self.values:
                self.cards.append((f"{value} {suit}"))
        random.shuffle(self.cards)
    
    
    def draw(self):
        """This method draws card from a shuffled deck of cards"""
        if len(self.cards) > 0:
            drawnCard = self.cards.pop(0)
            cardSplit = str(drawnCard).split(" ")   
        return cardSplit

class Card():
    """Card class assigns names to highcards currenlty represented as numbers.
    
    Attributes:
        self.name (str): The name of a card.
        self.suits (str): The suit of a card.
        self.value (int): The value of a card. For example, Jack = 11 and 3 = 3.
        """
    def __init__(self,value,suit):
        """This method intializes variables"""
        self.name = ""
        self.suit = suit
        self.value = int(value)

    def highCard(self):
        """This method assings values to names"""
        if self.value == 11:
            self.name = "Jack"
        elif self.value == 12:
            self.name = "Queen"
        elif self.value == 13:
            self.name = "King"
        elif self.value == 14:
            self.name = "Ace"
        else:
            self.name = self.value

    def finalCard(self):
        """This method returns a card"""
        return self.name 

class Player():
    def __init__(self,myNum,myList):
        """This method intializes variables"""
        self.myNum = myNum
        self.myList = myList
        
    def action(self):
        """This method calls the playerMoves function and returns data about the
        game being played"""
        playerData = playerMoves(self.myNum,self.myList)
        return playerData

class Dealer(Player):
    def __init__(self,myNum,myList,dealerChoice):
        """This method intializes variables"""
        self.dealerChoice = dealerChoice
        super().__init__(myNum,myList)

    def action(self):
        """This method calls the dealerMoves function and returns data about the
        game being played"""
        dealerData = dealerMoves(self.myNum,self.myList,self.dealerChoice)
        return dealerData
      
#Functions
def getRules():
    """getRules webscrapes the bicyclecards website for blackjack rules
    
    Parameters:
                None.

    Returns
        Nothing. The funtion prints the rules instead of returning a value"""
    link = "https://bicyclecards.com/how-to-play/blackjack/"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    myText = (soup.get_text())

    filename = "INST326_rule_file.txt"
    with open(filename,"w") as f:
        f.writelines(myText)
        f.close

    with open(filename,"r") as f:
        for line in f:
            line = line.rstrip()
            rule1 = re.findall(r'Object of the Game(.*?)Card Values/scoring',line)
            rule2 = re.findall(r'worth 1 or 11. (.*?)BettingBefore the',line)
            rule3 = re.findall(r'pip value.Betting(.*?), in chips, in',line)
            rule4 = re.findall(r'aturals(.*?) If any player',line)
            rule5 = re.findall(r'left goes first and (.*?) Thus, a player may stand on',line)

            myRules = [rule1,rule2,rule3,rule4,rule5]
            fixedRules = []
            for rule in myRules:
                string1 = str(rule).replace("[","")
                string2 =str(string1).replace("]","")
                fixedRules.append(string2)

            print("------------------------------------------------------------------------------------------------------")
            print(fixedRules[0])
            print("------------------------------------------------------------------------------------------------------")
            print(fixedRules[1])
            print("------------------------------------------------------------------------------------------------------")
            print(fixedRules[2])
            print("------------------------------------------------------------------------------------------------------")
            print("players are dealt 2 cards")
            print("------------------------------------------------------------------------------------------------------")
            print(fixedRules[3])
            print("------------------------------------------------------------------------------------------------------")
            print("If a player is not dealt a natural then they",fixedRules[4])
            print("------------------------------------------------------------------------------------------------------")

def getCards(myNum,person):
    """getCards uses the Card class to draw cards for the game being played.
    
    Parameters:
                myNum (int): Current total value of cards in your hand.
                person (str): Who is playing.
                
    Returns
        myNum (int): Current total value of cards in your hand.
        cardData (str): The card you have
        mySuit (str): The suit of the card you have"""
    myCard = d.draw()
    myValue = int(myCard[0])
    mySuit = myCard[1]
    
    c =  Card(myValue,myCard)
    c.__init__(myValue,mySuit) 
    c.highCard()  
    cardData = c.finalCard()

    faceCards = ["Jack","Queen","King"]
    if cardData in faceCards:
        
        myNum += 10
    elif cardData == "Ace":
        
        myNum += 11
    else:
        myNum += myValue

    print(f"{person} draws {cardData} {mySuit}")
    
    return myNum, cardData, mySuit

def playerMoves(myNum,myList):
    """playerMoves is a function that helps the player either hit or stay.
    
    Parameters:
                myNum (int): Current total value of cards in your hand.
                myList (list): List of the values associated with your cards.
                
    Returns
        df1 (dataframe): A representation of the hand you played.
        myNum (int): Current total value of cards in your hand.
        """
    myCount = 2
    myRoundList = ["round1","round2"]
    while myNum < 21:
        playerChoice = input("Would you like another card?[y/n]:")
        if playerChoice == "y":
            myData = getCards(myNum,playerName)
            myNum = myData[0]
            
            myList.append(myNum)
            print(myNum)
            myCount += 1
            myRoundList.append(f"round{myCount}")
        else:
            myList.append(myNum)
            myCount += 1
            myRoundList.append(f"round{myCount}")
            break
    #Store player moves in dataframe 
    myData = {"Me": myList}
    df1 = pd.DataFrame(myData,index = [myRoundList])
    return df1,myNum

def dealerMoves(dealerNum,dealerList,dealerChoice):
    """dealerMoves is a function that helps the player either hit or stay.
    
    Parameters:
                dealerNum (int): Current total value of cards in the dealer's hand.
                dealerList (list): List of the values associated with the dealer's cards.
                
    Returns
        df2 (dataframe): A representation of the hand you played.
        dealerNum (int): Current total value of cards in the dealer's hand. .
        """
    dealerRoundList = ["round1","round2"]
    dealerCount = 2
    #If the dealer is dealt 21 they won't draw again
    while dealerNum < 21:
        #Uncomment below line for testing
        #The highest card (ace) is worth 11 so if you are at 10 after drawing you should always hit
        if dealerNum <= 10:
            myData= getCards(dealerNum,"Dealer")
            dealerNum = myData[0]
            dealerList.append(dealerNum)
            dealerCount += 1
            dealerRoundList.append(f"round{dealerCount}")
        #If the dealer has more than 10 they might hit sometimes, but mostly play it safe and hope you mess up 
        elif dealerChoice == 1 and dealerNum > 10:
            myData = getCards(dealerNum,"Dealer")
            dealerNum = myData[0]
            dealerList.append(dealerNum)
            dealerCount += 1
            dealerRoundList.append(f"round{dealerCount}")
        else:
            dealerList.append(dealerNum)
            dealerCount += 1
            dealerRoundList.append(f"round{dealerCount}")  
            break
    #Store dealer moves in dataframe 
    dealerData = {"dealer": dealerList}
    df2 = pd.DataFrame(dealerData,index = [dealerRoundList])
    return df2,dealerNum 

def findWinner(myNum,dealerNum,wins,winnings,thePot):
    """findWinner is a function that finds the winner of the hand.
    
    Parameters:
                myNum (int): Current total value of cards in your hand.
                dealerNum (int): Current total value of cards in the dealer's hand.
                wins (int): # of Hands won.
                winnings (int): How much you won from the pot.
                thePot (int): How much you stand to win.
                
    Returns
        winData (list): Contains wins and winnings.
        """
    if myNum <= 21:
        #Check if player has more or equal to dealer
        if myNum >= dealerNum:
            #If you have 21 or less and have more than/equal to dealer then you win
            print("you win")
            wins += 1
            winnings += thePot
            
        #Dealer has more
        else:
            #Dealer has 21 or less
            if dealerNum <= 21:
                print("you lose")
            #Dealer went over 21 
            else:
                print("you win")
                wins += 1
                winnings += thePot 
    else:
        print("you lose")

    winData = [wins, winnings]
    return winData

def parse_args(arglist):
    """ Parses command-line arguments.

    The following required command-line arguments are defined:

    money: How much money/chips the player is bringing to the table. The 
    player will use this pool of money to place bets. 

    Args:
        arglist (list of str): a list of command-line arguments.

    Returns:
        namespace: a namespace with variables target and strings.
    """
    parser = ArgumentParser()
    parser.add_argument("money",type = int, help = "How much money are you playing with")
    args = parser.parse_args(arglist)
    return args

def chips(money):
    """Player must enter how much money they are bringing to the table
    
    Parameters:
        money (int): How much money you are playing with.
        
    Returns
        money (int): How much money you are playing with."""
    return money

def myFile(wins,winnings):
    """When you are done playing myFile creates a file showing how much you won and how many hands you won.
    
    Parameters:
                wins (int): # of Hands won.
                winnings (int): How much you won from the pot.
                            
    Returns
        None.
        """
    filename = "INST326_final_file.txt"
    with open(filename,"w") as f:
        x = (str(wins))
        y = (str(winnings))

        line1 = f"Wins: {x}\n"
        line2 = f"Winnings: {y}\n"
        
        f.writelines([line1,line2])
      
        f.close()
    
def myDB(sqlData):
    """creates a sqllite file to display the first two cards you drew each hand. You
       could use this to find how naturals you were dealt
    
    Parameters:
                sqlData (list): A list of tuples representing card data
                            
    Returns
        None.
        """
    conn = sqlite3.connect('INST326_SQL_Data.sqlite')
    cursor = conn.cursor()

    cq = '''CREATE TABLE IF NOT EXISTS cards (card TEXT, suit TEXT) '''
    cursor.execute(cq)

    imq = '''INSERT INTO cards VALUES (?,?)'''

    cursor.executemany(imq, sqlData)

    conn.commit()

    cursor.close()
     
def getData(card,suit,sqlData):
    """getData is a function that helps the player either hit or stay.
    
    Parameters:
                card (str): Name of card. 
                suit (str): Suit of card.
                sqlData (list): A list of tuples representing card data
                
    Returns
        sqlData
        """
    data = (f"{card}",f"{suit}")
    sqlData.append(data)
    
    return sqlData
    
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    money = chips(args.money)
    wins = 0
    winnings = 0
    
    playerKnowledge = input("Do you know how to play Blackjack?[type no for help, type anything to skip]: ")
    if playerKnowledge == "no":
        getRules()
    play = input("Would you like to play Blackjack?[y/n]: ")
    if play == "n":
        print("Ok, have a nice day")
            
    elif play != "y" and play != "n":
            print("ERROR")
            play = input("Would you like to play Blackjack?[y/n]: ")

    playerName = input("Enter your name: ")

    while play == "y":
        dealerNum = 0
        dealerList = []
        thePot = 0
        myNum = 0
        myList = []
        sqldata = []
        
        myBet = input("Place your bet:")

        if int(myBet) <= money:
            thePot += int(myBet)
        else:
            print("You do not have enough money")
            myBet = input("Place your bet:")
            
        print("---------------------------------------------------") 

        #Cards are dealt
        d = Deck()
        d.__init__()
        d.shuffle()

        #Card 1
        #Card for you
        myData = getCards(myNum,playerName)
        myNum = myData[0]
        myList.append(myNum)
        sqldata = getData(myData[1],myData[2],sqldata)
        #Card 2
        #Card for you 
        myData = getCards(myNum,playerName)
        myNum = myData[0]
        sqldata = getData(myData[1],myData[2],sqldata)
    
        myList.append(myNum)
        print("Total Value: ",myNum)
        
        #Card 1
        #Card for Dealer
        myData = getCards(dealerNum,"Dealer")
        dealerNum = myData[0]
        sqldata = getData(myData[1],myData[2],sqldata)
        dealerList.append(dealerNum)

        #Card 2
        #Card for Dealer
        myData = getCards(dealerNum,"Dealer")
        dealerNum = myData[0]
        sqldata = getData(myData[1],myData[2],sqldata)
        dealerList.append(dealerNum)

        myDB(sqldata)
        print("Total Value: ",dealerNum)
        print("---------------------------------------------------")
        
        p = Player(myNum,myList)
        p.__init__(myNum,myList)
        playerData = p.action()
        playerDF = playerData[0]
        myNum = playerData[1]
        
        dealerChoice = random.randint(1,3)
        de = Dealer(dealerNum,dealerList,dealerChoice)
        de.__init__(dealerNum,dealerList,dealerChoice)
        dealerData = de.action()
        dealerDF = dealerData[0]
        dealerNum = dealerData[1]
        
        print(playerDF)
        print(dealerDF)
        #Find winner
        winData = findWinner(myNum,dealerNum,wins,winnings,thePot)

        wins = winData[0]
        winnings = winData[1]

        play = input("Would you like to again?[y/n]: ")
        if play == "n":
            
            myFile(wins,winnings)
            print("Thanks for playing")
            break
        elif play != "y" and play != "n":
            print("ERROR")
            play = input("Would you like to play to again?[y/n]: ")

