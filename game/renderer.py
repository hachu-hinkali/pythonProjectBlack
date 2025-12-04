import pygame


class Renderer:
    """Класс для отрисовки всех игровых элементов"""

    def __init__(self, screen, config):
        """
        screen: объект pygame.display
        config: объект ConfigLoader
        """
        self.screen = screen
        self.config = config
        self.width = config.get('game', 'screen_width')
        self.height = config.get('game', 'screen_height')

        # Цвета из конфига
        self.bg_color = config.get('colors', 'background')
        self.text_white = config.get('colors', 'text_white')
        self.text_black = config.get('colors', 'text_black')
        self.text_gold = config.get('colors', 'text_gold')
        self.card_bg = config.get('colors', 'card_background')
        self.card_border = config.get('colors', 'card_border')

        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)

        # Размеры карты
        self.card_width = 80
        self.card_height = 120
        self.card_spacing = 20

    def draw_background(self):
        """Отрисовка фона игрового стола"""
        self.screen.fill(self.bg_color)

        # Рисуем овал стола
        table_rect = pygame.Rect(100, 150, self.width - 200, self.height - 300)
        pygame.draw.ellipse(self.screen, (0, 100, 0), table_rect)
        pygame.draw.ellipse(self.screen, self.config.get('colors', 'table_border'), table_rect, 5)

    def draw_card(self, card, x, y):
        """
        Отрисовка одной карты
        card: объект Card
        x, y: координаты левого верхнего угла
        """
        # Прямоугольник карты
        card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

        if card.face_up:
            # Открытая карта - белый фон
            pygame.draw.rect(self.screen, self.card_bg, card_rect)
            pygame.draw.rect(self.screen, self.card_border, card_rect, 2)

            # Ранг карты (A, K, Q, J или число)
            rank_text = self.font_medium.render(card.rank, True, card.color)
            self.screen.blit(rank_text, (x + 10, y + 10))

            # Масть карты (♥, ♦, ♣, ♠)
            suit_text = self.font_large.render(card.suit_symbol, True, card.color)
            suit_rect = suit_text.get_rect(center=(x + self.card_width // 2, y + self.card_height // 2))
            self.screen.blit(suit_text, suit_rect)

            # Ранг в правом нижнем углу (перевернутый)
            rank_text_bottom = self.font_medium.render(card.rank, True, card.color)
            self.screen.blit(rank_text_bottom, (x + self.card_width - 30, y + self.card_height - 40))
        else:
            # Закрытая карта - синий паттерн
            pygame.draw.rect(self.screen, (0, 0, 150), card_rect)
            pygame.draw.rect(self.screen, self.card_border, card_rect, 2)

            # Рисуем паттерн на рубашке
            for i in range(5):
                for j in range(7):
                    pygame.draw.circle(self.screen, (0, 0, 200),
                                       (x + 15 + i * 15, y + 15 + j * 15), 3)

    def draw_hand(self, hand, x, y, show_value=True, value=0):
        """
        Отрисовка руки карт
        hand: список карт
        x, y: начальная позиция
        show_value: показывать ли сумму
        value: значение руки
        """
        # Рисуем карты с отступом
        for i, card in enumerate(hand):
            card_x = x + i * (self.card_width + self.card_spacing)
            self.draw_card(card, card_x, y)

        # Показываем сумму карт
        if show_value and len(hand) > 0:
            value_text = self.font_medium.render(f"Value: {value}", True, self.text_white)
            value_x = x + len(hand) * (self.card_width + self.card_spacing) + 20
            self.screen.blit(value_text, (value_x, y + 50))

    def draw_text(self, text, x, y, font='medium', color=None):
        """
        Отрисовка текста
        text: строка текста
        x, y: координаты
        font: размер шрифта ('small', 'medium', 'large')
        color: цвет текста (если None - белый)
        """
        if color is None:
            color = self.text_white

        if font == 'large':
            text_surface = self.font_large.render(text, True, color)
        elif font == 'small':
            text_surface = self.font_small.render(text, True, color)
        else:
            text_surface = self.font_medium.render(text, True, color)

        self.screen.blit(text_surface, (x, y))

    def draw_text_centered(self, text, y, font='medium', color=None):
        """Отрисовка текста по центру экрана"""
        if color is None:
            color = self.text_white

        if font == 'large':
            text_surface = self.font_large.render(text, True, color)
        elif font == 'small':
            text_surface = self.font_small.render(text, True, color)
        else:
            text_surface = self.font_medium.render(text, True, color)

        text_rect = text_surface.get_rect(center=(self.width // 2, y))
        self.screen.blit(text_surface, text_rect)

    def draw_player_info(self, player, x, y):
        """
        Отрисовка информации об игроке
        player: объект Player
        x, y: координаты
        """
        # Баланс
        balance_text = f"Balance: ${player.balance}"
        self.draw_text(balance_text, x, y, 'medium', self.text_gold)

        # Ставка
        if player.bet > 0:
            bet_text = f"Bet: ${player.bet}"
            self.draw_text(bet_text, x, y + 35, 'medium', self.text_white)

    def draw_dealer_label(self, x, y):
        """Отрисовка надписи 'Dealer'"""
        self.draw_text("DEALER", x, y, 'medium', self.text_gold)

    def draw_player_label(self, x, y):
        """Отрисовка надписи 'Player'"""
        self.draw_text("PLAYER", x, y, 'medium', self.text_gold)

    def draw_message(self, message, color=None):
        """Отрисовка сообщения в центре экрана"""
        if color is None:
            color = self.text_gold

        self.draw_text_centered(message, self.height // 2, 'large', color)

    def draw_game_result(self, result_text, win_amount=0):
        """
        Отрисовка результата игры
        result_text: текст результата ('WIN', 'LOSE', 'PUSH', 'BLACKJACK')
        win_amount: сумма выигрыша
        """
        # Цвет в зависимости от результата
        if 'WIN' in result_text or 'BLACKJACK' in result_text:
            color = (0, 255, 0)
        elif 'LOSE' in result_text:
            color = (255, 0, 0)
        else:
            color = self.text_gold

        self.draw_text_centered(result_text, self.height // 2 - 50, 'large', color)

        if win_amount > 0:
            win_text = f"+${win_amount}"
            self.draw_text_centered(win_text, self.height // 2 + 10, 'large', (0, 255, 0))

    def draw_deck_info(self, cards_remaining):
        """Отрисовка информации о колоде"""
        # Фон для индикатора (правый верхний угол)
        info_rect = pygame.Rect(820, 20, 160, 80)
        pygame.draw.rect(self.screen, (20, 20, 20), info_rect)
        pygame.draw.rect(self.screen, self.text_gold, info_rect, 3)

        # Заголовок "DECK"
        self.draw_text("DECK", 850, 30, 'small', self.text_gold)

        # Количество карт
        cards_text = f"{cards_remaining} cards"
        self.draw_text(cards_text, 835, 60, 'small', self.text_white)
