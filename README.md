# ValutaTrade Hub

Торговая платформа с интерфейсом командной строки для обмена фиатными и криптовалютными активами.

## Описание

ValutaTrade Hub - это симулятор торговой платформы на Python, который позволяет пользователям:
- Регистрироваться и входить в личные кабинеты
- Покупать и продавать различные валюты (фиатные и криптовалюты)
- Просматривать портфель и текущие курсы обмена
- Отслеживать рыночные данные в реальном времени с автоматическим обновлением

## 🚀 Функциональности

- **👤 Управление пользователями**: Регистрация, вход, смена пароля
- **💱 Торговые операции**: Покупка и продажа валют
- **📊 Управление портфелем**: Просмотр баланса, общей стоимости активов
- **📈 Курсы валют**: Получение текущих курсов, автоматическое обновление
- **🔐 Безопасность**: Хеширование паролей с использованием соли
- **📋 История операций**: Весь обмен курсов сохраняется в историю

## 💰 Поддерживаемые валюты

### Фиатные валюты:
- **USD** ($) - базовая валюта
- **EUR** (€)
- **GBP** (£)
- **RUB** (₽)

### Криптовалюты:
- **BTC** (Bitcoin)
- **ETH** (Ethereum) 
- **SOL** (Solana)

## ⚙️ Установка и запуск

### Требования
- Python 3.10 или выше
- Установленный Poetry

### Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd valutatrade_hub
```

2. Установите зависимости через Poetry:
```bash
poetry install
```

3. Установите переменные окружения:
```bash
export EXCHANGERATE_API_KEY='your_api_key_here'
```

4. Запустите приложение:
```bash
poetry run project
```

Или напрямую:
```bash
python main.py
```

## 🎮 Использование

### Основные команды:

#### Аутентификация:
```bash
register --username <name> --password <password>
login --username <name> --password <password>
change-password --password <new_password>
```

#### Торговые операции:
```bash
buy --currency <currency> --amount <amount>
sell --currency <currency> --amount <amount>
```

#### Просмотр информации:
```bash
show-portfolio
get-rate --from <currency> --to <currency>
show-rate --top true/false
```

#### Системные команды:
```bash
update-rates
exit
```

### Примеры использования:

1. **Регистрация и вход:**
```bash
>>> register --username john --password secret123
>>> login --username john --password secret123
```

2. **Покупка Bitcoin:**
```bash
>>> buy --currency btc --amount 0.1
```

3. **Просмотр портфеля:**
```bash
>>> show-portfolio
```

4. **Получение курса обмена:**
```bash
>>> get-rate --from usd --to eur
```

## 🏗️ Архитектура проекта

```
valutatrade_hub/
├── core/                    # Ядро приложения
│   ├── models.py           # Модели данных (User, Wallet, Portfolio)
│   ├── usercases.py        # Бизнес-логика
│   ├── utils_funcs.py      # Вспомогательные функции
│   └── exceptions.py       # Пользовательские исключения
├── infra/                   # Инфраструктурный слой
│   ├── database.py         # Менеджер базы данных
│   ├── consts.py           # Константы и настройки
│   └── logger.py           # Логирование
├── parser_service/         # Сервис парсинга и обновления курсов
│   ├── updater.py          # Обновление курсов валют
│   ├── scheduler.py        # Планировщик обновлений
│   ├── api_clients.py      # API клиенты для получения данных
│   └── config.py           # Конфигурация парсера
├── cli/                    # Интерфейс командной строки
│   ├── interface.py        # Основной CLI интерфейс
│   └── parser.py           # Парсер пользовательского ввода
├── data/                   # Файлы данных (JSON)
├── main.py                 # Точка входа в приложение
└── pyproject.toml          # Конфигурация проекта и зависимости
```

## 🔧 Технологии

- **Python 3.10+** - основной язык программирования
- **Poetry** - управление зависимостями
- **Requests** - HTTP запросы к API
- **JSON** - хранение данных
- **SHA-256** - хеширование паролей

## 📊 Базы данных

Проект использует JSON файлы для хранения данных:
- `users.json` - данные пользователей
- `portfolios.json` - портфели пользователей  
- `rates.json` - текущие курсы валют
- `exchange_rates.json` - история курсов

## 🔄 API интеграции

- **CoinGecko API** - получение курсов криптовалют
- **ExchangeRate-API** - получение курсов фиатных валют

## 🛡️ Безопасность

- Пароли хешируются с использованием SHA-256 и соли
- Изоляция пользовательских данных

## Установка

Перед установкой, убедитесь, что у вас установлен менеджер зависиостей поэтри и make
```bash
git clone https://github.com/arthuraswork/final-project #установка 
cd final-project 
poetry install #установка запвисимостей
export EXCHANGERATE_API_KEY='your_key' #добавление свого апи в окружение
poetry run project
 ```

[![asciicast]( https://asciinema.org/a/Zq1agv7OHQ0YBPfM1bxeOqkgo.svg)]( https://asciinema.org/a/Zq1agv7OHQ0YBPfM1bxeOqkgo)

