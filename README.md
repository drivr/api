# API ![Continuous Integration](https://github.com/drivr/api/workflows/Continuous%20Integration/badge.svg)

## Desenvolvimento

Para o desenvolvimento dessa aplicação, é necessário que tenha-se o Python 3.9+, Docker e Poetry como gerenciador de dependências e ambiente. Antes de ir adiante e mostrar como construir o projeto (e/ ou executar os testes), vamos preparar o ambiente.

Neste projeto estamos utilizando a versão 3.9.1 do Python, então primeiramente faça a [instalação](https://www.python.org/downloads/) da versão especificada. Uma vez que você tenha o Python instalado, [instale o Poetry](https://python-poetry.org/docs/#installation) de acordo com as recomendações do seu sistema operacional. Após isto, faça a [instalação do Docker](https://docs.docker.com/get-docker/) também de acordo com o seu SO.

Há uma configuração do Poetry que recomendamos que seja utilizada. Trata-se de espeficiar a configuraçao [`virtualenvs.in-project`](https://python-poetry.org/docs/configuration/#virtualenvsin-project-boolean) como `true` para que o ambiente virtual do Python seja criado no diretório _root_ da aplicação (`.venv`). Para isto, no abra um novo shell/terminal e execute:

```sh
poetry config virtualenvs.in-project true
```

> Você pode utilizar o comando `poetry config --list` para validar que a configuração mencionada anteriormente foi habilitada.

Clone este projeto (ou faça o _fork_ caso não tenha permissões de contribuição diretamente) e instale as dependências.

```sh
git clone https://github.com/drivr/api.git

cd ./api
poetry install
```

### Executando a aplicação

Para executar a aplicação, é necessário subir um novo container com o Postgres e executar as migrações. Para isto, entre no shell do ambiente virtual e execute:

```sh
poetry shell

sh ./scripts/docker.db.sh
alembic upgrade head
uvicorn drivr:app --reload

    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [12912] using statreload
    INFO:     Started server process [16156]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
```

### Executando testes unitários

Para executar os testes unitários não é necessário nem que nenhum container (do banco de dados) e nem que a aplicação esteja em execução. Basta executar o shell script dentro do ambiente virtual do Python:

```sh
poetry shell

sh ./scripts/test.unit.sh
```

### Executando os testes de integração

Para executar os testes de integração é necessário que o container do banco de dados de teste esteja em execução. Mas já deixamos um script pronto que cria o container, roda os testes e posteriormente remove o container criado. Para executar tudo isso, simplesmente execute o shell script dentro do ambiente virtual do Python:

```sh
poetry shell

sh ./scripts/docker.test.integration.sh
```
