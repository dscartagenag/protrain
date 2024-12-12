rm ./protrain/db.sqlite3
touch ./protrain/db.sqlite3

find ./protrain "*_initial.py_" -delete
find ./protrain "*.pyc" -delete

python3 manage makemigrations
python3 manage migrate

