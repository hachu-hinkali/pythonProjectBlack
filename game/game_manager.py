import pygame
from game.deck import Deck
from game.player import Player, Dealer


class GameManager:
    """Менеджер игровой логики Блек Джека"""

    def __init__(self, config, renderer):
        """
        config: объект ConfigLoader
        renderer: объект Renderer
        """
        self.config = config
        self.renderer = renderer

        # Создаем колоду и игроков
        num_decks = config.get('difficulty', 'medium', 'decks')
        self.deck = Deck(config, num_decks)
        self.deck.shuffle()

        self.player = Player("Player", config)
        self.dealer = Dealer(config)

        # Состояния игры
        self.game_state = "betting"  # betting, playing, dealer_turn, game_over
        self.result_message = ""
        self.win_amount = 0

        # Параметры игры
        self.min_bet = config.get('game', 'min_bet')
        self.max_bet = config.get('game', 'max_bet')
        self.blackjack_payout = config.get('game', 'blackjack_payout')

    def start_new_round(self):
        """Начало нового раунда"""
        # Проверяем, может ли игрок продолжать
        if not self.player.can_play():
            self.game_state = "game_over"
            self.result_message = "Game Over - No money left!"
            return

        # Сбрасываем руки
        self.player.reset_hand()
        self.dealer.reset_hand()

        self.game_state = "betting"
        self.result_message = ""
        self.win_amount = 0

    def place_bet(self, amount):
        """Делает ставку и раздает карты"""
        if self.game_state != "betting":
            return False

        # Игрок делает ставку
        actual_bet = self.player.place_bet(amount)

        # Раздаем карты (по 2 каждому)
        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

        # Прячем первую карту дилера
        self.dealer.hide_first_card()

        # Проверяем блекджек у игрока
        if self.player.has_blackjack:
            self.dealer.reveal_cards()
            if self.dealer.has_blackjack:
                self.end_round("push")
            else:
                self.end_round("blackjack")
        else:
            self.game_state = "playing"

        return True

    def player_hit(self):
        """Игрок берет карту"""
        if self.game_state != "playing":
            return

        self.player.add_card(self.deck.deal_card())

        # Проверяем перебор
        if self.player.is_busted:
            self.end_round("bust")

    def player_stand(self):
        """Игрок останавливается"""
        if self.game_state != "playing":
            return

        self.player.is_standing = True
        self.game_state = "dealer_turn"
        self.dealer.reveal_cards()

        # Дилер берет карты по правилам
        self.dealer_play()

    def dealer_play(self):
        """Дилер играет по правилам (берет до 17+)"""
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal_card())
            pygame.time.wait(500)  # Задержка для анимации

        # Определяем победителя
        self.determine_winner()

    def determine_winner(self):
        """Определяет победителя и заканчивает раунд"""
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()

        if self.dealer.is_busted:
            self.end_round("win")
        elif dealer_value > player_value:
            self.end_round("lose")
        elif dealer_value < player_value:
            self.end_round("win")
        else:
            self.end_round("push")

    def end_round(self, result):
        """
        Завершает раунд и начисляет выигрыш
        result: 'win', 'lose', 'push', 'blackjack', 'bust'
        """
        self.game_state = "round_over"

        if result == "blackjack":
            self.win_amount = self.player.win(self.blackjack_payout)
            self.result_message = "BLACKJACK!"
            self.config.update_stats('blackjacks')
            self.config.update_stats('wins')

        elif result == "win":
            self.win_amount = self.player.win(1.0)
            self.result_message = "YOU WIN!"
            self.config.update_stats('wins')

        elif result == "lose" or result == "bust":
            self.result_message = "YOU LOSE!" if result == "lose" else "BUST!"
            self.win_amount = 0
            self.config.update_stats('losses')

        elif result == "push":
            self.player.push()
            self.result_message = "PUSH - Tie!"
            self.win_amount = 0

        # Обновляем статистику
        self.config.update_stats('total_games')

        # Обновляем максимальный баланс
        if self.player.balance > self.config.get('stats', 'highest_balance'):
            self.config.set('stats', 'highest_balance', value=self.player.balance)
            self.config.save_config()

    def draw(self):
        """Отрисовка всей игры"""
        self.renderer.draw_background()

        self.renderer.draw_deck_info(self.deck.cards_remaining())

        # Дилер (сверху)
        self.renderer.draw_dealer_label(50, 50)
        dealer_value = self.dealer.get_visible_value() if self.game_state == "playing" else self.dealer.get_hand_value()
        show_dealer_value = self.game_state != "playing" or len([c for c in self.dealer.hand if c.face_up]) > 1
        self.renderer.draw_hand(self.dealer.hand, 250, 50, show_dealer_value, dealer_value)

        # Игрок (снизу)
        self.renderer.draw_player_label(50, 450)
        self.renderer.draw_hand(self.player.hand, 250, 450, True, self.player.get_hand_value())

        # Информация об игроке
        self.renderer.draw_player_info(self.player, 50, 550)

        # Сообщения о результате
        if self.game_state == "round_over":
            self.renderer.draw_game_result(self.result_message, self.win_amount)

        # Если игра окончена
        if self.game_state == "game_over":
            self.renderer.draw_message(self.result_message, (255, 0, 0))

    def get_state(self):
        """Возвращает текущее состояние игры"""
        return self.game_state

    def can_hit(self):
        """Может ли игрок взять карту"""
        return self.game_state == "playing" and not self.player.is_busted

    def can_stand(self):
        """Может ли игрок остановиться"""
        return self.game_state == "playing"

    def can_bet(self):
        """Может ли игрок сделать ставку"""
        return self.game_state == "betting" and self.player.can_play()

    def get_stats(self):
        """Возвращает статистику игрока"""
        return {
            'balance': self.player.balance,
            'total_games': self.config.get('stats', 'total_games'),
            'wins': self.config.get('stats', 'wins'),
            'losses': self.config.get('stats', 'losses'),
            'blackjacks': self.config.get('stats', 'blackjacks'),
            'highest_balance': self.config.get('stats', 'highest_balance')
        }
