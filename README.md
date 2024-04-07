### Remote Control

- Controll your machine from the browser.

<!-- open pipe -->
browser <==> socket-server <==> ssh-client


#### 1 - Run app ui

```zsh
    docker-compose up --build -d
```
#### 2 - Django server

##### - using pipenv
```zsh
    pipenv sync
    pipenv run python manage.py runserver
```
##### - Or pip
```zsh
    pip install -r requirements.txt
    python manage.py runserver
```

#### 3 - URL
```zsh
   http://localhost:4000 
```
