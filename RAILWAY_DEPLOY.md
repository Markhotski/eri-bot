# 🚀 Railway Deployment Guide

## ✅ Готово к деплою

Проект настроен для Railway с использованием **Nixpacks** (не Docker).

### 🔧 Настройка Railway

1. **Убедитесь что используется Nixpacks:**
   - Railway Dashboard → Settings → Environment
   - Builder: **NIXPACKS** (не Docker)

2. **Переменные окружения:**
   
   **Сначала для успешной сборки (без прокси):**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```
   
   **После успешной сборки добавить прокси:**
   ```
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
2. **ВАЖНО: Временно удалите HTTPS_PROXY** для сборки
3. Проверьте переменные окружения
4. Посмотрите логи сборки в Railway

**Ошибка nixpkgs download:**
```
Could not connect to server (7) Failed to connect to 185.162.131.20
```
**Решение:** Удалите переменную `HTTPS_PROXY` в Railway, дождитесь успешной сборки, затем добавьте обратно.

**Если API 403:**
1. Попробуйте другой прокси
2. Или уберите HTTPS_PROXY переменную временно

### 📋 Пошаговая инструкция

1. **Удалите HTTPS_PROXY** в Railway Variables
2. **Сделайте commit и push**
3. **Дождитесь успешной сборки**
4. **Добавьте HTTPS_PROXY обратно**
5. **Проверьте работу бота**
