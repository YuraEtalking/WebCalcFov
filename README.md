# WebCalcFov.

Считает высоту и ширину кадра на заданном расстоянии в зависимости от фокусного
расстояния объектива и физического размера матрицы.
ТАк же сервис имеет вики по камерам и объективам с разными данными и ссылками 
на обзоры/обсуждения/гайды.

## Запуск

Клонировать репозиторий:

```
git clone https://github.com/YuraEtalking/WebCalcFov.git
```
Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
```
source venv/bin/activate
```
```
.\venv\Scripts\Activate.ps1
```
Обновить pip:

```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
#### Запуск приложения:
```
uvicorn backend.main:app --reload
```
<br>

#### Админ панель:
```
http://127.0.0.1:8000/admin
```
<br>

#### Документация:
```
http://127.0.0.1:8000/docs
```
<br>


## Стек технологий
- **Python 3.10+**
- **Fast API**
- **uvicorn**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **SQLAdmin**

<br>

#### Автор [Юрий Рыжков](https://github.com/YuraEtalking)