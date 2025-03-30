# This file tells Render.com how to start my app in production

uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1 --no-access-log --limit-concurrency 100 --timeout-keep-alive 30