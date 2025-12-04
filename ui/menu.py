import pygame
from ui.button import Button


class Menu:
    """Класс меню игры"""

    def __init__(self, screen, config, renderer):
        """
        screen: объект pygame.display
        config: объект ConfigLoader
        renderer: объект Renderer
        """
        self.screen = screen
        self.config = config
        self.renderer = renderer

        self.width = config.get('game', 'screen_width')
        self.height = config.get('game', 'screen_height')

        # Текущий экран меню
        self.current_screen = "main"  # main, settings, stats

        # Создаем кнопки для главного меню
        self._create_main_menu_buttons()
        self._create_settings_buttons()
        self._create_stats_buttons()

    def _create_main_menu_buttons(self):
        """Создает кнопки главного меню"""
        center_x = self.width // 2 - 100
        start_y = 250
        button_spacing = 80

        self.main_buttons = [
            Button(center_x, start_y, 200, 60, "PLAY", self.config),
            Button(center_x, start_y + button_spacing, 200, 60, "SETTINGS", self.config),
            Button(center_x, start_y + button_spacing * 2, 200, 60, "STATS", self.config),
            Button(center_x, start_y + button_spacing * 3, 200, 60, "EXIT", self.config)
        ]

    def _create_settings_buttons(self):
        """Создает кнопки меню настроек"""
        center_x = self.width // 2 - 100
        start_y = 350
        button_spacing = 80

        self.settings_buttons = [
            Button(center_x, start_y, 200, 60, "EASY", self.config),
            Button(center_x, start_y + button_spacing, 200, 60, "MEDIUM", self.config),
            Button(center_x, start_y + button_spacing * 2, 200, 60, "HARD", self.config),
            Button(center_x, start_y + button_spacing * 3, 200, 60, "BACK", self.config)
        ]

    def _create_stats_buttons(self):
        """Создает кнопки меню статистики"""
        center_x = self.width // 2 - 100

        self.stats_buttons = [
            Button(center_x, 550, 200, 60, "BACK", self.config)
        ]

    def draw_main_menu(self):
        """Отрисовка главного меню"""
        self.renderer.draw_background()

        # Заголовок
        title = self.config.get('game', 'title')
        self.renderer.draw_text_centered(title, 100, 'large', self.renderer.text_gold)

        # Кнопки
        for button in self.main_buttons:
            button.draw(self.screen)

    def draw_settings_menu(self):
        """Отрисовка меню настроек"""
        self.renderer.draw_background()

        # Заголовок
        self.renderer.draw_text_centered("DIFFICULTY", 100, 'large', self.renderer.text_gold)

        # Описание уровней сложности
        self.renderer.draw_text_centered("Easy: 1 deck, $1500 start", 200, 'small')
        self.renderer.draw_text_centered("Medium: 4 decks, $1000 start", 250, 'small')
        self.renderer.draw_text_centered("Hard: 6 decks, $500 start", 300, 'small')

        # Кнопки
        for button in self.settings_buttons:
            button.draw(self.screen)

    def draw_stats_menu(self):
        """Отрисовка меню статистики"""
        self.renderer.draw_background()

        # Заголовок
        self.renderer.draw_text_centered("STATISTICS", 100, 'large', self.renderer.text_gold)

        # Получаем статистику
        stats = self.config.get('stats')

        # Отображаем статистику
        y_pos = 200
        line_spacing = 50

        self.renderer.draw_text_centered(f"Total Games: {stats['total_games']}", y_pos, 'medium')
        self.renderer.draw_text_centered(f"Wins: {stats['wins']}", y_pos + line_spacing, 'medium', (0, 255, 0))
        self.renderer.draw_text_centered(f"Losses: {stats['losses']}", y_pos + line_spacing * 2, 'medium', (255, 0, 0))
        self.renderer.draw_text_centered(f"Blackjacks: {stats['blackjacks']}", y_pos + line_spacing * 3, 'medium',
                                         self.renderer.text_gold)
        self.renderer.draw_text_centered(f"Highest Balance: ${stats['highest_balance']}", y_pos + line_spacing * 4,
                                         'medium', self.renderer.text_gold)

        # Процент побед
        if stats['total_games'] > 0:
            win_rate = (stats['wins'] / stats['total_games']) * 100
            self.renderer.draw_text_centered(f"Win Rate: {win_rate:.1f}%", y_pos + line_spacing * 5, 'medium')

        # Кнопки
        for button in self.stats_buttons:
            button.draw(self.screen)

    def draw(self):
        """Отрисовка текущего экрана меню"""
        if self.current_screen == "main":
            self.draw_main_menu()
        elif self.current_screen == "settings":
            self.draw_settings_menu()
        elif self.current_screen == "stats":
            self.draw_stats_menu()

    def handle_event(self, event):
        """
        Обработка событий меню
        Возвращает действие: 'play', 'exit', None
        """
        if self.current_screen == "main":
            return self._handle_main_menu_event(event)
        elif self.current_screen == "settings":
            return self._handle_settings_event(event)
        elif self.current_screen == "stats":
            return self._handle_stats_event(event)

        return None

    def _handle_main_menu_event(self, event):
        """Обработка событий главного меню"""
        for i, button in enumerate(self.main_buttons):
            button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and button.is_hovered():
                if i == 0:  # PLAY
                    return "play"
                elif i == 1:  # SETTINGS
                    self.current_screen = "settings"
                elif i == 2:  # STATS
                    self.current_screen = "stats"
                elif i == 3:  # EXIT
                    return "exit"

        return None

    def _handle_settings_event(self, event):
        """Обработка событий меню настроек"""
        for i, button in enumerate(self.settings_buttons):
            button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and button.is_hovered():
                if i == 0:  # EASY
                    self._set_difficulty("easy")
                elif i == 1:  # MEDIUM
                    self._set_difficulty("medium")
                elif i == 2:  # HARD
                    self._set_difficulty("hard")
                elif i == 3:  # BACK
                    self.current_screen = "main"

        return None

    def _handle_stats_event(self, event):
        """Обработка событий меню статистики"""
        for button in self.stats_buttons:
            button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and button.is_hovered():
                self.current_screen = "main"

        return None

    def _set_difficulty(self, difficulty):
        """Устанавливает уровень сложности"""
        difficulty_settings = self.config.get('difficulty', difficulty)

        # Сохраняем настройки в основной конфиг
        self.config.set('game', 'starting_balance', value=difficulty_settings['starting_balance'])
        self.config.save_config()

        # Возвращаемся в главное меню
        self.current_screen = "main"

    def reset_to_main(self):
        """Возврат в главное меню"""
        self.current_screen = "main"
