# import pytest
# from app.models import User
# from app.repository.base_repository import BaseRepository
# @pytest.mark.asyncio
# async def test_read_by_id(async_session, user):
#     repo = BaseRepository(session_factory=async_session, model=User)
#     result = await repo.read_by_id(id=user.id, eager=False)
#     assert result is not None
#     assert result.created_at == user.created_at
#     assert result.updated_at == user.updated_at
#     assert result.email == user.email
#     assert result.username == user.username
#     assert result.password == user.password
# # from sqlalchemy.orm import Session
# # from app.core.exceptions import DuplicatedError, NotFoundError
# # @pytest.mark.asyncio
# # async def test_read_by_options(async_session, user):
# #     repo = BaseRepository(session_factory=async_session, model=User)
# #     # Create test data if necessary
# #     # Call the method being tested
# #     result = await repo.read_by_options(schema=your_schema_object, eager=False)
# #     # Perform assertions
# #     assert isinstance(result, dict)
# #     assert "founds" in result
# #     assert "search_options" in result
# # @pytest.mark.asyncio
# # async def test_create(async_session):
# #     repo = BaseRepository(session_factory=async_session, model=YourModel)
# #     # Create test schema object
# #     # Call the method being tested
# #     result = await repo.create(schema=your_schema_object)
# #     # Perform assertions
# #     assert result is not None
# # Similar tests can be written for other methods like update, update_attr, whole_update, and delete_by_id
