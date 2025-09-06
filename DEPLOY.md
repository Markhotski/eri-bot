# 🚀 Деплой ERI Bot

## 📋 Быстрый старт (Railway - рекомендуется)

### 1. Подготовка репозитория
```bash
# Инициализация git (если еще не сделано)
git init
git add .
git commit -m "Initial commit"

# Создание репозитория на GitHub
# Зайдите на github.com, создайте новый репозиторий
git remote add origin https://github.com/ваш-username/eri-bot.git
git push -u origin main
```

### 2. Деплой на Railway
1. Зайдите на [railway.app](https://railway.app)
2. Войдите через GitHub
3. Нажмите "New Project" → "Deploy from GitHub repo"
4. Выберите ваш репозиторий `eri-bot`
5. Railway автоматически определит Python проект

### 3. Настройка переменных окружения
В панели Railway добавьте переменные:
```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
API_URL=https://eri2.nca.by/api/guest/abandonedObject/search
VIEW_URL_BASE=https://eri2.nca.by/api/guest/abandonedObject
```

### 4. Проверка деплоя
- Бот автоматически запустится
- Проверьте логи в Railway Dashboard
- Отправьте `/start` в Telegram для тестирования

---

## 🐳 Альтернатива: Docker деплой

### Подготовка
```bash
# Создайте .env файл на сервере
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
```

### Запуск через Docker Compose
```bash
# Клонирование репозитория
git clone https://github.com/ваш-username/eri-bot.git
cd eri-bot

# Создание .env файла
cp .env.example .env
# Отредактируйте .env файл

# Запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

---

## 🖥️ VPS деплой (Ubuntu/Debian)

### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install python3 python3-pip python3-venv git -y

# Клонирование репозитория
git clone https://github.com/ваш-username/eri-bot.git
cd eri-bot
```

### 2. Настройка окружения
```bash
# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
cp .env.example .env
nano .env  # Отредактируйте переменные
```

### 3. Создание systemd сервиса
```bash
# Создание сервиса
sudo nano /etc/systemd/system/eri-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=ERI Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/eri-bot
Environment=PATH=/home/your_username/eri-bot/.venv/bin
ExecStart=/home/your_username/eri-bot/.venv/bin/python simple_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Запуск сервиса
```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable eri-bot

# Запуск сервиса
sudo systemctl start eri-bot

# Проверка статуса
sudo systemctl status eri-bot

# Просмотр логов
sudo journalctl -u eri-bot -f
```

---

## 📊 Мониторинг

### Проверка работы бота
```bash
# Проверка процесса
ps aux | grep simple_bot.py

# Просмотр логов
tail -f eri_bot.log

# Проверка места на диске
df -h
du -sh eri_bot.log*
```

### Полезные команды
```bash
# Перезапуск (systemd)
sudo systemctl restart eri-bot

# Остановка
sudo systemctl stop eri-bot

# Обновление кода
git pull
sudo systemctl restart eri-bot
```

---

## ⚠️ Безопасность

1. **Никогда не коммитьте .env файл в git**
2. **Используйте SSH ключи для доступа к серверу**
3. **Регулярно обновляйте систему**
4. **Настройте firewall (ufw)**

```bash
# Базовая настройка firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
```

---

## 🆘 Troubleshooting

### Частые проблемы:
1. **Бот не отвечает** → Проверьте TELEGRAM_BOT_TOKEN
2. **Не приходят уведомления** → Проверьте TELEGRAM_CHAT_ID
3. **Ошибки API** → Проверьте доступ к eri2.nca.by
4. **Высокое потребление места** → Логи ротируются автоматически

### Получение логов:
```bash
# Railway
railway logs

# Docker
docker-compose logs eri-bot

# Systemd
sudo journalctl -u eri-bot --since "1 hour ago"

# Файловые логи
tail -100 eri_bot.log
```
