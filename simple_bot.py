#!/usr/bin/env python3
"""
ERI Bot - Simple version that works with current python-telegram-bot
"""

import asyncio
import logging
import sys
import requests
import json
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from api_client import AbandonedObjectsAPI
from data_manager import DataManager
from message_formatter import MessageFormatter

# Configure logging with automatic rotation
def setup_logging():
    """Setup logging with automatic rotation"""
    # Create rotating file handler
    # Max file size: 10MB, keep 5 backup files (about 1 month of logs)
    file_handler = RotatingFileHandler(
        'eri_bot.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set formatter for both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )
    
    return logging.getLogger(__name__)

# Setup logging
logger = setup_logging()


class SimpleEriBot:
    """Simplified ERI Bot using direct Telegram API calls"""
    
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.api_client = AbandonedObjectsAPI()
        self.data_manager = DataManager()
        self.formatter = MessageFormatter()
        self.last_update_id = 0
        self.last_command_time = 0  # Track last command time to prevent rapid duplicates
        self.last_check_time = None  # Track last check time for status
        self.last_check_result = None  # Track last check result for status
        
        if not self.token or not self.chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        
        # Remove 'bot' prefix if present
        if self.token.startswith('bot'):
            self.token = self.token[3:]
    
    async def send_message(self, text: str) -> bool:
        """Send message via Telegram Bot API"""
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            # Don't use proxy for Telegram API
            response = requests.post(url, json=data, timeout=30, proxies={})
            
            if response.status_code == 200:
                logger.info("Message sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test Telegram bot connection"""
        try:
            url = f"https://api.telegram.org/bot{self.token}/getMe"
            # Don't use proxy for Telegram API
            response = requests.get(url, timeout=10, proxies={})
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    logger.info(f"Bot connected: @{bot_info.get('username', 'unknown')}")
                    return True
                    
            logger.error(f"Bot connection failed: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"Error testing connection: {e}")
            return False
    
    async def get_updates(self):
        """Get updates from Telegram API to handle commands"""
        try:
            url = f"https://api.telegram.org/bot{self.token}/getUpdates"
            params = {
                'offset': self.last_update_id + 1,
                'timeout': 1,  # Short timeout to not block
                'allowed_updates': ['message'],
                'limit': 10  # Limit number of updates
            }
            
            # Don't use proxy for Telegram API
            response = requests.get(url, params=params, timeout=10, proxies={})
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('result'):
                    updates = data['result']
                    for update in updates:
                        new_update_id = update['update_id']
                        # Only process if this is a new update
                        if new_update_id > self.last_update_id:
                            self.last_update_id = new_update_id
                            # Only process recent messages (within last 2 minutes)
                            message = update.get('message', {})
                            message_date = message.get('date', 0)
                            current_time = datetime.now().timestamp()
                            if current_time - message_date < 120:  # 2 minutes
                                await self.handle_update(update)
                        
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
    
    async def handle_update(self, update):
        """Handle incoming Telegram update"""
        try:
            message = update.get('message', {})
            text = message.get('text', '')
            chat_id = message.get('chat', {}).get('id')
            message_date = message.get('date', 0)
            
            # Only respond to messages from our configured chat
            if str(chat_id) != str(self.chat_id):
                return
            
            # Only process commands that are newer than our last processed command
            # and not older than 30 seconds to prevent processing old commands
            current_time = datetime.now().timestamp()
            if text.startswith('/') and message_date > self.last_command_time and (current_time - message_date) < 30:
                self.last_command_time = message_date
                logger.info(f"Processing fresh command: {text.strip()} from {message_date}")
                await self.handle_command(text.strip())
            elif text.startswith('/'):
                logger.debug(f"Ignoring old/duplicate command: {text.strip()}, age: {current_time - message_date}s")
                
        except Exception as e:
            logger.error(f"Error handling update: {e}")
    
    async def handle_command(self, command):
        """Handle bot commands"""
        try:
            if command == '/start':
                welcome_message = (
                    "🚀 Добро пожаловать в ERI Bot!\n\n"
                    "🔍 Я отслеживаю появление новых заброшенных объектов в Минском районе за одну базовую "
                    "и буду уведомлять вас о каждом новом объявлении.\n\n"
                    "⏰ Проверка происходит каждый час.\n"
                    "📱 Используйте /help для просмотра всех команд.\n\n"
                    "✅ Мониторинг активен!"
                )
                await self.send_message(welcome_message)
                logger.info("Start command executed")
                
            elif command == '/status':
                if self.last_check_time:
                    time_str = self.last_check_time.strftime("%d.%m.%Y в %H:%M")
                    if self.last_check_result:
                        result_str = f"Найдено новых объектов: {self.last_check_result}"
                    else:
                        result_str = "Новых объектов не найдено"
                    
                    status_message = (
                        f"📊 Статус мониторинга ERI Bot\n\n"
                        f"🕐 Последняя проверка: {time_str}\n"
                        f"📋 Результат: {result_str}\n\n"
                        f"🔄 Интервал проверки: каждый час\n"
                        f"🎯 Регион: Минский район за одну базовую\n"
                        f"✅ Мониторинг активен"
                    )
                else:
                    status_message = (
                        f"📊 Статус мониторинга ERI Bot\n\n"
                        f"🕐 Проверки еще не выполнялись\n"
                        f"🔄 Интервал проверки: каждый час\n"
                        f"🎯 Регион: Минский район за одну базовую\n"
                        f"✅ Мониторинг активен"
                    )
                
                await self.send_message(status_message)
                logger.info("Status command executed")
                
            elif command == '/check':
                await self.send_message("🔍 Выполняю проверку новых объектов в Минском районе за одну базовую...")
                
                # Perform manual check with notification about results
                try:
                    current_objects = self.api_client.fetch_abandoned_objects()
                    
                    if current_objects is None:
                        error_msg = self.formatter.format_error_message("Не удалось получить данные с API")
                        await self.send_message(error_msg)
                        return
                    
                    # Get new objects
                    new_objects = self.data_manager.get_new_objects(current_objects)
                    
                    if new_objects:
                        message = self.formatter.format_new_objects_message(new_objects)
                        await self.send_message(message)
                        logger.info(f"Manual check: found {len(new_objects)} new objects")
                    else:
                        # For manual check, always send result
                        no_objects_message = "🔍 Новых заброшенных объектов в Минском районе за одну базовую не найдено."
                        await self.send_message(no_objects_message)
                        logger.info("Manual check: no new objects found")
                        
                except Exception as e:
                    logger.error(f"Error in manual check: {e}")
                    error_msg = self.formatter.format_error_message(str(e))
                    await self.send_message(error_msg)
                
                logger.info("Manual check command executed")
                
            elif command == '/help':
                help_message = (
                    "🤖 ERI Bot - Мониторинг заброшенных объектов\n\n"
                    "📋 Доступные команды:\n"
                    "• /start - Приветствие и информация о боте\n"
                    "• /status - Показать статус и время последней проверки\n"
                    "• /check - Запустить проверку вручную\n"
                    "• /help - Показать это сообщение\n\n"
                    "🔄 Бот автоматически проверяет новые объекты в Минском районе за одну базовую каждый час.\n\n"
                    "ℹ️ Источник данных: eri2.nca.by"
                )
                await self.send_message(help_message)
                logger.info("Help command executed")
                
        except Exception as e:
            logger.error(f"Error handling command {command}: {e}")
            await self.send_message("❌ Ошибка при выполнении команды")

    async def check_and_notify(self):
        """Check for new objects and send notifications"""
        try:
            logger.info("Starting scheduled check...")
            
            # Fetch current objects
            current_objects = self.api_client.fetch_abandoned_objects()
            
            if current_objects is None:
                error_msg = self.formatter.format_error_message("Не удалось получить данные с API")
                await self.send_message(error_msg)
                return
            
            # Get new objects
            new_objects = self.data_manager.get_new_objects(current_objects)
            
            # Update status tracking
            self.last_check_time = datetime.now()
            self.last_check_result = len(new_objects) if new_objects else 0
            
            if new_objects:
                message = self.formatter.format_new_objects_message(new_objects)
                success = await self.send_message(message)
                
                if success:
                    logger.info(f"Sent notification about {len(new_objects)} new objects")
                else:
                    logger.error("Failed to send notification")
            else:
                logger.info("No new objects found")
                
        except Exception as e:
            logger.error(f"Error in check_and_notify: {e}")
            error_msg = self.formatter.format_error_message(str(e))
            await self.send_message(error_msg)
    
    async def run_forever(self):
        """Run the bot with hourly checks"""
        logger.info("Starting ERI Bot (Simple Version)...")
        logger.info("Log rotation configured: 10MB max size, 5 backup files")
        
        # Test connection first
        if not await self.test_connection():
            logger.error("Failed to connect to Telegram. Check your bot token.")
            return
        
        # Clear ALL pending messages to avoid processing old commands
        try:
            logger.info("Clearing all pending messages...")
            url = f"https://api.telegram.org/bot{self.token}/getUpdates"
            
            # Get all pending updates (don't use proxy)
            response = requests.get(url, timeout=10, proxies={})
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and data.get('result'):
                    updates = data['result']
                    if updates:
                        # Mark all as processed by setting offset to last update_id + 1
                        last_id = updates[-1]['update_id']
                        logger.info(f"Found {len(updates)} pending updates, clearing them...")
                        
                        # Clear all pending updates (don't use proxy)
                        clear_response = requests.get(
                            url, 
                            params={'offset': last_id + 1}, 
                            timeout=10,
                            proxies={}
                        )
                        
                        self.last_update_id = last_id
                        logger.info(f"Cleared all pending messages. Starting from update_id: {self.last_update_id}")
                    else:
                        logger.info("No pending messages found")
        except Exception as e:
            logger.warning(f"Could not clear pending messages: {e}")
        
        # Send startup message
        startup_msg = "🚀 ERI Bot запущен и начинает мониторинг заброшенных объектов в Минском районе за одну базовую"
        await self.send_message(startup_msg)
        
        # Initial check
        await self.check_and_notify()
        
        # Check if API is accessible
        test_result = self.api_client.fetch_abandoned_objects()
        if test_result is None:
            error_msg = (
                "⚠️ Внимание: API недоступен с серверов Railway\n\n"
                "Возможные причины:\n"
                "• Геоблокировка (сервер не в Беларуси)\n"
                "• Защита от ботов\n"
                "• Изменения в API\n\n"
                "Бот продолжит попытки подключения каждый час.\n"
                "Используйте /check для ручной проверки."
            )
            await self.send_message(error_msg)
        
        last_check_time = datetime.now()
        
        while True:
            try:
                # Check for commands less frequently to avoid duplicates
                await self.get_updates()
                
                # Check if it's time for scheduled check (every hour for production)
                now = datetime.now()
                if now - last_check_time >= timedelta(hours=1):
                    await self.check_and_notify()
                    last_check_time = now
                
                # Longer sleep to avoid command duplication
                await asyncio.sleep(5)
                
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                await asyncio.sleep(10)  # Wait 10 seconds on error


async def main():
    """Main entry point"""
    try:
        bot = SimpleEriBot()
        await bot.run_forever()
        
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program terminated")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
