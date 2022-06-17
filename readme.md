# HR Management System

---

## Endpoints

** `/employees/register`
** `/employees/login`
** `/employees/logout`
** `/employees/checkin`
** `/employees/checkout`
** `/employees/history`

## models

1 - Employee
2- Attendence

## installation

- you should install isolated virtual environment with python3
- [1] to make environment `python3 -m venv .venv`

- [2] to activate environment `source .venv/bin/activate` in linux
  for windows `.venv/Scripts/activate`

- [3] to install requirements `pip install -r requirements.txt`

- [4] create a user in mysql
  `create user 'hrmanager'@'localhost' identified by 'hrmanager';`

---

- [5] create database with `create database hrmanagement;`

- to grante access for this database user
  `GRANT All ON hrmanagement.* TO 'hrmanager'@'localhost';`

---

- to rum migrations
  `python3 manage.py makemigrations` then
  `python3 manage.py migrate`
- to run server `python3 manage.py runserver`
