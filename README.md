# iTrabaho-api

## Setup

### Database

Install [PostgreSQL](https://www.postgresql.org/download/)

```sql
CREATE DATABASE itrabaho_db;
```

```sql
CREATE USER postgres WITH PASSWORD 'password';
```

```sql
GRANT ALL PRIVILEGES ON DATABASE "itrabaho_db" to postgres;
```

```sql
\q
```

```bash
cd path/to/itrabaho-api
```

```bash
python manage.py migrate
```

```bash
python manage.py loaddata data.json
```

### Dependencies

Install [Poetry](https://python-poetry.org/docs/#installation)

```bash
cd path/to/itrabaho-api
```

```bash
poetry install
```
