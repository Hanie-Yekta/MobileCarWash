# Installation
1. <a href="https://github.com/Hanie-Yekta/MobileCarWash?tab=readme-ov-file#installation">**Clone the repository**</a>

<br>

2. **Create and active virtual environment** (On Windows)
```
cd MobileCarWash
cd CarWashBackEnd
virtualenv venv
venv\Scripts\Activate
cd MobileCarWashBackEnd
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
