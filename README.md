# Task Manager API
 
API REST para gerenciamento de tarefas, desenvolvida com Django e Django REST Framework. Eu estou desenvolvendo esse projeto com fins de aprendizado e adquirir experiencias, essa é a primeira sprint da aplicação que está em desenvolvimento

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
cd task_manger_API
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

## 🔐 Autenticação
 
A API utiliza **JWT**. Para acessar os endpoints protegidos, é necessário incluir o token no header da requisição:
 
```
Authorization: Bearer <seu_token>
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
 
Por enquanto ele tem testes basicos para criação de tarefas, usando o framework de testes nativo do Django 
 
Para ver os testes no terminal rode:
 
```bash
python manage.py test apps.tasks.tests.test_tasks_api
```
 
---

##  Próximas Melhorias 
 
- [ ] Migrar testes para **pytest + pytest-django**
- [ ] Adicionar documentação automática com **Swagger (drf-spectacular)**
- [ ] Adicionar campo de **data de vencimento** nas tarefas
- [ ] Implementar **categorias/tags** para as tarefas
- [ ] Configurar **CI/CD com GitHub Actions**
- [ ] Preparar ambiente de produção dedicado
- [ ] Frontend para melhor vizualização

---

##  Autor
 
Feito por **Daniel Donizeti**  
[LinkedIn](https://www.linkedin.com/in/daniel-donizeti-853320239)

## Link da API
[API](https://task-manager-api-qesq.onrender.com)