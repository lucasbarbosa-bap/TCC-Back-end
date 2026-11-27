# Sinapse — Back-end API 🌟

API REST desenvolvida em **Django** para gerenciamento de usuários, postagens, comentários e interações, com autenticação via **JWT**, hospedagem no **Render**, Banco de dados no **Supabase** e armazenamento de mídias no **Cloudinary**.

🌐 **API em produção (Base URL):** <https://sinapse.onrender.com>

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

### Configure as variáveis de ambiente (`.env`)
Crie um arquivo `.env` na raiz do projeto com as credenciais do banco de dados, `DATABASE_URL` e chaves do Cloudinary.

### Ative o Banco de Dados (Docker compose): 
``` bash
docker compose up -d 
``` 
>**Nota**: É necessário ter o Docker instalado na sua máquina para rodar o banco de dados. [Clique aqui para acessar a página oficial de download.](https://docs.docker.com/get-started/get-docker/)

### Rode as migrations e inicie o servidor
```bash
python manage.py migrate
python manage.py runserver
```

### Ligar o Servidor do Django:
```
python manage.py runserver
```

Logo apos executar o comando acima, acesse <http://127.0.0.1:8000/> para confirmar se o servidor está rodando (você verá a tela inicial de sucesso do Django).

Para acessar o painel de controle do banco de dados, acesse <http://127.0.0.1:8000/admin>.

## 🔐 Autenticação

Rotas marcadas com 🔒 exigem o envio do token JWT obtido no login através do cabeçalho HTTP:

```http
Authorization: Bearer <seu_token_jwt>
```

---

## 📌 Documentação das Rotas

### Usuários e Autenticação

| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `POST` | `api/auth/login/` | Público | Autentica o usuário e retorna o token JWT |
| `POST` | `api/registar/` | Público | Cadastra um novo usuário |
| `GET` | `api/usuarios/<int:id>/` | Público | Retorna dados e postagens do usuário |
| `PATCH` / `PUT` | `api/usuarios/<int:id>/` | 🔒 Dono | Atualiza perfil (`username`, `biografia`, `avatar`) |
| `DELETE` | `api/usuarios/<int:id>/` | 🔒 Dono | Deleta a conta do usuário |
| `POST` | `api/usuarios/<int:id>/seguir/` | 🔒 Logado | Passa a seguir o usuário informado na URL |
| `DELETE` | `api/usuarios/<int:id>/seguir/` | 🔒 Logado | Deixa de seguir o usuário informado na URL |
| `GET` | `api/usuarios/<int:id>/seguidores/` | Público | Lista os seguidores do usuário |
| `GET` | `api/usuarios/<int:id>/seguindo/` | Público | Lista quem o usuário está seguindo |

<details>
<summary><strong>Ver detalhes de requisição e resposta (Usuários)</strong></summary>

* **`POST api/auth/login/`** (`JSON`)
  ```json
  {
    "username": "nome_de_usuario",
    "password": "senha"
  }
  ```
  *Retorna dados do usuário + `"token"` (`200 OK`) ou `"Credenciais inválidas"` (`401`).*

* **`POST api/registar/`** (`FormData`)
  * `username`, `email`, `password` (obrigatórios)
  * `avatar` (opcional — `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`)

* **`GET api/usuarios/<int:id>/`**
  ```json
  {
    "mensagem": {
      "id": 1,
      "username": "nome_legal",
      "avatar": "url_da_imagem",
      "biografia": "sou legal",
      "seguidores": 69,
      "seguindo": 24,
      "posts": []
    }
  }
  ```

* **`PATCH / PUT api/usuarios/<int:id>/`** (`FormData` ou `JSON`) — 🔒 *Exige token do próprio usuário*
  * `username`, `biografia`, `avatar` (opcionais, enviar ao menos um)

* **`POST / DELETE api/usuarios/<int:id>/seguir/`** — 🔒 *Exige token (não necessita de corpo na requisição)*
  * `POST` (`201 Created`): `{"mensagem": "Usuário seguido com sucesso."}` *(bloqueia auto-seguir ou duplicidade retornando `400`)*
  * `DELETE` (`200 OK`): `{"mensagem": "usuário deseguido com sucesso."}` *(retorna `400` se não estiver seguindo)*

* **`GET api/usuarios/<int:id>/seguidores/`**
  ```json
  {
    "seguidores": [
      {
        "id": 2,
        "username": "nome_do_usuario",
        "avatar": "url_da_imagem"
      }
    ]
  }
  ```

* **`GET api/usuarios/<int:id>/seguindo/`**
  ```json
  {
    "seguindo": [
      {
        "id": 3,
        "username": "outro_usuario",
        "avatar": "url_da_imagem"
      }
    ]
  }
  ```

</details>

---

### Postagens

| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `GET` | `api/postagem/` | Público | Lista todas as postagens (mais recentes primeiro) |
| `POST` | `api/postagem/` | 🔒 Logado | Cria uma nova postagem (autor extraído do token) |
| `GET` | `api/postagem/<int:id>/` | Público | Detalha uma postagem específica |
| `PATCH` / `PUT` | `api/postagem/<int:id>/` | 🔒 Autor | Edita `titulo` e/ou `conteudo` da postagem |
| `DELETE` | `api/postagem/<int:id>/` | 🔒 Autor | Remove a postagem |

<details>
<summary><strong>Ver detalhes de requisição e resposta (Postagens)</strong></summary>

* **`GET api/postagem/`**
  ```json
  {
    "Postagens": [
      {
        "id": 1,
        "titulo": "titulo legal",
        "autor": {
          "id": 1,
          "nome": "nome legal",
          "avatar": "url_da_imagem"
        },
        "data_criacao": "2026-11-26T12:00:00Z",
        "conteudo": "conteudo do post",
        "midia": ["url_da_midia_1"],
        "curtidas": 10,
        "compartilhamentos": 2,
        "comentarios": 5
      }
    ]
  }
  ```

* **`POST api/postagem/`** (`FormData`) — 🔒 *Exige token*
  * `titulo` (obrigatório), `conteudo` (obrigatório)
  * `midia` (opcional — até 10 arquivos, máx. 20MB cada: imagens `.jpg/.jpeg/.png/.gif/.webp` e vídeos `.mp4/.webm/.mov`)

* **`PATCH / PUT api/postagem/<int:id>/`** (`JSON` ou `FormData`) — 🔒 *Exige token do autor*
  * `titulo`, `conteudo` (opcionais, enviar ao menos um; não edita mídias)

</details>

---

### Comentários

| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `GET` | `api/comentario/<int:id_post>/` | Público | Lista comentários de um post (mais antigos primeiro) |
| `POST` | `api/comentario/<int:id_post>/` | 🔒 Logado | Cria comentário no post (autor extraído do token) |

<details>
<summary><strong>Ver detalhes de requisição e resposta (Comentários)</strong></summary>

* **`GET api/comentario/<int:id_post>/`**
  ```json
  {
    "Comentarios": [
      {
        "autor": {
          "id": 1,
          "nome": "nome legal",
          "avatar": "url_da_imagem"
        },
        "id": 1,
        "post_original": 26,
        "conteudo": "texto do comentário",
        "data_criacao": "2026-11-26T12:00:00Z",
        "midia": [],
        "curtidas": 3,
        "compartilhamentos": 0
      }
    ]
  }
  ```

* **`POST api/comentario/<int:id_post>/`** (`FormData`) — 🔒 *Exige token*
  * `conteudo` (obrigatório)
  * `midia` (opcional — até 5 imagens, máx. 5MB cada: `.jpg/.jpeg/.png/.gif/.webp`)

</details>

---

### Interações

| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `GET` | `api/interacao/` | Público | Lista interações (aceita filtros `?post=`, `?comentario=`, `?autor=`, `?tipo=`) |
| `POST` | `api/interacao/` | 🔒 Logado | Registra interação (`like` ou `share`) sem duplicidade |
| `DELETE` | `api/interacao/<int:id>/` | 🔒 Autor | Remove interação (descurtir / desfazer) |

<details>
<summary><strong>Ver detalhes de requisição e resposta (Interações)</strong></summary>

* **`POST api/interacao/`** (`JSON`) — 🔒 *Exige token*
  ```json
  {
    "post": 26,
    "comentario": null,
    "tipo": "like"
  }
  ```
  *Enviar apenas `post` **ou** `comentario`. Tipos aceitos: `"like"` e `"share"`.*

* **Resposta (`201 Created`):**
  ```json
  {
    "mensagem": "Interação criada com sucesso!",
    "id": 1,
    "interacao": {
      "id": 1,
      "autor_id": 1,
      "post_id": 26,
      "comentario_id": null,
      "tipo": "like"
    }
  }
  ```

</details>