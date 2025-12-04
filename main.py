import pygame
import sys
from config.config_loader import ConfigLoader
from game.renderer import Renderer
from game.game_manager import GameManager
from ui.menu import Menu
from ui.button import Button


class BlackjackGame:
    """Главный класс игры Блек Джек"""

    def __init__(self):
        """Инициализация игры"""
        # Инициализация pygame
        pygame.init()

        # Загрузка конфигурации
        self.config = ConfigLoader()

        # Создание окна
        self.width = self.config.get('game', 'screen_width')
        self.height = self.config.get('game', 'screen_height')
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.config.get('game', 'title'))

        # FPS
        self.clock = pygame.time.Clock()
        self.fps = self.config.get('game', 'fps')

        # Создание компонентов
        self.renderer = Renderer(self.screen, self.config)
        self.menu = Menu(self.screen, self.config, self.renderer)
        self.game_manager = None

        # Состояние приложения
        self.app_state = "menu"  # menu, game

        # Кнопки управления игрой
        self._create_game_buttons()

        # Кнопки ставок
        self._create_bet_buttons()

    def _create_game_buttons(self):
        """Создает кнопки для игрового процесса"""
        self.hit_button = Button(300, 600, 120, 50, "HIT", self.config)
        self.stand_button = Button(450, 600, 120, 50, "STAND", self.config)
        self.new_round_button = Button(600, 600, 150, 50, "NEW ROUND", self.config)
        self.menu_button = Button(780, 600, 120, 50, "MENU", self.config)

    def _create_bet_buttons(self):
        """Создает кнопки для ставок"""
        start_x = 150
        start_y = 300
        button_width = 100
        button_spacing = 120

        bet_amounts = [10, 25, 50, 100, 500, 1000]
        self.bet_buttons = []

        for i, amount in enumerate(bet_amounts):
            x = start_x + i * button_spacing
            button = Button(x, start_y, button_width, 50, f"${amount}", self.config)
            self.bet_buttons.append(button)

    def start_game(self):
        """Запуск игры из меню"""
        self.app_state = "game"
        self.game_manager = GameManager(self.config, self.renderer)
        self.game_manager.start_new_round()

    def handle_events(self):
        """Обработка всех событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Обработка событий в зависимости от состояния
            if self.app_state == "menu":
                self._handle_menu_events(event)
            elif self.app_state == "game":
                self._handle_game_events(event)

        return True

    def _handle_menu_events(self, event):
        """Обработка событий меню"""
        action = self.menu.handle_event(event)

        if action == "play":
            self.start_game()
        elif action == "exit":
            pygame.quit()
            sys.exit()

    def _handle_game_events(self, event):
        """Обработка событий в игре"""
        game_state = self.game_manager.get_state()

        # Кнопка возврата в меню (всегда активна)
        self.menu_button.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu_button.is_hovered():
            self.app_state = "menu"
            self.menu.reset_to_main()
            return

        # Состояние: делаем ставку
        if game_state == "betting":
            self._handle_betting_events(event)

        # Состояние: игра идет
        elif game_state == "playing":
            self._handle_playing_events(event)

        # Состояние: раунд окончен
        elif game_state == "round_over":
            self._handle_round_over_events(event)

    def _handle_betting_events(self, event):
        """Обработка ставок"""
        bet_amounts = [10, 25, 50, 100, 500, 1000]

        for i, button in enumerate(self.bet_buttons):
            button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and button.is_hovered():
                # Проверяем, достаточно ли у игрока денег для этой ставки
                if self.game_manager.player.balance >= bet_amounts[i]:
                    self.game_manager.place_bet(bet_amounts[i])
                # Если денег недостаточно - кнопка просто не сработает

    def _handle_playing_events(self, event):
        """Обработка хода игрока"""
        # Кнопка HIT
        self.hit_button.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.hit_button.is_hovered():
            if self.game_manager.can_hit():
                self.game_manager.player_hit()

        # Кнопка STAND
        self.stand_button.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.stand_button.is_hovered():
            if self.game_manager.can_stand():
                self.game_manager.player_stand()

    def _handle_round_over_events(self, event):
        """Обработка конца раунда"""
        self.new_round_button.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and self.new_round_button.is_hovered():
            self.game_manager.start_new_round()

    def update(self):
        """Обновление логики игры"""
        # Пока обновлять нечего, но можно добавить анимации
        pass

    def draw(self):
        """Отрисовка всего"""
        if self.app_state == "menu":
            self.menu.draw()

        elif self.app_state == "game":
            # Отрисовываем игру
            self.game_manager.draw()

            game_state = self.game_manager.get_state()

            # Отрисовываем кнопки в зависимости от состояния
            if game_state == "betting":
                self._draw_betting_screen()

            elif game_state == "playing":
                self._draw_playing_screen()

            elif game_state == "round_over":
                self._draw_round_over_screen()

            # Кнопка меню всегда видна
            self.menu_button.draw(self.screen)

        pygame.display.flip()

    def _draw_betting_screen(self):
        """Отрисовка экрана ставок"""
        self.renderer.draw_text_centered("Place Your Bet", 250, 'large', self.renderer.text_gold)

        # Отрисовываем кнопки ставок
        bet_amounts = [10, 25, 50, 100, 500, 1000]
        player_balance = self.game_manager.player.balance

        # Активируем/деактивируем кнопки в зависимости от баланса
        for i, button in enumerate(self.bet_buttons):
            if bet_amounts[i] <= player_balance:
                button.set_enabled(True)
            else:
                button.set_enabled(False)
            button.draw(self.screen)

    def _draw_playing_screen(self):
        """Отрисовка экрана игры"""
        # Активируем кнопки
        self.hit_button.set_enabled(self.game_manager.can_hit())
        self.stand_button.set_enabled(self.game_manager.can_stand())

        # Рисуем кнопки
        self.hit_button.draw(self.screen)
        self.stand_button.draw(self.screen)

    def _draw_round_over_screen(self):
        """Отрисовка экрана конца раунда"""
        self.new_round_button.draw(self.screen)

    def run(self):
        """Главный игровой цикл"""
        running = True

        while running:
            # Обработка событий
            running = self.handle_events()

            # Обновление логики
            self.update()

            # Отрисовка
            self.draw()

            # Ограничение FPS
            self.clock.tick(self.fps)

        # Выход
        pygame.quit()
        sys.exit()


# Точка входа

game = BlackjackGame()
game.run()
