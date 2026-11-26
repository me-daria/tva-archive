# TVA Archive

Вебсервіс на Flask і SQLite для обліку записів.

## Запуск сервера

Запускати з теки проєкту (`tva-archive`) з активованим віртуальним оточенням (`venv`):

1. Спочатку запустити сервер `waitress`:
   `waitress-serve --listen=127.0.0.1:8000 app:app`

2. Потім у другому терміналі запустити тунель `cloudflared`:
   `cloudflared tunnel --url http://127.0.0.1:8000`