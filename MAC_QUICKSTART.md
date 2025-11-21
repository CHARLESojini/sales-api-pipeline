# 🚀 Mac Quick Start

## Step-by-Step Setup

### 1. Install PostgreSQL
```bash
brew install postgresql@14
brew services start postgresql@14
```

### 2. Create Database
```bash
createdb sales_analytics
psql -d sales_analytics -f schema.sql
```

### 3. Configure
```bash
cp .env.example .env
open -e .env
# Change DB_USER to your username (run: whoami)
# Save
```

### 4. Install Packages
```bash
pip3 install -r requirements.txt
```

### 5. Test
```bash
python3 test_system.py
```

### 6. Run Pipeline
```bash
python3 run_pipeline.py
```

### 7. Start API
```bash
python3 api/api_service.py
```

### 8. Test API
Open: http://localhost:8000/docs

## Done! 🎉
