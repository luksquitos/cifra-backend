# Cifra
Comparador de preços bolado.

## Comandos

Rodar o container
```
docker-compose up --build
```

Criar migrations
```
docker-compose exec api ./manage.py makemigrations
```

Aplicar migrations
```
docker-compose exec api ./manage.py migrate
```

Acessar terminal do container do serviço API
```
docker exec -it api bash
```

Acessar linha de comando do postgres
```
docker exec -it db psql -U postgres
```

## Configurações iniciais 

- Entre no terminal do container com o comando 
```
docker exec -it api bash
```

- Dentro desse terminal execute os seguintes comandos 
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser

Apenas username e password serão necessários
Para acessar os endpoints da admin_api será necessário criar um super usuário.

## Endpoints 

-Tem os que estão na raiz " / "
- localhost:8000/api/token - Recebe username e password para receber o token jwt
- localhost:8000/admin - Apenas para testes e criar instâncias mais rápidamente.
