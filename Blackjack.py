#!/usr/bin/env python
# coding: utf-8

#   ## General task: allow for string or int input

# In[552]:


import random
import numpy as np


# In[617]:


class Game:
    def __init__(self, deck, player, dealer):
        self.deck = deck
        self.player = player
        self.dealer = dealer
        self.pot = 0
        
    def accept_bet(self, stake):
        self.pot += stake
        
    def request_bet(self):
        while True:
            bet = input('Choose your bet: ')
            if bet.isnumeric(): 
                if 0 < int(bet) <= self.player.stack:
                    bet = int(bet)
                    break
            print('Invalid bet. Please choose a positive integer which is less than your stack.')
        self.accept_bet(bet)
        self.player.place_bet(bet)

    def initial_deal(self):
        for i in range(2):
            self.player.give_card(deck.deal_card())  
            self.dealer.give_card(deck.deal_card())
        print('\n')
        print(player)
        print(dealer.show_first())
        print('\n')

    def player_deal(self):
        while self.player.state == 'active':
            action = ''
            while True:
                action = input('Player Action: Enter H for hit or S for stand: ')
                if (action == 'H') or (action == 'S'):
                    break
                print('Please enter a valid player action: H or S')
            
            if action == 'S':
                score = self.player.total[np.argmin([21 - x for x in self.player.total])]
                print(self.player)
                print('Player finishes with score '+ str(score) + '\n')
                self.player.total = score
                break
            elif action == 'H':
                self.player.give_card(deck.deal_card()) 
                print(self.player)
        if self.player.state == 'bust':
            print('Player went bust\n')
        elif self.player.state == '21':
            self.player.total = 21 
            print('Player scored 21\n')
                
    def dealer_deal(self):
        # Better to not deal with this in this function, BUT no dealer deal if player busts
        if self.player.state == 'bust':
            print('Dealer wins!\n')
            return 
        print(self.dealer)
        while self.dealer.state == 'active':
            self.dealer.give_card(deck.deal_card()) 
            print(self.dealer)
        print('Dealer finishes with score ' + str(max(self.dealer.total)))
        self.dealer.total = max(self.dealer.total)
        if self.dealer.state == 'bust':
            print('Dealer went bust\n')
        
    def declare_winner(self):
        if self.player.state == 'bust':
            return            
        elif (self.dealer.state == 'bust') | (self.player.total > self.dealer.total):
            print('Player wins!\n')
            self.player.receive_winnings(2 * self.pot)
        elif self.dealer.total > self.player.total:
            print('Dealer wins!\n')
        elif self.player.total == self.dealer.total:
            print('Scores tied!\n')  
            self.player.receive_winnings(self.pot)
    
    def reset_hand(self):
        self.pot = 0
        self.player.return_cards(self.deck)
        self.dealer.return_cards(self.deck)
        self.deck.build
            
                                                    
                                    
                                                    


# In[618]:


class Deck: 
    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        self.cards = []
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            for value in [str(i) for i in range(2,11)] + ['J', 'Q', 'K', 'A']:
                self.cards.append(Card(suit,value))
        random.shuffle(self.cards)
                
    def deal_card(self):
        dealt_card = self.cards[-1]
        self.cards.pop(-1)
        return dealt_card
    
    def return_cards(self, returned):
        self.cards += returned
        


# In[619]:


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return self.value + self.suit[0]


# In[621]:


# Eventually make player an extension of dealer

