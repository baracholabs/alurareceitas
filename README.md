# Receitas

Projeto laboratório django - ágina de receitas (alura receitas)

## Dependências

-[poetry](https://python-poetry.org/)

## Run?

Instalar Dependências

```
$ poetry install
```

Criar/atualizar base e estrutura de dados

```
$ poetry run python manage.py migrate
```

Criar o super user de admin

```
$ poetry run python manage.py createsuperuser
```

Rodar o server local

```
$ poetry run python manage.py runserver
```

Estará disponível em `http://127.0.0.1:8000/`

Admin em `http://127.0.0.1:8000/admin`
