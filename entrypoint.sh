#!/bin/sh

# applicate the migrations
alembic upgrade head

# run server
uvicorn --host 0.0.0.0 --port 8000 app.main:app
