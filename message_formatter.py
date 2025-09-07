import logging
from typing import List, Dict
from datetime import datetime
from api_client import AbandonedObjectsAPI

logger = logging.getLogger(__name__)


class MessageFormatter:
    """Formatter for Telegram messages about abandoned objects"""
    
    def __init__(self):
        self.api_client = AbandonedObjectsAPI()
    
    def format_new_objects_message(self, new_objects: List[Dict]) -> str:
        """
        Format a message about new abandoned objects
        
        Args:
            new_objects: List of new abandoned objects
            
        Returns:
            Formatted message string
        """
        if not new_objects:
            return "🔍 Новых заброшенных объектов не найдено."
        
        count = len(new_objects)
        header = f"🏠 Найдено {count} нов{'ый' if count == 1 else 'ых'} заброшенн{'ый объект' if count == 1 else 'ых объекта' if count < 5 else 'ых объектов'} в Минском районе:\n\n"
        
        items = []
        for i, obj in enumerate(new_objects, 1):
            item = self._format_single_object(obj, i)
            items.append(item)
        
        # Add footer with timestamp in Minsk time (with empty line before it)
        from datetime import timezone, timedelta
        minsk_tz = timezone(timedelta(hours=3))
        minsk_time = datetime.now(minsk_tz)
        footer = f"\n\n🕐 Проверка выполнена: {minsk_time.strftime('%d.%m.%Y %H:%M')}"
        
        message = header + "\n\n".join(items) + footer
        
        # Telegram message limit is 4096 characters
        if len(message) > 4000:
            # Split into multiple messages if too long
            return self._split_long_message(new_objects)
        
        return message
    
    def _format_single_object(self, obj: Dict, index: int) -> str:
        """
        Format information about a single abandoned object
        
        Args:
            obj: Abandoned object data
            index: Item number in the list
            
        Returns:
            Formatted string for single object
        """
        object_id = obj.get('id', 'N/A')
        position = obj.get('position', 'Адрес не указан')
        
        # Generate view URL
        view_url = self.api_client.get_view_url(object_id)
        
        # Create simplified formatted item - only address and link
        item = f"{index}. 📍 {position}\n"
        item += f"🔗 [Подробнее]({view_url})"
        
        return item
    
    def _format_timestamp(self, timestamp) -> str:
        """
        Format timestamp to readable date
        
        Args:
            timestamp: Unix timestamp in milliseconds
            
        Returns:
            Formatted date string or empty string if invalid
        """
        try:
            if timestamp:
                # Convert from milliseconds to seconds
                dt = datetime.fromtimestamp(timestamp / 1000)
                return dt.strftime('%d.%m.%Y')
        except (ValueError, TypeError, OSError):
            pass
        return ""
    
    def _split_long_message(self, objects: List[Dict]) -> str:
        """
        Handle case when message is too long for Telegram
        
        Args:
            objects: List of objects
            
        Returns:
            Truncated message with indication of total count
        """
        count = len(objects)
        header = f"🏠 Найдено {count} новых заброшенных объектов в Минском районе (показаны первые 5):\n\n"
        
        items = []
        for i, obj in enumerate(objects[:5], 1):
            item = self._format_single_object(obj, i)
            items.append(item)
        
        footer = f"\n\n... и еще {count - 5} объектов\n\n"
        from datetime import timezone, timedelta
        minsk_tz = timezone(timedelta(hours=3))
        minsk_time = datetime.now(minsk_tz)
        footer += f"🕐 Проверка выполнена: {minsk_time.strftime('%d.%m.%Y %H:%M')}"
        
        return header + "\n\n".join(items) + footer
    
    def format_error_message(self, error: str) -> str:
        """
        Format error message
        
        Args:
            error: Error description
            
        Returns:
            Formatted error message
        """
        from datetime import timezone, timedelta
        minsk_tz = timezone(timedelta(hours=3))
        minsk_time = datetime.now(minsk_tz)
        timestamp = minsk_time.strftime('%d.%m.%Y %H:%M')
        return f"❌ Ошибка при проверке объектов:\n{error}\n\n🕐 {timestamp}"
    
    def format_status_message(self, objects_count: int, last_update: str = None) -> str:
        """
        Format status message
        
        Args:
            objects_count: Number of tracked objects
            last_update: Last update timestamp
            
        Returns:
            Formatted status message
        """
        message = f"📊 Статус мониторинга:\n"
        message += f"🏠 Отслеживается объектов: {objects_count}\n"
        
        if last_update:
            try:
                dt = datetime.fromisoformat(last_update)
                formatted_date = dt.strftime('%d.%m.%Y %H:%M')
                message += f"🕐 Последняя проверка: {formatted_date}\n"
            except:
                message += f"🕐 Последняя проверка: {last_update}\n"
        else:
            message += "🕐 Последняя проверка: Никогда\n"
        
        message += f"⏰ Следующая проверка через 5 минут (режим тестирования)"
        
        return message
