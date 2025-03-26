# Template para projetos
Um template atualizado para novos projetos, ao invés de usar o template gerado pelo próprio Django.

## Rodar o Container
- Criar arquivo `.env` na raiz no projeto usando o exemplo `.env.sample`

- ### Rodar o container
```docker-compose up --build```

## Para desenvolvimento
- Criar uma .venv com `python3 -m venv .nome-venv
- Ativar a venv com 
```shell source .venv/bin/activate```
- Instalar o pre-commit com `pre-commit install`