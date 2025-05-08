class TestRootAPICase:
    def test_root_by_api(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "SOLO API Endpoints is health!"}
