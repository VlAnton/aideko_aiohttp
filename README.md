Тестовое для Айдеко на aiohttp.
=====================

Запускаем приложение. Из корневой папки прописываем следующее:
-----------------------------------

- python3 -m venv aideko
- source aideko/bin/activate
- pip install --upgrade pip; pip install -r requirements.txt
- cd aideko_project
- python entry.py

Урлы приложения:
-----------------------------------

- /news — список неудаленных новостей
- /news/{id} — взятие новости по id с выводом списка соответствующих комментариев
