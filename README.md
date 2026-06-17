# Task-Manager
Task Manager in FastAPI

## Live API
https://task-manager-f13j.onrender.com/docs

Note: Free tier spins down after inactivity. First request may take 30-60 seconds.

## Endpoints
POST /auth/register

POST /auth/login

POST /tasks

GET  /tasks?status=todo&priority=high

GET  /tasks/{id}

PUT  /tasks/{id}

PATCH /tasks/{id}/status

DELETE /tasks/{id}
