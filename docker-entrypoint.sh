if [ "$MODE" = "local" ] ; then python manage.py migrate && python manage.py runserver_plus 0.0.0.0:80 ; fi
if [ "$MODE" = "testing" ] ; then pytest --junit-xml=test-report.xml --cov=helpers --cov-report=html --cov-report=term tests ; fi
if [ "$MODE" = "dev" ] || [ "$MODE" = "qa" ] || [ "$MODE" = "prod" ] ; then python manage.py migrate && uvicorn --host=0.0.0.0 --port 80 project.asgi:application ; fi
