# 🛠️ Устранение ошибки 403 Forbidden

## 🚨 Проблема
API `eri2.nca.by` возвращает ошибку 403 Forbidden при запросах с серверов Railway.

## 🔍 Причины
1. **Геоблокировка** - API доступен только из Беларуси/России
2. **Защита от ботов** - блокировка автоматических запросов
3. **IP-блокировка** - серверы Railway в черном списке

## ✅ Решения

### Решение 1: Использование прокси
В Railway Variables добавьте:
```
HTTPS_PROXY=http://proxy-server:port
```

**Бесплатные прокси (Беларусь/Россия):**
- `http://91.241.19.134:8080`
- `http://185.162.131.20:3128`
- `http://194.67.91.153:3128`

### Решение 2: VPS в Беларуси
Перенести бота на VPS в Беларуси:
- **beget.com** - от 200₽/месяц
- **timeweb.com** - от 200₽/месяц
- **selectel.ru** - от 300₽/месяц

### Решение 3: Hybrid подход
Запустить API-клиент локально/VPS, а бота на Railway:
1. Создать простой API-прокси на VPS
2. Бот обращается к вашему API вместо eri2.nca.by

## 🧪 Тестирование API

### Локальный тест:
```bash
curl -X POST "https://eri2.nca.by/api/guest/abandonedObject/search" \
  -H "Content-Type: application/json" \
  -d '{"pageSize": 5, "pageNumber": 0, "sortBy": 1, "sortDesc": true, "abandonedObjectId": null, "fromInspectionDate": null, "toInspectionDate": null, "fromEventDate": null, "toEventDate": null, "abandonedObjectTypeId": 1, "stateTypeId": null, "stateGroupId": null, "stateSearchCategoryId": 2, "streetId": null, "ateId": 19824, "oneBasePrice": true, "emergency": false, "destroyed": false, "fromDeterioration": null, "toDeterioration": null, "fromMoneyAmount": null, "toMoneyAmount": null}'
```

### Тест через прокси:
```bash
curl -X POST "https://eri2.nca.by/api/guest/abandonedObject/search" \
  --proxy "http://proxy-server:port" \
  -H "Content-Type: application/json" \
  -d '{"pageSize": 5, ...}'
```

## 📊 Мониторинг

Бот продолжит работать и:
- ✅ Отвечать на команды `/start`, `/status`, `/help`
- ✅ Показывать информативные сообщения об ошибках
- ✅ Делать попытки подключения каждый час
- ✅ Уведомлять о проблемах с API

## 🎯 Рекомендации

1. **Краткосрочно**: Попробуйте прокси
2. **Долгосрочно**: Используйте VPS в Беларуси
3. **Альтернатива**: Создайте API-прокси сервис
