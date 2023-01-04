#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import sys

values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
suits = ["Hearts","Diamonds","Spades","Clubs"]
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')


# In[2]:


class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + " of " + self.suit


# In[3]:


class Deck:
    
    def __init__(self):
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
    
    def shuffle(self):
        
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        
        return self.all_cards.pop()


# In[4]:


class Chips:
    
    def __init__(self,stack):
        self.stack = stack
        
    def wager(self,bet):
        self.bet = bet
        self.stack -= bet
    
    def win_bet(self,win):
        self.win = win
        self.stack += win*2
        
    def lose_bet(self,lose):
        self.lose = lose
        self.stack -= self.bet   
        
    def __str__(self):
        return self.player_name +" has "+ str(self.stack) + " chips remaining"
    
    
class Player:
    
    def __init__(self, name, hand=list):
        self.name = name
        self.hand = hand
        
    def count(self):
        self.current = 0
        for x in range(0,len(self.hand)):
            self.current += values[str(self.hand[x]).split()[0]]
            
        for x in range(0,len(self.tracker().split()),3):
            if str(self.tracker()).split()[x] == 'Ace' and self.current>21:
                return self.current-10
        else:
            return self.current

            
          
    def tracker(self):
        self.total=[]
        self.add = ""
        for x in range(0,len(self.hand)):
            self.total.append(str(Card(str(self.hand[x]).split()[2],str(self.hand[x]).split()[0])))
                              
        for i in range(0,len(self.total)):
            self.add += str(self.total[i]) + "   "
        return self.add
        

                         
    def add_card(self,card):
        self.card = card
        self.hand.append(card)
                                 
       
    def __str__(self):
                         
        return f"{self.name}'s hand: "
    

class Dealer:
    
    def __init__(self, hand = list):
        self.hand = hand

    def tracker(self):
        self.total=[]
        self.add = ""
        for x in range(0,len(self.hand)):
            self.total.append(str(Card(str(self.hand[x]).split()[2],str(self.hand[x]).split()[0])))
                              
        for i in range(0,len(self.total)):
            self.add += str(self.total[i]) + "   "
        return self.add
    
    def add_card(self,card):
        self.card = card
        self.hand.append(card)
        
    
    
    def count(self):
        self.current = 0
        for x in range(0,len(self.hand)):
            self.current += values[str(self.hand[x]).split()[0]]
            
        for x in range(0,len(self.tracker().split()),3):
            if str(self.tracker()).split()[x] == 'Ace' and self.current>21:
                return self.current-10
        else:
            return self.current

    def __str__(self):

        return f"Dealer's hand: {self.hand}\nDealer's Count: {self.count()}"

    


# In[14]:


def player_view(player,dealer):
    player=player
    dealer=dealer
    print('\n\n\r')
    print(f"{player} {player.tracker()} \r")
    print(f"Current Count: {player.count()}\n\nDealer card: {dealer.hand[0]}\r")
    
def dealer_view(dealer):
    dealer = dealer
    print(f"\n\nDealer's hand: {dealer.tracker()}\nDealer's Count: {dealer.count()}")
    
            
            

class Black_jack:  
    
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        

    def dealer(self,d_cards,p_cards,wager, deck):

        self.d_cards = d_cards
        self.p_cards = p_cards
        self.wager = wager
        self.deck = deck
        dealer_view(self.d_cards)
        
        turn = False
        while turn == False:
            
            if self.d_cards.count() <=16:
                self.d_cards.add_card(self.deck.deal_one())
                dealer_view(self.d_cards)
                continue
            
            elif self.d_cards.count()>21:
                print("You Win!!")
                self.chips.win_bet(self.wager)
                turn = True

            elif self.d_cards.count() > self.p_cards.count():
                print("You Lose!!")
                turn = True

            elif self.d_cards.count() < self.p_cards.count():
                print("You Win!!")
                self.chips.win_bet(self.wager)
                turn = True
            
            elif self.d_cards.count() == self.p_cards.count():
                print("Push! You Tied!")
                self.chips.win_bet(self.wager/2)
                turn = True


        if self.chips.stack != 0:

            print(f"You now have {self.chips.stack} chips")

            rematch = False
            while rematch == False:
                y_n = input("Would you like to play another hand? ")
                if y_n == 'yes' or y_n=='no':
                    rematch = True
                else:
                    print("Must choose 'yes' or 'no'")
                    continue
            if y_n == 'yes':
                self.game_setup()

            else:
                print ("PUSSY!")
                return None 

            hit_pass = True
        else:
            print(f"You're out of chips, go to the ATM!")
            hit_pass = True
        
    def game_setup(self):


    #Instantiating dek
        new_deck = Deck()
        new_deck.shuffle()

    #Taking a bet   
        bet = False
        while bet == False:

            try:
                wager = int(input("How many chips would you like to wager on this hand? "))
                if wager > self.chips.stack:
                    print("You do not have that many chips")
                    continue
                else:
                    bet = True
            except:
                print("wager must be an integer")

        self.chips.wager(wager)

    #deals two cards to player and dealer
        player_cards = Player(self.name, [new_deck.deal_one(),new_deck.deal_one()])
        dealer_cards = Dealer([new_deck.deal_one(),new_deck.deal_one()])

    #Shows Player their hand
        player_view(player_cards,dealer_cards)


    #asks for hit or pass
        hit_pass=False
        while hit_pass == False:
            hit = input("Would you like to hit or pass? \r")
            if hit == "hit":
                player_cards.add_card(new_deck.deal_one())
                sys.stdout.flush()
    #If hit, deals a card and show them their hand again
                player_view(player_cards,dealer_cards)
    #Checks for 21
                if player_cards.count() == 21:
                    self.chips.win_bet(wager)
                    print("21!! You win!")
                    print(f"You now have {self.chips.stack}")
                    hit_pass = True

    #Checks for bust
                elif player_cards.count() >= 21:
                    print("Bust!! You lose!")
                    if self.chips.stack != 0:

                        print(f"You now have {self.chips.stack} chips")

                        rematch = False
                        while rematch == False:
                            y_n = input("Would you like to play another hand? ")
                            if y_n == 'yes' or y_n=='no':
                                rematch = True
                            else:
                                print("Must choose 'yes' or 'no'")
                                continue
                        if y_n == 'yes':
                            self.game_setup()

                        else:
                            print ("PUSSY!")
                            return None 

                        hit_pass = True
                    else:
                        print(f"You're out of chips, go to the ATM!")
                        hit_pass = True

                else:
                    continue


            elif hit == "pass":
                print(f"Your count is {str(player_cards.count())}...Dealers turn!")
                hit_pass = True
                
                self.dealer(dealer_cards,player_cards, wager, new_deck)

            else:
                print("You must choose 'hit' or 'pass'.")
                continue



def start_black_jack():
    player_name  = input("Welcome to Black Jack! What is your name? ")
    chips = False
    while chips == False:
        try:
            stack = int(input("How many chips do you want? (1 chip = 1 cent) "))
            chips = True

        except:
            print("Chip amount must be an integer")
            continue
    total_chips = Chips(stack)
    
    play = Black_jack(player_name, total_chips)
    play.game_setup()
        


# In[15]:


start_black_jack()




