import json
import pytest


class TestGetCategories:
    """Tests for GET /categories"""

    def test_get_all_categories_empty(self, client):
        """Happy path: returns empty list when no categories exist."""
        response = client.get('/categories')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_all_categories_with_data(self, client):
        """Happy path: returns all categories."""
        # Create two categories
        client.post('/categories', json={'name': 'Electronics', 'description': 'Electronic devices'})
        client.post('/categories', json={'name': 'Clothing', 'description': 'Fashion items'})

        response = client.get('/categories')
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]['name'] == 'Electronics'
        assert data[1]['name'] == 'Clothing'


class TestGetCategoryById:
    """Tests for GET /categories/<id>"""

    def test_get_category_by_id_success(self, client):
        """Happy path: returns category with its products."""
        create_resp = client.post('/categories', json={'name': 'Books', 'description': 'All books'})
        category_id = create_resp.get_json()['id']

        response = client.get(f'/categories/{category_id}')
        data = response.get_json()

        assert response.status_code == 200
        assert data['name'] == 'Books'
        assert data['description'] == 'All books'
        assert 'products' in data

    def test_get_category_not_found(self, client):
        """Error case: category does not exist."""
        response = client.get('/categories/999')
        data = response.get_json()

        assert response.status_code == 404
        assert 'error' in data
        assert data['error'] == 'Category not found'


class TestCreateCategory:
    """Tests for POST /categories"""

    def test_create_category_success(self, client):
        """Happy path: creates a category with valid data."""
        response = client.post('/categories', json={
            'name': 'Electronics',
            'description': 'Electronic gadgets and devices'
        })
        data = response.get_json()

        assert response.status_code == 201
        assert data['name'] == 'Electronics'
        assert data['description'] == 'Electronic gadgets and devices'
        assert 'id' in data

    def test_create_category_missing_name(self, client):
        """Error case: name field is missing."""
        response = client.post('/categories', json={
            'description': 'No name provided'
        })
        data = response.get_json()

        assert response.status_code == 400
        assert 'error' in data
        assert data['error'] == 'Category name is required'

    def test_create_category_empty_name(self, client):
        """Error case: name field is empty string."""
        response = client.post('/categories', json={
            'name': '',
            'description': 'Empty name'
        })
        data = response.get_json()

        assert response.status_code == 400
        assert 'error' in data

    def test_create_category_duplicate_name(self, client):
        """Error case: category with same name already exists."""
        client.post('/categories', json={'name': 'Electronics'})
        response = client.post('/categories', json={'name': 'Electronics'})
        data = response.get_json()

        assert response.status_code == 409
        assert 'error' in data
        assert 'already exists' in data['error']

    def test_create_category_no_json_body(self, client):
        """Error case: request has no JSON body."""
        response = client.post('/categories', content_type='application/json', data='{}')
        data = response.get_json()

        assert response.status_code == 400
        assert 'error' in data


class TestUpdateCategory:
    """Tests for PUT /categories/<id>"""

    def test_update_category_success(self, client):
        """Happy path: updates category name and description."""
        create_resp = client.post('/categories', json={'name': 'Old Name', 'description': 'Old desc'})
        category_id = create_resp.get_json()['id']

        response = client.put(f'/categories/{category_id}', json={
            'name': 'New Name',
            'description': 'New description'
        })
        data = response.get_json()

        assert response.status_code == 200
        assert data['name'] == 'New Name'
        assert data['description'] == 'New description'

    def test_update_category_partial(self, client):
        """Happy path: updates only the description."""
        create_resp = client.post('/categories', json={'name': 'Tech', 'description': 'Old'})
        category_id = create_resp.get_json()['id']

        response = client.put(f'/categories/{category_id}', json={
            'description': 'Updated description'
        })
        data = response.get_json()

        assert response.status_code == 200
        assert data['name'] == 'Tech'
        assert data['description'] == 'Updated description'

    def test_update_category_not_found(self, client):
        """Error case: category does not exist."""
        response = client.put('/categories/999', json={'name': 'Ghost'})
        data = response.get_json()

        assert response.status_code == 404
        assert data['error'] == 'Category not found'

    def test_update_category_empty_name(self, client):
        """Error case: trying to set name to empty string."""
        create_resp = client.post('/categories', json={'name': 'Valid'})
        category_id = create_resp.get_json()['id']

        response = client.put(f'/categories/{category_id}', json={'name': ''})
        data = response.get_json()

        assert response.status_code == 400
        assert 'error' in data

    def test_update_category_duplicate_name(self, client):
        """Error case: trying to rename to an existing category name."""
        client.post('/categories', json={'name': 'First'})
        create_resp = client.post('/categories', json={'name': 'Second'})
        category_id = create_resp.get_json()['id']

        response = client.put(f'/categories/{category_id}', json={'name': 'First'})
        data = response.get_json()

        assert response.status_code == 409
        assert 'already exists' in data['error']


class TestDeleteCategory:
    """Tests for DELETE /categories/<id>"""

    def test_delete_category_success(self, client):
        """Happy path: deletes an existing category."""
        create_resp = client.post('/categories', json={'name': 'ToDelete'})
        category_id = create_resp.get_json()['id']

        response = client.delete(f'/categories/{category_id}')
        data = response.get_json()

        assert response.status_code == 200
        assert data['message'] == 'Category deleted successfully'

        # Verify it's gone
        get_resp = client.get(f'/categories/{category_id}')
        assert get_resp.status_code == 404

    def test_delete_category_not_found(self, client):
        """Error case: category does not exist."""
        response = client.delete('/categories/999')
        data = response.get_json()

        assert response.status_code == 404
        assert data['error'] == 'Category not found'
