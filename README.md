# Computação UFCG

## Instale e configure o PostgreSQL
```
sudo apt-get install -y postgresql
sudo su postgres

export computacao_ufcg_user=computacao_ufcg_user
export computacao_ufcg_password=computacao_ufcg_password
export computacao_ufcg_db_name=computacao_ufcg_db_name

psql -c "CREATE USER computacao_ufcg_user WITH PASSWORD 'computacao_ufcg_password';"
psql -c "CREATE DATABASE computacao_ufcg_db_name OWNER computacao_ufcg_user;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE computacao_ufcg_db_name TO computacao_ufcg_user;"
exit
```

## Instale o psycopg2
```
pip install Flask psycopg2-binary
```

## Clone o repositório
```
git clone https://github.com/cilasmarques/ufcg-comp-app-api
cd ufcg-comp-app-api
```

## Crie um ambiente virtual e instale as dependencia
* Instale o python venv
  ```
  sudo apt-get install python3.8
  ```

* Crie o ambiente virtual
  ```
  python3 -m venv computacaoUFCG
  ```

* Inicie o ambiente e instale as dependencias
  ```
  source computacaoUFCG/bin/activate
  pip install -r requirements.txt
  ```

## Inicie o projeto
  ```
  python3 run.py
  ```