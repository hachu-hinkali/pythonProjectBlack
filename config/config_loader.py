import json
import os


class ConfigLoader:
    """Загрузчик конфигурации игры из JSON файла"""

    def __init__(self, config_file='game_config.json'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(current_dir, config_file)
        self.config = self._load_config()

    def _load_config(self):
        """Загружает настройки из JSON"""
        with open(self.config_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_config(self):
        """Сохраняет настройки в JSON"""
        with open(self.config_path, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, indent=2, ensure_ascii=False)

    def get(self, *keys, default=None):
        """
        Получает значение из конфига
        Пример: config.get('game', 'fps') вернет 60
        """
        result = self.config
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return default
        return result

    def set(self, *keys, value):
        """
        Устанавливает значение в конфиге
        Пример: config.set('stats', 'wins', value=10)
        """
        result = self.config
        for key in keys[:-1]:
            if key not in result:
                result[key] = {}
            result = result[key]
        result[keys[-1]] = value

    def update_stats(self, stat_name, increment=1):
        """Обновляет статистику игрока"""
        current_value = self.get('stats', stat_name, default=0)
        self.set('stats', stat_name, value=current_value + increment)
        self.save_config()
