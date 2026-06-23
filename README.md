README ko aise likho ki recruiter ko lage ye actual production-level project hai.

---

# AI CRM Assistant

**AI-Powered CRM Automation Platform built with FastAPI, LangChain, PostgreSQL, and LLMs**

AI CRM Assistant is a full-stack AI application that automates customer support and CRM workflows using Large Language Models (LLMs), agent-based tool calling, and conversational memory. The system can classify customer queries, draft responses, create support tickets, fetch order information, and perform CRM actions through natural language conversations.

---

## Features

### AI-Powered Customer Support

- Customer query classification
- Automated response generation
- Intent detection
- Multi-turn conversations
- Context-aware responses

### Agent-Based CRM Actions

The assistant can perform CRM operations through tool calling:

- Create support tickets
- Fetch order information
- Retrieve customer details
- Update ticket status
- Send follow-up messages
- Escalate support requests

### Conversational Memory

- Session-based chat history
- Context retention across conversations
- Personalized customer interactions
- Long-running conversation support

### CRM Dashboard

- Customer management
- Ticket management
- Conversation history
- Analytics dashboard
- User authentication

---

## Architecture

```text
┌──────────────┐
│   Next.js    │
│   Frontend   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   FastAPI    │
│   Backend    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  LangChain   │
│    Agent     │
└──────┬───────┘
       │
 ┌─────┼─────┐
 ▼     ▼     ▼
Orders Tickets Customers
Tools   Tools   Tools
       │
       ▼
┌──────────────┐
│ PostgreSQL   │
└──────────────┘
```

---

## Tech Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- ShadCN UI
- React Query

### Backend

- FastAPI
- Python
- SQLAlchemy
- PostgreSQL
- JWT Authentication

### AI Layer

- OpenAI API / Gemini API
- LangChain
- Tool Calling
- Conversation Memory
- Prompt Engineering

### DevOps

- Docker
- Docker Compose
- GitHub Actions
- Nginx

---

## Core Workflow

```text
User Message
      │
      ▼
Intent Detection
      │
      ▼
LangChain Agent
      │
      ▼
Tool Selection
      │
      ▼
CRM Action
      │
      ▼
LLM Response
      │
      ▼
User
```

---

## Database Schema

### Users

```sql
id
name
email
password
created_at
```

### Conversations

```sql
id
user_id
title
created_at
```

### Messages

```sql
id
conversation_id
role
content
created_at
```

### Tickets

```sql
id
customer_id
title
status
priority
created_at
```

### Orders

```sql
id
customer_id
amount
status
created_at
```

---

## API Endpoints

### Authentication

```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Chat

```http
POST /api/chat
GET  /api/conversations
GET  /api/conversations/:id
```

### Tickets

```http
POST /api/tickets
GET  /api/tickets
PATCH /api/tickets/:id
```

### Orders

```http
GET /api/orders/:id
```

---

## Example Prompts

```text
Where is my order #1234?
```

```text
Create a high priority ticket for payment failure.
```

```text
Show all pending support tickets.
```

```text
Send a follow-up email to the customer.
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/as-ga/ai-crm-assistant.git
cd ai-crm-assistant
```

### Backend

```bash
cd backend

python -m venv venv

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

### Docker

```bash
docker-compose up --build
```

---

## Future Improvements

- Multi-agent architecture
- RAG-based company knowledge integration
- Voice support
- WhatsApp integration
- Email automation
- Analytics and reporting
- Fine-tuned support models
