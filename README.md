h1 Тестовое для Айдеко на aiohttp.

h2 Запускаем приложение. Из корневой папки прописываем следующее:

- python3 -m venv aideko
- . aideko/bin/activate
- pip install --upgrade pip; pip install -r requirements.txt
- cd aideko_project
- python entry.py

h2 Урлы приложения:
- / — список неудаленных новостей
- /{id} — взятие новости по id с выводом списка соответствующих комментариев
