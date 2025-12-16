
# Traffic Monitor API

API REST para monitorização de tráfego rodoviário, desenvolvida com Django Rest Framework.

Este projeto foi desenvolvido como exercício técnico para a Ubiwhere.
## Descrição

Esta API permite gerir segmentos de estrada e leituras de velocidade média, calculando automaticamente a intensidade do tráfego com base na velocidade registada.

### Caracterização da Intensidade

| Velocidade Média | Intensidade |
|------------------|-------------|
| ≤ 20 km/h | Elevada |
| > 20 e ≤ 50 km/h | Média |
| > 50 km/h | Baixa |

## Funcionalidades

- ✅ CRUD completo para segmentos de estrada
- ✅ CRUD completo para leituras de velocidade
- ✅ Cálculo automático da intensidade do tráfego
- ✅ Sistema de permissões (Admin vs Anónimo)
- ✅ Autenticação por Token
- ✅ Documentação através do Swagger
- ✅ Filtros por segmento de estrada
- ✅ Contador de leituras por segmento

## Tecnologias

- Python 3.13.3
- Django 6.0
- Django REST Framework
- PostgreSQL
- drf-spectacular (Swagger/OpenAPI)

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/Ricardo-Antunes0/traffic-monitor.git
cd traffic-monitor-api
```

### 2. Criar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Cria uma base de dados PostgreSQL:

```sql
CREATE DATABASE traffic_monitor;
```

Edita `config/settings.py` com as tuas credenciais:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'traffic_monitor',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Aplicar migrations

```bash
python manage.py migrate
```

### 6. Criar superuser

```bash
python manage.py createsuperuser
```

Preenche:
- Username: `admin`
- Password: `admin` (ou outra à escolha)

### 7. Importar dataset

```bash
python manage.py import_data
```

Logs a serem vistos:
```
Importação concluída!
Segmentos criados: 5943
Leituras criadas: 5943
```

### 8. Iniciar servidor

```bash
python manage.py runserver
```

Aceder a: http://127.0.0.1:8000

## Autenticação

### Obter Token

1. Aceder ao Django Admin: http://127.0.0.1:8000/admin/
2. Login com o superuser criado
3. Ir a **"Tokens"** → **"Add Token +"**
4. Selecionar o utilizador **admin**
5. Guardar (Django gera o token automaticamente)
6. Copiar o token gerado

### Usar Token na API

**No Swagger:**
1. Clicar em **"Authorize"**
2. Escrever: `Token TOKEN_AQUI`
3. Clicar **"Authorize"**


## Documentação da API

### Swagger
http://127.0.0.1:8000/api/docs/

### Schema OpenAPI (JSON)
http://127.0.0.1:8000/api/schema/

## Permissões

| Tipo de Utilizador | Operações Permitidas |
|-------------------|---------------------|
| **Administrador** | Create, Read, Update, Delete |
| **Anónimo** | Read|

## Principais Endpoints

### Segmentos de Estrada

- `GET /api/segments/` - Listar todos os segmentos
- `GET /api/segments/{id}/` - Detalhes de um segmento
- `POST /api/segments/` - Criar segmento (Admin)
- `PUT /api/segments/{id}/` - Editar segmento (Admin)
- `DELETE /api/segments/{id}/` - Apagar segmento (Admin)

### Leituras de Velocidade

- `GET /api/readings/` - Listar todas as leituras
- `GET /api/readings/{id}/` - Detalhes de uma leitura
- `GET /api/readings/?road_segment=1` - Filtrar por segmento
- `POST /api/readings/` - Criar leitura (Admin)
- `PUT /api/readings/{id}/` - Editar leitura (Admin)
- `DELETE /api/readings/{id}/` - Apagar leitura (Admin)

## Exemplos de Uso

### Listar segmentos (Anónimo)

```bash
curl http://127.0.0.1:8000/api/segments/
```

### Criar segmento (Admin)

```bash
curl -X POST http://127.0.0.1:8000/api/segments/ \
  -H "Authorization: Token O_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "longitude_start": 103.946,
    "latitude_start": 30.750,
    "longitude_end": 103.956,
    "latitude_end": 30.745,
    "length": 100.1
  }'
```

### Criar leitura (Admin)

```bash
curl -X POST http://127.0.0.1:8000/api/readings/ \
  -H "Authorization: Token O_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "road_segment": 1,
    "average_speed": 25.5,
    "timestamp": "2024-12-17T14:00:00Z"
  }'
```

## Testes

Para executar os testes (Parte 2 - opcional):

```bash
python manage.py test
```

## Estrutura do Projeto

```
traffic-monitor/
├── config/                 # Configurações do Django
│   ├── settings.py
│   └── urls.py
├── traffic_monitor/        # App principal
│   ├── models.py          # Models (RoadSegment, SpeedReading)
│   ├── serializers.py     # Serializers DRF
│   ├── views.py           # ViewSets
│   ├── permissions.py     # Permissões customizadas
│   ├── urls.py            # URLs da app
│   └── management/
│       └── commands/
│           └── import_data.py  # Comando de importação
├── data/
│   └── traffic_speed.csv  # Dataset
├── manage.py
├── requirements.txt
└── README.md
```

## Notas de Implementação

- A intensidade do tráfego é **calculada dinamicamente** (não é guardada na db).
- Cada segmento tem uma leitura inicial após importação.
- Não foi usado o campo ID do CSV; os IDs são gerados automaticamente pelo PostgreSQL, evitando problemas com a sequência ou conflitos de chave.
- **Serialização de segmentos:**
  - **Detalhada:** Para um segmento específico, devolvo os dados do segmento e também a última leitura e o número total de leituras.
  - **Leve:** Para a lista de todos os segmentos, devolvo apenas os campos essenciais para ser mais rápida.



