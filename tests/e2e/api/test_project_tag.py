from dataclasses import asdict
from fastapi.encoders import jsonable_encoder

from src.api.repo import (
    ProjectTagRepo,
    TagRepo,
    ProjectRepo,
)
from tests.factory.repo import (
    create_tag,
    create_project_with_attachments,
)


class TestTagAPICase:
    async def test_add_tag_to_project_by_api(
        self, session, client, default_header, default_project, default_tag
    ):
        # Act: Add tag to project resource
        response = client.put(
            f"/v1/projects/{default_project.id}/tags/{default_tag.id}",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check if the tag add to the db
        repo = ProjectTagRepo(session)
        db_project_tags = await repo.list_by_project_id(default_project.id)
        db_tags = [item.tag for item in db_project_tags]

        assert default_tag in db_tags

    async def test_get_tags_in_project_by_api(
        self, session, client, default_header, default_project, default_account_id
    ):
        # Arrange: Get project ID
        project_id = default_project.id

        # Arrange: Create tags and add it to project
        NEW_TAGS = 7
        new_tags_dict = {}

        tag_repo = TagRepo(session)
        project_tag_repo = ProjectTagRepo(session)

        for _ in range(NEW_TAGS):
            new_tag = await create_tag(tag_repo, owner_id=default_account_id)
            new_tags_dict[new_tag.id] = jsonable_encoder(asdict(new_tag))
            await project_tag_repo.add_tag_by_id(project_id, new_tag.id)

        # Act: Get tags by project ID
        response = client.get(
            f"/v1/projects/{default_project.id}/tags/",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check if the all new tag add to db could be returned
        return_tags_dict = {item["tag"]["id"]: item["tag"] for item in response.json()}

        for tag_id, tag_dict in new_tags_dict.items():
            return_tag = return_tags_dict[tag_id]
            for key, value in return_tag.items():
                assert tag_dict[key] == value

    async def test_get_projects_in_tag_by_api(
        self, session, client, default_header, default_tag, default_account_id
    ):
        # Arrange: Get tag ID
        tag_id = default_tag.id

        # Arrange: Create projects and add the default tag to them
        NEW_PROJETS = 7
        new_projects_dict = {}

        project_repo = ProjectRepo(session)
        project_tag_repo = ProjectTagRepo(session)

        for _ in range(NEW_PROJETS):
            new_project = await create_project_with_attachments(
                project_repo, owner_id=default_account_id
            )
            new_projects_dict[new_project.id] = jsonable_encoder(asdict(new_project))
            await project_tag_repo.add_tag_by_id(new_project.id, tag_id)

        # Act: Get projects by tag ID
        response = client.get(
            f"/v1/tags/{default_tag.id}/projects/",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check if the all new tag add to db could be returned
        return_projects_dict = {project["id"]: project for project in response.json()}

        for project_id, project_dict in return_projects_dict.items():
            return_project = return_projects_dict[project_id]
            for key, value in return_project.items():
                assert project_dict[key] == value

    async def test_remove_tag_from_project_by_api(
        self,
        session,
        client,
        default_header,
        default_project,
        default_tag_add_to_project,
    ):
        # Act: Remove tag from project resource
        response = client.delete(
            f"/v1/projects/{default_project.id}/tags/{default_tag_add_to_project.id}",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 204

        # Assert: Check if the tag add to the db
        repo = ProjectTagRepo(session)
        db_project_tags = await repo.list_by_project_id(default_project.id)
        db_tags = [item.tag for item in db_project_tags]

        assert default_tag_add_to_project not in db_tags
