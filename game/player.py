import pygame


class Player:
    """Класс игрока"""

    def __init__(self, name, config, balance=None):
        """
        name: имя игрока
        config: объект ConfigLoader
        balance: начальный баланс (если None - берется из конфига)
        """
        self.name = name
        self.config = config
        self.balance = balance if balance else config.get('game', 'starting_balance')
        self.hand = []  # Карты на руках
        self.bet = 0  # Текущая ставка
        self.is_busted = False  # Перебор (больше 21)
        self.has_blackjack = False  # Блек Джек (21 с 2 карт)
        self.is_standing = False  # Игрок остановился

    def add_card(self, card):
        """Добавляет карту в руку"""
        self.hand.append(card)
        self._check_hand()

    def _check_hand(self):
        """Проверяет состояние руки (блекджек, перебор)"""
        total = self.get_hand_value()

        # Проверка на блекджек (21 с двух карт)
        if len(self.hand) == 2 and total == 21:
            self.has_blackjack = True

        # Проверка на перебор
        if total > 21:
            self.is_busted = True

    def get_hand_value(self):
        """Возвращает сумму значений карт в руке"""
        total = 0
        aces = 0

        # Считаем сумму и количество тузов
        for card in self.hand:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.value

        # Если перебор и есть тузы - считаем их за 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def place_bet(self, amount):
        """Делает ставку"""
        min_bet = self.config.get('game', 'min_bet')
        max_bet = self.config.get('game', 'max_bet')

        if amount < min_bet:
            amount = min_bet
        if amount > max_bet:
            amount = max_bet
        if amount > self.balance:
            amount = self.balance

        self.bet = amount
        self.balance -= amount
        return amount

    def win(self, multiplier=1.0):
        """
        Выигрыш
        multiplier: множитель выигрыша (1.0 - обычный, 1.5 - блекджек)
        """
        winnings = int(self.bet * multiplier)
        self.balance += self.bet + winnings
        return winnings

    def push(self):
        """Ничья - возврат ставки"""
        self.balance += self.bet

    def reset_hand(self):
        """Сброс руки для новой игры"""
        self.hand = []
        self.bet = 0
        self.is_busted = False
        self.has_blackjack = False
        self.is_standing = False

    def can_play(self):
        """Может ли игрок продолжать играть"""
        min_bet = self.config.get('game', 'min_bet')
        return self.balance >= min_bet

    def __str__(self):
        cards_str = ', '.join([str(card) for card in self.hand])
        return f"{self.name}: [{cards_str}] = {self.get_hand_value()} | Balance: ${self.balance}"


class Dealer(Player):
    """Класс дилера (наследует от Player)"""

    def __init__(self, config):
        """Дилер не имеет баланса, только карты"""
        super().__init__("Dealer", config, balance=0)
        self.stand_value = config.get('game', 'dealer_stand_value')

    def should_hit(self):
        """
        Дилер берет карту если сумма < 17
        Возвращает True если нужно брать карту
        """
        return self.get_hand_value() < self.stand_value and not self.is_busted

    def hide_first_card(self):
        """Скрывает первую карту дилера"""
        if len(self.hand) > 0:
            self.hand[0].face_up = False

    def reveal_cards(self):
        """Открывает все карты дилера"""
        for card in self.hand:
            card.face_up = True

    def get_visible_value(self):
        """Возвращает сумму только открытых карт"""
        total = 0
        aces = 0

        for card in self.hand:
            if card.face_up:
                if card.rank == 'A':
                    aces += 1
                    total += 11
                else:
                    total += card.value

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total
