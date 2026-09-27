# TCC em progresso 🌟

## Para rodar:

### Clone o repositório:
``` bash
git clone https://github.com/lucasbarbosa-bap/TCC-Back-end.git

cd TCC-Back-end
```

### Crie o ambiente virtual e ative:

***Windows:***
``` powershell
py -m venv venv

venv\Scripts\Activate.ps1
```

***Mac ou Linux:***

``` bash
python3 -m venv venv

source venv/bin/activate
```


### Instale as bibliotecas:
``` bash
pip install -r requirements.txt
```

### Ative o Banco de Dados (Docker compose): 
``` bash
docker compose up -d 
``` 
>**Nota**: É necessário ter o Docker instalado na sua máquina para rodar o banco de dados. [Clique aqui para acessar a página oficial de download.](https://docs.docker.com/get-started/get-docker/)

### Ligar o Servidor do Django:
```
python manage.py runserver
```

Logo apos executar o comando acima, acesse <http://127.0.0.1:8000/> para confirmar se o servidor está rodando (você verá a tela inicial de sucesso do Django).

Para acessar o painel de controle do banco de dados, acesse <http://127.0.0.1:8000/admin>.