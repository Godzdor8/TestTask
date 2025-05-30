# Тестовое задание
## Описание
Тестовое задание в компанию СовКомБанк на позицию разработчика 

## Установка и запуск
- Склонируйте репозиторий

``` bash
git clone https://github.com/Godzdor8/TestTask
```
- Установите зависимости

``` bash 
pip install -r requirements.txt
```

- Создайте файл .env и добавьте в него переменные окружения

``` .env
DADATA_API_KEY=<ВАШ_API_КЛЮЧ>
DADATA_SECRET_KEY=<ВАШ_СЕРКРЕТНЫЙ_КЛЮЧ>
DATABASE_URL=postgresql://user:password@localhost:5432/bankruptcy
```
- Создайте базу данных bankruptcy

``` sql
CREATE DATABASE bankruptcy;
```
- Запустите проект

``` bash
python main.py
```