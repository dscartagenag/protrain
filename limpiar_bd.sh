rm db.sqlite3
touch db.sqlite3

find ./ -name "*_initial.py" -delete
find ./ -name "*.pyc" -delete

python3 manage.py makemigrations
python3 manage.py migrate

