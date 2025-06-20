
1.  * Трассировка автономных систем. Пользователь вводит доменное имя
    или IP адрес. Осуществляется трассировка до указанного узла, т. е. мы узнаем IP адреса маршрутизаторов, через которые проходит пакет. 
    * Определяет к какой автономной системе относится каждый из полученных IP адресов
    маршрутизаторов, для этого обращается к базам данных региональных интернет регистраторов.
    * Выход: для каждого IP-адреса – результат трассировки (или кусок результата до появления ***), 
    * для "белых" IP-адресов из него указать номер автономной системы.
    * В итоге должна получиться таблица № по порядку IP AS страна и провайдер.
    
---
2. 
    * Кэширующий DNS сервер. 
    * Сервер прослушивает 53 порт. При первом запуске кэш пустой. 
    * Сервер получает от клиента рекурсивный запрос и выполняет разрешение запроса. 
    * Получив ответ, сервер разбирает пакет ответа, извлекает из него ВСЮ полезную информацию, т. е. все ресурсные записи, а не только то, 
    о чем спрашивал клиент. Полученная информация сохраняется в кэше сервера. Например, это может быть два хэш-массива.
    * Сервер регулярно просматривает кэш и удаляет просроченные записи (использует поле TTL).
    * Сервер не должен терять работоспособность (уходить в бесконечное ожидание, падать с
    ошибкой и т. д.), если старший сервер почему-то не ответил на запрос. 
    * Во время штатного выключения сервер сериализует данные из кэша, сохраняет их на диск. 
    * При повторных запусках
    сервер считывает данные с диска и удаляет просроченные записи, инициализирует таким образом свой кэш.
---
3.
   * используя, API В Контакте получает информацию и выводит список друзей указанного пользователя

# DNS Cache Server - Руководство по запуску

## Предварительные требования
- Python 3.8+


## Установка зависимостей
```bash
pip install -r .\requirements.txt
```

## Запуск сервера и тестов

### 1. Основной сервер (main_dns_server.py)
```bash
python main_dns_server.py
```
**Что делает:**
- Запускает DNS-сервер на порту 53
- Кэширует запросы и сохраняет их в `dns_cache.pkl`
- Логирует операции в `dns_server.log`

### 2. Запуск через nslookup
**Если провалиться в консоль `nslookup`:**
```bash
nslookup
```
```bash
server 127.0.0.1
```
```bash
vk.com
```
**Если в одну строку:**
```bash
nslookup google.com 127.0.0.1
```
**Содержимое скрипта:**
```text
Non-authoritative answer:
Name:   vk.com
Address: 87.240.129.133
Name:   vk.com
Address: 87.240.132.78
Name:   vk.com
Address: 87.240.132.72
Name:   vk.com
Address: 93.186.225.194
Name:   vk.com
Address: 87.240.137.164
Name:   vk.com
Address: 87.240.132.67
```

### 3. Проверка кэша (check_cache.py)
```bash
python check_cache.py
```

**Что делает:**
- Данные из `dns_cache.pkl` записывает в файл `dns_cache.json`.

**Пример JSON:**
```json
{
  "timestamp": "2025-06-12T18:49:09.875235",
  "cache_source": "dns_cache.pkl",
  "records": [
    {
      "domain": "google.com",
      "type": "A",
      "expires": "2025-06-12T18:53:53.788311",
      "ttl_remaining": 283,
      "records": [
        "216.58.210.174"
      ]
    },
    {
      "domain": "google.com",
      "type": "AAAA",
      "expires": "2025-06-12T18:53:53.896557",
      "ttl_remaining": 284,
      "records": [
        "2a00:1450:4026:805::200e"
      ]
    },
    {
      "domain": "vk.com",
      "type": "A",
      "expires": "2025-06-12T18:55:24.871214",
      "ttl_remaining": 374,
      "records": [
        "87.240.132.67",
        "87.240.129.133",
        "93.186.225.194",
        "87.240.132.72",
        "87.240.137.164",
        "87.240.132.78"
      ]
    }
  ]
}
```

## Структура файлов
```
.
├── main_dns_server.py    # Основной сервер
├── check_cache.py   # Проверка кэша
├── dns_cache.pkl    # Файл кэша (создаётся автоматически)
├── dns_server.log   # Лог операций
└── dns_cache.json   # Файл кеша (в формате json)
```
## Особенности работы
1. Сервер автоматически создает `dns_cache.pkl` при первом запуске
2. Для первой работы сервера, удалить 3 файла: `dns_server.log`, `dns_cache.pkl`, `dns_cache.json`
3. Кэш обновляется каждые 60 секунд
4. Для корректного завершения нажмите `Ctrl+C`
5. DNS Сервер запущен на 53 порту
6. Проверяет записи типа А, АААА, NS, PTR, но можно указать явно `nslookup -type=AAAA google.com 127.0.0.1`
7. Новая версия находится в директории `DNS_Server_prod/DNS_v5`
