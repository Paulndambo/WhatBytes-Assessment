# WhatBytes-Assessment
This is a simple django-based web application that simulates user authentication.

The applications showcases several functionalities such as;-
1. User registration and login
2. User password management, i.e, forgot password and password reset.
3. Email notifications.
4. Authentication and Authorization, especially access control.

# Downloading the code and running the code.
Before you clone the repository, make sure you have python installed on your computer.

Then, create a virtual environment so that you can easily manage the project dependencies, use the command below;-
```sql
python -m venv venv
```

or

```sql
python3 -m venv venv
```

After creating the virtual environment activate it using the commands below;-
```sql
source venv\Scripts\activate
```
or
```sql
source venv/bin/activate
```


Proceed to clone the repo using the command below;-
```sql
git clone https://github.com/Paulndambo/WhatBytes-Assessment.git
```
or
```sql
git clone git@github.com:Paulndambo/WhatBytes-Assessment.git
```

Change directory into the cloned folder using;-
```sql
cd WhatBytes-Assessment/
```

Then install dependencies using;-
```sql
pip install -r requirements.txt
```

Then, run the project using;-
```sql
python manage.py runserver
```
or
```sql
python3 manage.py runserver
```

# Accessing on the browser
Open your browser and type <link>http://127.0.0.1:8000</link>