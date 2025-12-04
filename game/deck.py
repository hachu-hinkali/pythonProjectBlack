import random
from game.card import Card


class Deck:
    """Класс колоды карт"""

    def __init__(self, config, num_decks=1):
        """
        config: объект ConfigLoader
        num_decks: количество колод (обычно 1, 4 или 6)
        """
        self.config = config
        self.num_decks = num_decks
        self.cards = []
        self.create_deck()

    def create_deck(self):
        """Создает колоду из 52 карт * num_decks"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        self.cards = []
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    card = Card(suit, rank, self.config)
                    self.cards.append(card)

    def shuffle(self):
        """Тасует колоду"""
        random.shuffle(self.cards)

    def deal_card(self):
        """
        Выдает одну карту из колоды
        Если карт не осталось - пересоздает и тасует колоду
        """
        if len(self.cards) == 0:
            self.create_deck()
            self.shuffle()
        return self.cards.pop()

    def cards_remaining(self):
        """Возвращает количество оставшихся карт"""
        return len(self.cards)

    def __len__(self):
        return len(self.cards)
