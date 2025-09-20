# 📅 Schedule Parser Bot

Парсер расписания с сайта [Dnevnik.ru](https://dnevnik.ru) с использованием **Selenium**, сохранением данных в **PostgreSQL** и динамической отправкой в **Telegram-бота**.  

Теперь, чтобы узнать расписание, не нужно заходить на старый и медленный сайт — бот спарсит и достанет его для вас из базы за **миллисекунды** ⚡

---

## 🚀 Возможности

- 🔄 Автоматический парсинг расписания каждые **12 часов**  
- 🔐 Для работы нужен только **логин и пароль** от `dnevnik.ru`    
- 💾 Сохранение расписания в PostgreSQL
- 📅 Ежедневная авто-рассылка расписания в чат по подписке
- 🤖 Телеграм-бот с командами:
  - `/расписание ДД.ММ.ГГГГ` — расписание на выбранный день  
  - `/добавить` — подписка на ежедневную автоотправку   
  - `/удалить` — отписка от автоотправки  
  - `/help` — помощь по командам  
  - `/start` — стартовое меню  

- ⚙️ Кастомизация:
  - Количество недель для парсинга (по умолчанию **2 недели**)  
  - Имя группы/класса задаётся в `.env`  
  - Время автоотправки (часы и минуты в формате UTC)  

---

## 🛠 Настройка и запуск
### 1. Клонируйте репозиторий

Сделайте это командой:
```bash
git clone git@github.com:thetrueryan/schedule_parser_bot.git
```

### 2. Переменные окружения
Создайте файл `.env` и укажите в нём:
```env
# токен бота
BOT_TOKEN=YOUR_BOT_TOKEN # Получите токен бота через BotFather

# кастомизация бота
GROUP_NAME=YOUR_GROUP_NAME # Название вашей группы или класса
WEEKS_TOTAL=TOTAL_WEEK_TO_PARSE_SCHEDULE # DEFAULT=2 (сколько недель будет парсить бот)
NOTIFICATION_TIME_HOUR=YOUR_NOTIFICATION_HOUR #Важно!! Время указывается в UTC, по этому для отправки например в 14:00 по МСК надо указать 11 УЧТИТЕ ЭТО!!
NOTIFICATION_TIME_MINUTES=YOUR_NOTIFICATION_MINUTES #DEFAULT=0 (минуты для времени автоотправки)

# Парсер
DNEVNIK_URL="https://dnevnik.ru/"
DNEVNIK_LOGIN=YOUR_DNEVNIK_LOGIN
DNEVNIK_PASS=YOUR_DNEVNIK_PASS

# PostgreSQL БД
DB_HOST=YOUR_DB_HOST # DEFAULT=localhost
DB_PASS=YOUR_DB_PASS
DB_USER=YOUR_DB_USER # DEFAULT=postgres
DB_PORT=YOUR_DB_PORT # DEFAULT=5432
DB_NAME=YOUR_DB_NAME # DEFAULT=postgres
```

### 3. Запуск в Docker (рекомендуется ✅)

В проекте есть готовый Dockerfile и docker-compose.yml.
Бот уже собран в [Docker Hub](https://hub.docker.com/repository/docker/thetrueryan/schedule_parser_bot/):
```bash
thetrueryan/schedule_parser_bot:latest
```

Запуск:
```bash
docker-compose up -d
```
- Поднимется PostgreSQL и сам бот (все переменные будут подтянуты из .env)
- В образ автоматически добавлен Linux chromedriver для Selenium

### 4. Запуск без Docker (Важно, перед запуском необходимо самому создать БД PostgreSQL

- Для Linux можно использовать chromedriver из репозитория
- Для Windows необходимо скачать актуальный [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/#stable) и заменить им chromedriver в директории проекта

Установка зависимостей через poetry:
```bash
pip install poetry # если не установлен
poetry install # установка зависимостей
poetry shell
```

Установка зависимостей через pip (если предпочитаете его):
```bash
pip install -r requirements.txt
```

Запуск:
```bash
alembic upgrade head # создаем таблицы в базе данных
python -m src.main 
```

---

## 📦 Стек

- Python 3.12+
- Aiogram 3x
- Selenium
- fake-useragents
- PostgreSQL
- SQLAlchemy 2.0
- Alembic


---

## 🔧 Рекомендации

- Запускать на сервере для бесперебойной работы
- Использовать docker-compose для изоляции и автоподнятия базы

---

## 📝 Лицензия

MIT License. Проект создан для личного использования и обучения.

**Буду рад звёздочке ⭐ на GitHub**
