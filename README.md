# AI Investment Advisor

An application that helps investors and business owners to find promising business opportunities in university graduation projects using AI-powered analysis and vector search.

## What it does

This tool analyzes university student projects and identifies which ones have commercial potential. Investors can ask questions like "Show me projects with farm management potential" and get detailed business analysis with market opportunities, revenue models, and investment recommendations.

## Demo Video

https://www.youtube.com/watch?v=oWTKxfpSTA8

## ScreenShots
![chat-interface](https://github.com/user-attachments/assets/0b55e855-2549-4788-8471-31cfcde778dc)

## Quick Start

1. **Install requirements**
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
   pip install langchain-huggingface together pgvector
   ```

2. **Set up environment variables** (create `.env` file)
   ```
   db_user=your_username
   db_password=your_password  
   db_host=localhost
   db_port=5432
   db_name=your_database
   togetherAPI=your_together_ai_key
   ```

3. **Set up PostgreSQL with pgvector**
   ```sql
   CREATE EXTENSION vector;
   ```

4. **Run the app**
   ```bash
   python main.py
   ```

Server runs at `http://localhost:8000`

## API Usage

**Add a project:**
```bash
curl -X POST "http://localhost:8000/v1/add-project" \
-H "Content-Type: application/json" \
-d '{
  "title": "Smart Farm Monitor",
  "description": "IoT sensors for crop monitoring",
  "supervisor": "Dr. Smith",
  "tools": ["Python", "IoT", "React"],
  "team_members": ["Alice", "Bob"],
  "year": 2024
}'
```

**Ask investment questions:**
```bash
curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"query": "What farm management projects do you have?"}'
```

## How it works

1. Projects are stored with vector embeddings based on their descriptions
2. When you ask a question, the system finds similar projects using vector search
3. An AI model (Llama 3.3) analyzes the projects and provides investment advice
4. You get a detailed response with market analysis, business potential, and next steps

## Key Features

- Vector similarity search to find relevant projects
- AI-powered investment analysis
- RESTful API for easy integration
- PostgreSQL database with vector indexing
- Professional investment advisor responses

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL + pgvector
- **AI**: HuggingFace embeddings + Together AI (Llama 3.3)
- **Search**: Vector cosine similarity
