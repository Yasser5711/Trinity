-To execute tests must be in the /app folder then execute this command

```python
pytest
```

pytest tests/test_my_routes.py
1- Verify Lint with Flake8
flake8 .
2- Format with Black
black .
3- Sort imports with isort
isort .

```bash
isort . && black .
```

generate migrations
alembic revision --autogenerate -m "msg"

apply migrations
alembic upgrade head
