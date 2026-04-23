# WebCalcFov.

Считает высоту и ширину кадра на заданном расстоянии в зависимости от фокусного
расстояния объектива и физического размера матрицы.

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
uvicorn main:app --reload
```
<br>

## Стек технологий
- **Python 3.10+**
- **Fast API**
- **uvicorn**

<br>

#### Автор [Юрий Рыжков](https://github.com/YuraEtalking)