class Player:
    def __init__(self, stack_size):
        self.stack = stack_size
        self.cards = []
        self.total = 0 
        self.state = 'active'
        
    def __str__(self):
        total = self.total 
        valid = [val for val in total if val <= 21]
        if len(valid)>1:
            return 'Player now has ' + str([str(c) for c in self.cards]) +' for possible totals of ' + str(valid)
        elif len(valid) == 1:
            return 'Player now has ' + str([str(c) for c in self.cards]) +' for a total of ' + str(valid)
        elif len(valid) == 0:
            return 'Player now has ' + str([str(c) for c in self.cards]) +' for a total of ' + str([min(total)])
        
    def update_total(self):
        non_aces = [c for c in self.cards if c.value != 'A']
        aces = [c for c in self.cards if c.value == 'A']
        royal_map = dict(zip([str(i) for i in list(range(2,11))], [str(i) for i in list(range(2,11))])) 
        royal_map.update({'J':10, 'Q':10, 'K':10})

        total = [sum([int(royal_map[c.value]) for c in non_aces])]
            
        if aces != []:
            totals = []
            for i in range(len(aces)+1):
                totals.append(total[0] + (len(aces)-i)*1 + i*11 )
            total = totals
        min_total = min(total)   
            
        self.total = total
        self.state = self.check_state()
     
    # Same for dealer?
    def check_state(self):
        current_total = self.total
        if not isinstance(current_total, list):
            current_total = [current_total]
        
        if 21 in current_total:
            return '21'
        elif min(current_total) > 21:
            return 'bust'
        else:
            return 'active'
  
        
    def give_card(self, card):
        self.cards.append(card)
        self.update_total()       
    
    def return_cards(self, deck):
        deck.return_cards(self.cards)
        self.cards = []
        
    def place_bet(self, size):
        if self.stack >= size:
            self.stack -= size
        else:
            # Deal with this later, possibly ValueError?
            pass
    
    def receive_winnings(self, amount):
        self.stack += amount


# In[622]:


# Don't want same __str__ as player
class Dealer(Player):  
    def __init__(self):
        self.cards = []
        self.total = 0 
        self.state = 'active'
        
    def __str__(self):
        total = self.total 
        valid = [val for val in total if val <= 21]
        if len(valid)>1:
            return 'Dealer now has ' + str([str(c) for c in self.cards]) +' for possible totals of ' + str(valid)
        elif len(valid) == 1:
            return 'Dealer now has ' + str([str(c) for c in self.cards]) +' for a total of ' + str(valid)
        elif len(valid) == 0:
            return 'Dealer now has ' + str([str(c) for c in self.cards]) +' for a total of ' + str(total)
        
    def show_first(self):
        return 'Dealer now has ' + str([self.cards[0].__str__(), '*'])  

    def update_total(self):
        non_aces = [c for c in self.cards if c.value != 'A']
        aces = [c for c in self.cards if c.value == 'A']
        royal_map = dict(zip([str(i) for i in list(range(2,11))], [str(i) for i in list(range(2,11))])) 
        royal_map.update({'J':10, 'Q':10, 'K':10})

        total = [sum([int(royal_map[c.value]) for c in non_aces])]
            
        if aces != []:
            totals = []
            for i in range(len(aces)+1):
                totals.append(total[0] + (len(aces)-i)*1 + i*11 )
            total = totals
        self.total = total
        self.state = self.check_state()
        
    def check_state(self):
            current_total = self.total
            if not isinstance(current_total, list):
                current_total = [current_total]

            if 17 <= max(current_total) <= 21 :
                return 'full'
            elif min(current_total) > 21:
                return 'bust'
            else:
                return 'active'
        
        
        
        
    def give_card(self, card):
        self.cards.append(card)
        self.update_total()
        
    def return_cards(self, deck):
        deck.return_cards(self.cards)
        self.cards = []


# In[626]:


# Do all gameplay in the Game object, using methods start(), stack() etc?

start_stack = None
while True:
    start_stack = input('Enter starting stack size: ')
    if start_stack.isnumeric(): 
        if int(start_stack) > 0:
            start_stack = int(start_stack)
            break
    print('Invalid stack size. Please choose a positive integer.')

player = Player(start_stack)
deck = Deck()
dealer = Dealer()
game = Game(deck, player, dealer)

while True:
    game.request_bet()
    game.initial_deal()
    game.player_deal()
    game.dealer_deal()
    game.declare_winner()
    if game.player.stack == 0:
        print('Game over, player lost their whole stack!')
        break

    new_hand = ''
    while True:
        new_hand = input('Play another hand? (Y/N): ')
        if new_hand in ['Y', 'N']:
            break
    if new_hand == 'N':
        print('\nPlayer final stack size: ' + str(game.player.stack))
        break
    game.reset_hand()
        
    

