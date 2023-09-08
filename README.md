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
