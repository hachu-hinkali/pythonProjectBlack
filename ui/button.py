import pygame


class Button:
    """Класс кнопки для игрового интерфейса"""

    def __init__(self, x, y, width, height, text, config, action=None):
        """
        x, y: координаты кнопки
        width, height: размеры кнопки
        text: текст на кнопке
        config: объект ConfigLoader
        action: функция, вызываемая при клике
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.config = config
        self.action = action
        self.enabled = True
        self.hovered = False

        # Цвета из конфига
        self.color_normal = config.get('colors', 'button_normal')
        self.color_hover = config.get('colors', 'button_hover')
        self.color_disabled = config.get('colors', 'button_disabled')
        self.text_color = config.get('colors', 'text_white')

        # Шрифт для текста
        self.font = pygame.font.Font(None, 32)

    def draw(self, surface):
        """Отрисовка кнопки"""
        # Выбор цвета в зависимости от состояния
        if not self.enabled:
            color = self.color_disabled
        elif self.hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        # Рисуем прямоугольник кнопки
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.text_color, self.rect, 2)  # Обводка

        # Рисуем текст по центру
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Обработка событий мыши
        Возвращает True если кнопка была нажата
        """
        if not self.enabled:
            return False

        # Проверка наведения мыши
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        # Проверка клика
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True

        return False

    def set_enabled(self, enabled):
        """Включить/выключить кнопку"""
        self.enabled = enabled

    def set_text(self, text):
        """Изменить текст кнопки"""
        self.text = text

    def is_hovered(self):
        """Проверка наведения мыши"""
        if not self.enabled:
            return False
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)
