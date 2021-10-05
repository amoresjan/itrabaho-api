# iTrabaho-api

## Setup

### Database

Install [PostgreSQL](https://www.postgresql.org/download/)

```sql
CREATE DATABASE itrabaho_db;
```

```sql
CREATE USER itrabaho WITH PASSWORD 'password';
```

```sql
GRANT ALL PRIVILEGES ON DATABASE "itrabaho_db" to itrabaho;
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

Activate Poetry

```bash
poetry shell
```

### Generate Data

Generate data from `data.json` (based on your local storage)

```bash
python3 manage.py dumpdata -e contenttypes -e auth.Permission -o data.json
```
