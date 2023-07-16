**Послідовність запуску:**
1. `git clone -b hometask-13.2 git@github.com:oleverse/PyEduWebHT10.git PyEduWebHT13.2`
2. Створимо віртуальне середовище і встановимо залежності:   
`cd PyEduWebHT13.2`  
`poetry shell`  
`poetry update`
3. Створимо і запустимо контейнер з БД, підставивши свої значення до плейсхолдерів:    
`docker run --name django-postgres -p <DB_PORT>:5432 -e POSTGRES_PASSWORD=<DB_PASSWORD> -d <DB_NAME>`
4. Переходимо до кореня Django-проєкту  
`cd hometask10`
5. Перейменувати, або скопіювати файл env_sample на .env з таким вмістом:  
`DB_ENGINE=django.db.backends.postgresql_psycopg2`  
`DB_NAME=<DB_NAME>`  
`DB_USER=postgres`  
`DB_PASS=<secret>`  
`DB_HOST=127.0.0.1`  
`DB_PORT=<DB_PORT>`  
Не забудьте змінити значення плейсхолдерів на такі ж, що вказали при створенні контейнера postgresql
6. Виконуємо міграцію БД:  
`python manage.py migrate`
7. Запускаємо сервер з ключем --insecure, щоб Django обробляв запити на статичні ресурси,
або у файлі hometask10/settings.py вмикаємо Debug режим `DEBUG = True`  
`python manage.py runserver --insecure`
8. Відкриваємо у браузері адресу застосунку  
`http://127.0.0.1:8000`
9. На початку БД порожня, щоб заповнити її даними, виконаємо скрейпінг сайту `https://quotes.toscrape.com`.
Для цього у правому верхньому кутку головної сторінки застосунку натискаємо на посилання
`Scrape quotes`. Відкриється проста readonly-форма, де вказано URL джерела цитат для скрейпінгу.
Натискаємо кнопку `Start scraping` і чекаємо завершення процесу заповнення БД даними.
Після завершення скрейпінгу на сторінці з'явиться звіт про зчитані дані.
10. Переходимо на головну сторінку, клікнувши на заголовок застосунку і бачимо список цитат.
11. Для створення авторів і цитат, потрібно перейти за посиланням `Sign Up` і створити користувача.
Після цього можна авторизуватися і у меню з'являться пункти `Add Author` i `Add Quote`
12. Створення нових тегів наразі не реалізовано, можна лише додавати до нових цитат існуючі теги. 
13. Цитати на головній сторінці навмисно відсортовані за датою їх створення у БД, тому, коли
користувач додасть свою цитату, то вона буде показана першою.
14. Для економії часу сайт має ідентичний дизайн, як у сайта-джерела, але з деякими відмінностями.
15. Пейджінація реалізована.
16. Для управління даними застосунку з адмін-панелі спочатку потрібно створити супер-адміністратора  
`python manage.py createsuperuser`
17. Для того щоб скинути пароль користувача, потрібно перейти на сторінку `Login` і обрати
знизу посилання `Forgot password?`