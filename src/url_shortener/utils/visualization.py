import io
from datetime import datetime, timedelta
from typing import List, Dict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class AnalyticsVisualizer:
    """Класс для визуализации аналитических данных"""
    
    @staticmethod
    def create_clicks_plot(
        clicks_data: Dict[str, int],
        title: str = "Статистика кликов"
    ) -> io.BytesIO:
        """
        Создает график статистики кликов
        
        Args:
            clicks_data: Данные для визуализации {страна: количество}
            title: Заголовок графика
            
        Returns:
            BytesIO: Байтовый поток с изображением
        """
        # Сортируем данные по количеству кликов
        sorted_data = dict(sorted(
            clicks_data.items(), 
            key=lambda item: item[1], 
            reverse=True
        ))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(sorted_data.keys(), sorted_data.values())
        ax.set_title(title)
        ax.set_xlabel("Страна")
        ax.set_ylabel("Количество кликов")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Сохраняем в байтовый поток
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plt.close(fig)
        return buf

    @staticmethod
    def create_timeline_plot(
        timeline_data: Dict[datetime, int],
        title: str = "Клики по времени"
    ) -> io.BytesIO:
        """
        Создает график кликов по времени
        
        Args:
            timeline_data: Данные по времени {время: количество}
            title: Заголовок графика
            
        Returns:
            BytesIO: Байтовый поток с изображением
        """
        times = sorted(timeline_data.keys())
        counts = [timeline_data[t] for t in times]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(times, counts, marker='o')
        ax.set_title(title)
        ax.set_xlabel("Время")
        ax.set_ylabel("Количество кликов")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plt.close(fig)
        return buf
