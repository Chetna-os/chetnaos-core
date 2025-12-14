# ChetnaOS

## Overview
ChetnaOS is an AGI-ready cognitive operating system runtime built with FastAPI. It provides a cognitive processing engine with intent detection, priority routing, workflow execution, and reflection capabilities.

## Project Structure
- `backend/` - FastAPI backend with AGI components
  - `app.py` - Main FastAPI application
  - `orchestrator/` - Brain router, intent detection, priority engine
  - `reflection/` - Dharma net and reflection engine
  - `workflows/` - Sales, lead, and custom workflow handlers
  - `monitoring/` - Health checks and metrics
- `frontend/` - Static HTML frontend
  - `index.html` - Simple web interface for the cognitive runtime
- `demos/` - Demo applications
- `docs/` - Documentation

## Running the Application
The app runs on port 5000 using uvicorn:
```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5000
```

## API Endpoints
- `GET /` - Serves the frontend
- `GET /health` - Health check endpoint
- `POST /process` - Main cognitive processing endpoint
  - Body: `{"input": "your request", "context": {}}`

## Architecture
1. Input received via `/process` endpoint
2. BrainRouterAdvanced orchestrates:
   - Intent Detection (sales, goal, support, lead, chat)
   - Priority Scoring
   - Dharma Validation (ethical checks)
   - Workflow Execution
   - Reflection Loop

## Dependencies
- FastAPI
- Pydantic
- Uvicorn
