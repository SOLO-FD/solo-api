import pytest

from api.service import ProjectTagService

# from api.dto import (
#     ProjectTagCreateDTO,
# )
from api.repo import ProjectTagRepo
from api.domain import ProjectTagDomain
from api.utils import generate_id
from tests.factory.service import create_project_by_service, create_tag_by_service


class TestProjectServiceCase:
    async def _add_tag_to_project(self, session, project_id, tag_id):
        repo = ProjectTagRepo(session)

        return await repo.add_tag_by_id(project_id, tag_id)

    # === HAPPY tests following ===
    async def test_project_add_tag_by_id_by_service(
        self, session, new_project, new_tag
    ):
        # Arrange: Get owner_id
        owner_id = new_project.owner_id

        # Act: Add tag to project
        service = ProjectTagService(session)
        return_list = await service.add_tag_by_id(owner_id, new_project.id, new_tag.id)

        # Assert: Check if tag get added to project by repo
        repo = ProjectTagRepo(session)
        project_tag_list = await repo.list_by_project_id(new_project.id)
        tag_list = [item.tag for item in project_tag_list]

        # Assert: CHeck if the return is as expected type
        for item in return_list:
            assert isinstance(item, ProjectTagDomain)

        # Assert: Check if the added tag in repo
        assert new_tag in tag_list

    # async def test_project_add_tags_by_id_by_service(
    #     self, session, new_project, new_tag
    # ):
    #     # Arrange: Get owner_id
    #     owner_id = new_project.owner_id

    #     # Arrange: Create new tags
    #     NEW_TAGS = 7
    #     new_tags = []

    #     for _ in range(NEW_TAGS):
    #         new_tag = await create_tag_by_service(session, owner_id=owner_id)
    #         new_tags.append(new_tag)

    #     # Act: Add tag to project
    #     service = ProjectTagService(session)
    #     project_tag_dtos = [ ProjectTagCreateDTO(tag_id=t.id) for t in new_tags ]
    #     await service.add_tags_by_id(
    #         owner_id, new_project.id, project_tag_dtos
    #     )

    #     # Assert: Check if tag get added to project by repo
    #     repo = ProjectTagRepo(session)
    #     project_tag_list = await repo.list_by_project_id(new_project.id)
    #     tag_list = [item.tag for item in project_tag_list]

    #     # Assert: Check if the added tag in repo
    #     assert all(new_tag in tag_list for new_tag in new_tags)

    async def test_project_list_by_tag_id_by_service(
        self, session, new_project, new_tag
    ):
        # Arrange: Get owner_id
        owner_id = new_project.owner_id

        # Arrange: Add tag to project
        await self._add_tag_to_project(session, new_project.id, new_tag.id)

        # Act: Get projects by giving tag_id
        service = ProjectTagService(session)
        project_list = await service.list_by_tag_id(owner_id, new_tag.id)

        # Assert: Check if project got
        assert new_project in project_list

    async def test_project_list_by_project_id_by_service(
        self, session, new_project, new_tag
    ):
        # Arrange: Get owner_id
        owner_id = new_project.owner_id

        # Arrange: Add tag to project
        await self._add_tag_to_project(session, new_project.id, new_tag.id)

        # Act: Get tags by giving project_id
        service = ProjectTagService(session)
        project_tag_list = await service.list_by_project_id(owner_id, new_project.id)

        tag_list = [item.tag for item in project_tag_list]

        # Assert: Check if project got
        assert new_tag in tag_list

    async def test_project_remove_tag_by_id_by_service(
        self, session, new_project, new_tag
    ):
        # Arrange: Get owner_id
        owner_id = new_project.owner_id

        # Arrange: Add tag to project
        await self._add_tag_to_project(session, new_project.id, new_tag.id)

        # Act: Remove tag from project by giving tag_id
        service = ProjectTagService(session)
        project_tag_list = await service.remove_tag_by_id(
            owner_id, new_project.id, new_tag.id
        )

        tag_list = [item.tag for item in project_tag_list]

        # Assert: Check if project got
        assert new_tag not in tag_list

    # === SAD tests following ===
    async def test_project_add_tag_to_non_owned_project_by_id_by_service(
        self, session, new_tag
    ):
        # Arrange: Create non_owned project
        another_account_id = generate_id()
        new_project = await create_project_by_service(
            session, owner_id=another_account_id
        )

        # Arrange: Get owner_id
        owner_id = new_tag.owner_id

        # Act: Add tag to non-owned project should raise ValueError
        service = ProjectTagService(session)

        with pytest.raises(ValueError):
            await service.add_tag_by_id(owner_id, new_project.id, new_tag.id)

    async def test_project_add_non_owned_tag_by_id_by_service(
        self, session, new_project
    ):
        # Arrange: Create non_owned tag
        another_account_id = generate_id()
        new_tag = await create_tag_by_service(session, owner_id=another_account_id)

        # Arrange: Get owner_id
        owner_id = new_project.owner_id

        # Act: Add non-owned tag to project should raise ValueError
        service = ProjectTagService(session)

        with pytest.raises(ValueError):
            await service.add_tag_by_id(owner_id, new_project.id, new_tag.id)

    async def test_project_list_by_non_owned_tag_id_by_service(
        self, session, new_project, new_tag
    ):
        # Arrange: Get another account id
        owner_id = generate_id()

        # Arrange: Add tag to project
        await self._add_tag_to_project(session, new_project.id, new_tag.id)

        # Act: Get projects by giving non-owned tag_id should raise ValueError
        service = ProjectTagService(session)

        with pytest.raises(ValueError):
            await service.list_by_tag_id(owner_id, new_tag.id)

    async def test_project_list_by_non_owned_project_id_by_service(
        self, session, new_project, new_tag
    ):
        # Arrange: Get another account id
        owner_id = generate_id()

        # Arrange: Add tag to project
        await self._add_tag_to_project(session, new_project.id, new_tag.id)

        # Act: Get tags by giving non-owned project_id should raise ValueError
        service = ProjectTagService(session)

        with pytest.raises(ValueError):
            await service.list_by_project_id(owner_id, new_project.id)

    async def test_project_remove_non_owned_tag_by_id_by_service(
        self, session, new_project, new_tag
    ):
        # Arrange: Get another account id
        owner_id = generate_id()

        # Arrange: Add tag to project
        await self._add_tag_to_project(session, new_project.id, new_tag.id)

        # Act: Remove tag from project by giving non-owned tag_id should raise ValueError
        service = ProjectTagService(session)
        with pytest.raises(ValueError):
            await service.remove_tag_by_id(owner_id, new_project.id, new_tag.id)
