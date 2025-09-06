# 🚀 Railway Deployment Guide

## ✅ Готово к деплою

Проект настроен для Railway с использованием **Nixpacks** (не Docker).

### 🔧 Настройка Railway

1. **Убедитесь что используется Nixpacks:**
   - Railway Dashboard → Settings → Environment
   - Builder: **NIXPACKS** (не Docker)

2. **Переменные окружения:**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   HTTPS_PROXY=http://185.162.131.20:3128
   ```

3. **Деплой:**
   ```bash
   git add .
   git commit -m "Deploy with Nixpacks: remove Docker, add Railway config"
   git push
   ```

### 📁 Файлы конфигурации

- `Procfile` - команда запуска для Railway
- `railway.json` - настройки Railway
- `nixpacks.toml` - конфигурация Nixpacks builder
- `requirements.txt` - зависимости Python
- `.railwayignore` - исключения при деплое

### 🎯 Преимущества Nixpacks vs Docker

✅ **Быстрая сборка** - не нужно собирать Docker образ
✅ **Автоматическое определение** Python проекта
✅ **Стабильность** - Railway оптимизирован для Nixpacks
✅ **Простота** - меньше конфигурации

### 🐳 Docker для локальной разработки

Docker файл сохранен как `Dockerfile.backup` для локального использования:

```bash
# Восстановить для локальной разработки
mv Dockerfile.backup Dockerfile

# Запустить локально
docker build -t eri-bot .
docker run --env-file .env eri-bot
```

### 📊 Ожидаемые логи Railway

После успешного деплоя:
```
✅ Build completed
✅ Deployment successful
✅ Starting ERI Bot (Simple Version)...
✅ Global proxy detected - HTTPS: http://...
✅ Bot connected: @EriMonitorBot
```

### 🆘 Troubleshooting

**Если сборка не работает:**
1. Проверьте что Builder = NIXPACKS
2. Проверьте переменные окружения
3. Посмотрите логи сборки в Railway

**Если API 403:**
1. Попробуйте другой прокси
2. Или уберите HTTPS_PROXY переменную временно
