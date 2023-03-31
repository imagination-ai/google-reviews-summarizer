 cd /applications || exit

export PYTHONUNBUFFERED=TRUE

python3 -m gunicorn -k uvicorn.workers.UvicornWorker \
  --workers 1 \
  --bind "${APP_HOST:-0.0.0.0}:${APP_PORT:-8000}" \
  --timeout 600 \
  --log-level info \
  --access-logfile - \
  --log-file - \
   summarizer.main:app \
  "$@"