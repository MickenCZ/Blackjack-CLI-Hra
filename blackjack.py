import random
class Dealer:
  def __init__(self):
    self.deck = [
      '♥A', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
      '♦A', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K',
      '♣A', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
      '♠A', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K'
    ]
    self.players: list[Player] = []

  def shuffle(self):
    result = []
    while len(self.deck) != 0:
        result.append(self.deck.pop(random.randint(0, len(self.deck) - 1)))
        #Pops a random item off the list and appends it to the result until length is 0.
    self.deck = result

  def deal(self, n):
    result = []
    for i in range(n):
        if (len(self.deck) != 0):
          result.append(self.deck.pop(0))
    if (len(result) == 1):
       return result[0]#Dealujeme vždy jen jednu kartu, list bude mít jen 1 element
    return result

  def addPlayer(self, player):
    self.players.append(player)

  def removePlayer(self, player):
    self.players.remove(player)

  def startRound(self):
    for player in self.players:
        player.acceptCard(self.deal(1))
    #Rozdá všem hráčům po jedné kartě

    while True:
        wantsCardsCount = 0
        for player in self.players:
            if player.needsCard():
                wantsCardsCount += 1
                player.acceptCard(self.deal(1))
        if (wantsCardsCount == 0):
           self.announceWinner()
           return


  def announceWinner(self):
    for player in self.players:
        playerValue = player.getHandValue()
        if (playerValue <= 21):
          player.handValue = playerValue
        else:
          player.handValue = 0
    #Get players with handvalues assigned
    result = bubbleSort(self.players)
    result.reverse()
    print("Vyhrává " + result[0].name + "!")
    for player in result:
       print("Hráč " + player.name + " získal " + str(player.handValue) + " bodů!")

    

class Player:
  def __init__(self, name, strategy):
    self.name = name
    self.strategy = strategy
    self.hand = []
    self.handValue = None

  def getHandValue(self):
    result = 0
    for card in self.hand:
        if (card[1] in ["J", "Q", "K"]):
          result += 1
        elif (card[1] in ["A"]):
          result += 11
        elif (card[1] in ["7", "8", "9"]):
          result += int(card[1])
        elif (card[1] in ["1"]): #Je to 10
          result += 10
    return result

  def acceptCard(self, cards):
    self.hand.append(cards)

  def needsCard(self):
    if (self.strategy == "Cautious"):
      return (self.getHandValue() <= 10)
    elif (self.strategy == "Bold"):
      return (self.getHandValue() <= 15)
    elif (self.strategy == "Human"):
      print(self.hand)
      inp = input("Toto jsou vaše karty, chcete další?(A/N)?: ")
      return inp == "A"

def bubbleSort(lst: list[Player]):
    while True:
        switched = False
        for i in range(1, len(lst)):
            if lst[i-1].handValue > lst[i].handValue:
                lst[i-1], lst[i] = lst[i], lst[i-1]
                switched = True
        if switched == False:
            return lst

# TEST DEAL

'''
dealer = Dealer()
dealer.shuffle()

myHand = dealer.deal(5)
print(myHand)
dealer.shuffle()
myHand = dealer.deal(3)
print(myHand)
'''
# TEST GAME

newDealer = Dealer()
player1 = Player('Čeněk Člověčí', 'Human')
player2 = Player('Vilda Vopatrný', 'Cautious')
player3 = Player('Olda Odvážný','Bold')
newDealer.addPlayer(player1)
newDealer.addPlayer(player2)
newDealer.addPlayer(player3)
newDealer.shuffle()
newDealer.startRound()