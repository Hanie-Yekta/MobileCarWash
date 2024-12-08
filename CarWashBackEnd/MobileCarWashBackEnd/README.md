# Installation
1. <a href="">**Clone the repository**</a>

<br>

2. **Create and active virtual environment** (On Windows)
```
virtualenv venv
venv\Scripts\Activate
cd project
```

<br>

3. **Install the dependencies**
```
pip install -r requirements.txt
```

<br>

4. **Apply migrations**:
```
python manage.py migrate
```

<br>

5. **Create a superuser**:
```
python manage.py createsuperuser
```

<br>

6. **Run**:
```
python manage.py runserver
```
