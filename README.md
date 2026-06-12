# Task Manager API
 
API REST para gerenciamento de tarefas, desenvolvida com Django e Django REST Framework. Eu estou desenvolvendo esse projeto com fins de aprendizado e adquirir experiencias, essa é a primeira sprint da aplicação que está em desenvolvimento

## Link da API
[API](https://task-manager-ag0w.onrender.com)

## Link do Front End
[Front](https://task-manager-front-kxgv.onrender.com)
---

##  Tecnologias Utilizadas
 
- **Python 3.12**
- **Django 6.0.4**
- **Django REST Framework 3.17.1**
- **PostgreSQL 15**
- **JWT Authentication**(djangorestframework-simplejwt)
- **Docker & Docker Compose**
- **Gunicorn**

---
 
##  Como Rodar o Projeto
 
### Pré-requisitos
 
- [Python]() 3.11+
- [Docker](https://www.docker.com/) instalado
- [Docker Compose](https://docs.docker.com/compose/) instalado
### Passo a passo
 
1. Clone o repositório:
```bash
git clone https://github.com/danieldonizeti/task_manger_API.git
cd task_manager_API
```
 
2. Crie o arquivo `.env` na raiz do projeto baseado no meu `.env.example`:
```env
SECRET_KEY=sua_chave
DEBUG=True
DATABASE_URL=postgresql://user:password@your_host:db_name
```

3. Suba os containers:
```bash
docker-compose up --build
```
 
4. Em outro terminal, rode as migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. A API estará disponível em:

`API: http://localhost:8000/api/`
`admin: http://localhost:8000/admin/`

Para criar um superusuario, no terminal rode este comando

```bash
docker-compose exec web python manage.py createsuperuser
```

## 🔐 Autenticação JWT

A API utiliza autenticação baseada em **JWT (JSON Web Token)** com dois tokens:

- **Access Token** → enviado em toda requisição no header `Authorization: Bearer <token>`. Tem curta duração
- **Refresh Token** → usado para renovar o access token sem precisar logar novamente. Tem longa duração

### Fluxo de autenticação

1. Usuário faz login em `POST /api/auth/login/` e recebe os dois tokens
2. O access token é enviado em toda requisição protegida
3. Quando o access token expira, o cliente usa `POST /api/auth/refresh/` para obter um novo
4. Quando o refresh token expira, o usuário precisa fazer login novamente

Para acessar endpoints protegidos:
```http
Authorization: Bearer <seu_access_token>
```
 
---

## 📌 Endpoints
 
### Autenticação
 
| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/api/users` | Registro de novo usuário 
| POST | `/api/auth/login/` | Login — obtém access e refresh token
| POST | `/api/auth/refresh/` | Renova o access token

### Tarefas
 
| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/api/tasks/` | Lista todas as tarefas do usuário logado
| POST | `/api/tasks/` | Cria uma nova tarefa
| GET | `/api/tasks/{id}/` | Detalha uma tarefa
| PUT | `/api/tasks/{id}/` | Atualiza uma tarefa completamemte
| PATCH | `/api/tasks/{id}/` | Atualiza parcialmente uma tarefa
| DELETE | `/api/tasks/{id}/` | Remove uma tarefa

### Filtros disponíveis
 
Os filtros que implementei:
 
```
GET /api/tasks/?status=pendente
GET /api/tasks/?priority=alta   (baixa, media e alta ou 1,2 e 3)
GET /api/tasks/?status=em progresso&ordering=priority
```

---
 
##  Modelo das Tarefas
 
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `title` | string | Título da tarefa |
| `description` | string | Descrição detalhada |
| `status` | string | Status da tarefa (ex: `pendente`, `concluida`) |
| `priority` | string | Prioridade (ex: `baixa, 1`, `media, 2`, `alta, 3`) |
| `user` | FK User | Usuário dono da tarefa |
| `created_at` | datetime | Data de criação (automática) |
| `updated_at` | datetime | Data da última atualização (automática) |
 
---

## 🧪 Testes
Testes feitos com pytest com um coverage de 90%

Para ver os testes no terminal rode:
 
```bash
python pytest
```
 
---

##  Algumas das próximas Melhorias 
 
- [ ] Adicionar documentação automática com **Swagger (drf-spectacular)**
- [ ] Configurar **CI/CD com GitHub Actions**

---

##  Autor

Feito por **Daniel Donizeti**  
[LinkedIn](https://www.linkedin.com/in/daniel-donizeti-853320239)
