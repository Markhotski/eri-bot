# 🪟 Запуск ERI Bot на Windows

## 📋 Подготовка

### 1. Скачайте файлы
Создайте папку `eri-bot` и поместите туда:
- `docker-compose-windows.yml` (переименуйте в `docker-compose.yml`)
- `.env` (создайте новый файл)
- `eri_bot.log` (создайте пустой файл)
- `last_check_data.json` (создайте файл с содержимым ниже)

### 2. Создайте файл `.env`
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
TELEGRAM_CHAT_ID=ваш_chat_id

# API Configuration
API_URL=https://eri2.nca.by/api/guest/abandonedObject/search
VIEW_URL_BASE=https://eri2.nca.by/api/guest/abandonedObject
CHECK_INTERVAL_HOURS=1

# Если нужен прокси, раскомментируйте:
# HTTP_PROXY=http://your-proxy:port
# HTTPS_PROXY=http://your-proxy:port
```

### 3. Создайте файл `last_check_data.json`
```json
{
  "last_checked_ids": [],
  "last_update": null,
  "objects_count": 0
}
```

### 4. Создайте пустой файл `eri_bot.log`
Просто создайте пустой текстовый файл с именем `eri_bot.log`

## 🚀 Запуск

### Через командную строку:
```bash
# Перейти в папку с проектом
cd C:\path\to\eri-bot

# Запустить
docker-compose up -d

# Посмотреть логи
docker-compose logs -f eri-bot

# Остановить
docker-compose down
```

### Через Docker Desktop:
1. Откройте Docker Desktop
2. Перейдите в "Containers"
3. Нажмите "Run" рядом с `eri-bot`
4. Для просмотра логов нажмите на контейнер → "Logs"

## ✅ Проверка работы

Бот должен:
- ✅ Отправить стартовое сообщение в Telegram
- ✅ Отвечать на команды `/start`, `/check`, `/status`, `/help`
- ✅ Проверять API каждый час
- ✅ Логировать действия в файл `eri_bot.log`

## 🔧 Устранение неполадок

### Ошибка "no matching manifest for linux/amd64"
- Убедитесь что используете `docker-compose-windows.yml`
- Проверьте что указана строка `platform: linux/amd64`

### Бот не отвечает
- Проверьте токен в `.env` файле
- Убедитесь что `CHAT_ID` правильный

### API не работает
- Это нормально из некоторых стран
- Используйте прокси в `.env` файле

## 📊 Команды бота

- `/start` - Приветствие и инфо
- `/check` - Ручная проверка API
- `/status` - Статус работы
- `/help` - Справка по командам

**Бот автоматически проверяет API каждый час! 🕐**
