# Computação UFCG

## Instale o MongoDB
```
curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install mongodb-org
sudo systemctl start mongod.service
sudo systemctl status mongod
sudo systemctl enable mongod
```

## Clone o repositório
```
git clone https://github.com/cilasmarques/ufcg-comp-app-api
cd ufcg-comp-app-api
```

## Crie um ambiente virtual e instale as dependencia
* Instale o python venv
  ```
  apt install python3.10-venv
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