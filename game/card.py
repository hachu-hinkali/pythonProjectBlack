class Card:
    """Класс карты с мастью и значением"""

    def __init__(self, suit, rank, config):
        """
        suit: масть карты ('hearts', 'diamonds', 'clubs', 'spades')
        rank: ранг карты ('A', '2'-'10', 'J', 'Q', 'K')
        config: объект ConfigLoader для получения настроек
        """
        self.suit = suit
        self.rank = rank
        self.config = config

        # Получаем символ масти и значение из конфига
        self.suit_symbol = config.get('card_suits', suit)
        self.value = config.get('card_values', rank)

        # Цвета для мастей (красные и черные)
        self.is_red = suit in ['hearts', 'diamonds']
        self.color = config.get('colors', 'text_black') if not self.is_red else [255, 0, 0]

        # Позиция карты на экране (устанавливается при отрисовке)
        self.x = 0
        self.y = 0
        self.face_up = True  # Видна ли карта игроку

    def get_value(self, current_total=0):
        """
        Возвращает значение карты
        Для туза возвращает 1 если сумма превышает 21, иначе 11
        """
        if self.rank == 'A' and current_total + self.value > 21:
            return 1
        return self.value

    def __str__(self):
        """Строковое представление карты"""
        return f"{self.rank}{self.suit_symbol}"

    def __repr__(self):
        return self.__str__()
