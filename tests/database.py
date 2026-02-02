# from fastapi.testclient import TestClient
# import pytest

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from app.main import app

# from app.config import settings
# from app.database import get_db, Base

# # TestClient(
# #     app,
# #     base_url="http://testserver",
# #     raise_server_exceptions=True,
# #     root_path="",
# #     backend="asyncio",
# #     backend_options=None,
# #     cookies=None,
# #     headers=None,
# #     follow_redirects=True,
# #     client=("testclient", 50000),
# # )

# # SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost:5432/fastapi_test_db'

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# # client = TestClient(app)


# @pytest.fixture(scope="function")
# def session():
#     print("my session fixture ran")
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture(scope="function")
# def client(session):
#     def overrid_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = overrid_get_db
#     yield TestClient(app)
    