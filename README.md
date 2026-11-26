# TVA Archive

Вебсервіс на Flask і SQLite для обліку записів.

## Запуск

python app.py

## Приклади curl

curl http://127.0.0.1:5000/items
curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d '{"code":"TVA-01","branch":"alpha","risk":4.5,"note":"first"}'
curl "http://127.0.0.1:5000/items?branch=alpha"
curl -i http://127.0.0.1:5000/report
curl -i -X DELETE http://127.0.0.1:5000/items/1
