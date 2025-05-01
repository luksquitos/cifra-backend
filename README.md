# Cifra Marketplace API

## Rodar o Container
- Criar arquivo `.env` na raiz no projeto usando o exemplo `.env.sample`
- Subir o container: `docker compose up --build`
- Derrubar o container: `docker compose down`

## Conta Admin
Email: admin@admin.com
Senha: admin

## Para desenvolvimento
- Criar uma .venv com `python3 -m venv .nome-venv`
- Ativar a venv com `source .venv/bin/activate`
- Instalar o pre-commit com `pre-commit install`

## Carregar as fixtures.
Esse comando foi removido do entrypoint, porque o arquivo de histórico de preço é muito grande e estava demorando para carregar todos os dados.

``` docker compose exec api python manage.py loaddata stores categories products price_histories```
