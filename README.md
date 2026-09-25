---V2 Architecture---
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                             │ Question
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │   Application   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Network       │
                    │   Context       │
                    └────────┬────────┘
                             │
                             │ prompt + data
                             ▼
                    ┌─────────────────┐
                    │    OpenAI       │
                    │      LLM        │
                    └────────┬────────┘
                             │
                             │ answer
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    └────────┬────────┘
                             │
                             ▼
                           User

--- V3 Flow ---
User
 ↓
FastAPI
 ↓
Gemini
 ↓
Function Call
 ↓
Tool Registry
 ↓
Python Tool
 ↓
Network Data
 ↓
Function Response
 ↓
Gemini
 ↓
Final Answer