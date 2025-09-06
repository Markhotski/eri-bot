# 🤖 ERI Bot

Telegram бот для мониторинга заброшенных объектов в Минском районе за одну базовую.

## 🚀 Возможности

- ✅ Автоматический мониторинг каждый час
- ✅ Уведомления о новых объектах в Telegram
- ✅ Команды `/start`, `/status`, `/check`, `/help`
- ✅ Ротация логов (10MB, 5 файлов)
- ✅ Docker поддержка

## 🛠️ Технологии

- Python 3.10
- Telegram Bot API (прямые запросы)
- eri2.nca.by API
- Docker

## ⚙️ Настройка

1. Создайте `.env` файл:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

2. Запуск локально:
```bash
pip install -r requirements.txt
python simple_bot.py
```

3. Запуск в Docker:
```bash
docker-compose up --build
```

4. Деплой:
```bash
git push origin main
```

## 📋 Команды бота

- `/start` - Приветствие и информация
- `/status` - Статус последней проверки
- `/check` - Ручная проверка новых объектов
- `/help` - Справка по командам

## 🔧 Конфигурация

Настройки в `config.py`:
- `SEARCH_PAYLOAD` - параметры поиска API
- `ateId: 19824` - Минский район
- `oneBasePrice: True` - за одну базовую
- Интервал проверки: 1 час