# celery-worker

rm build/ celery_worker.egg-info dist -Rf
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/* --verbose