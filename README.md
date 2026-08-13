# Справочник по фототехнике и инструменты.
Справочник будет иметь; паспортные данные по технике, ссылки на обзоры/тесты,
мфт графики, примеры фотографий и внешнего вида, страницы сравнений, 
сценарии использования, совместимости, база типичных неисправностей, аналоги и тп.


#### WebCalcFov
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

## Создание перевода страниц:
Пример в шаблоне:
```
<li>{{ _("Manufacturer") }}: {{ lens.manufacturer }}</li>
<li>{{ _("Mount") }}: {{ lens.bayonet.name }}</li>
```

### Шаг 1. Сканируем проект и ищем строки обёрнутые в _()
Из корневой папки **WebCalcFov** нужно выполнить:
```
pybabel extract -F babel.cfg -o messages.pot .
```
для создания технического шаблона **messages.pot**

### Шаг 2. Инициализируем(создаем) директории и файлы переводов

Нужно создать версию перевода, например русский
```
pybabel init -i messages.pot -d locales -l ru
```
или английски
```
pybabel init -i messages.pot -d locales -l en
```

Это создаст директорию **locales** в корне(WebCalcFov) со структурой
```
ru/LC_MESSAGES/messages.po
```
```
en/LC_MESSAGES/messages.po
```
### Шаг 3. Редактируем messages.po

Мы редактируем **messages.po**

для русского языка пример:

в ключ **msgstr** добавляем перевод
```
msgid "Manufacturer"
msgstr "Производитель"

msgid "Mount"
msgstr "Байонет"
```
Для английского языка пример:
```
msgid "Manufacturer"
msgstr "Manufacturer"

msgid "Mount"
msgstr "Mount"
```
### Шаг 4. Финал. Компелируем переводы.

Компиляция переводов.

После редактирования .po файлов нужно скомпилировать их в .mo
```
pybabel compile -d locales
```
Рядом с **messages.po** будет создан **messages.mo**

## Обновление перевода:
Например, добавляем еще строки:
```
<li>{{ _("Weight") }}: {{ lens.weight }}</li>
<li>{{ _("Focal length") }}: {{ lens.focal_length }}</li>
```
### Шаг 1. Обновление messages.pot
Обновляем **messages.pot** что бы найти новые строки обернутые в _()
```
pybabel extract -F babel.cfg -o messages.pot .
```
### Шаг 2. Обновление messages.po
Обновить существующий **messages.po**

Команда будет не **ini**, а **update**

Эта команда добавит новые строки в существующие файлы
```
locales/ru/LC_MESSAGES/messages.po
```
```
pybabel update -i messages.pot -d locales
```
### Шаг 3. Редактирование messages.po
Редактируем появившиеся строки, например в русском файле
```
msgid "Weight"
msgstr "Вес"

msgid "Focal length"
msgstr "Фокусное расстояние"
```
### Шаг 4. Финал. Компилируем обновленный messages.po
Тут команда не меняется.
```
pybabel compile -d locales
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
