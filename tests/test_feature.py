# test_feature.py
import unittest
import os
import json
from app.app import create_app, db
import json

class FeatureTestCase(unittest.TestCase):
    """This class represents the feature test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.feature = json.dumps({'title': 'my cool new feature','description':'My test description','priority':'1'})
        self.feature_put = json.dumps({'title': 'my cool new feature plus more' ,'description':'My test description plus more','priority':'2'})

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_feature_creation(self):
        """Test API can create a feature (POST request)"""
        res = self.client().post('/api/v1/feature', data=self.feature,content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn('my cool new feature', str(res.data))

    def test_api_can_get_all_feature(self):
        """Test API can get a feature (GET request)."""
        res = self.client().post('/api/v1/feature', data=self.feature,content_type="application/json")
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/feature')
        self.assertEqual(res.status_code, 200)
        self.assertIn('my cool new feature', str(res.data))

    def test_api_can_get_feature_by_id(self):
        """Test API can get a single feature by using it's id."""
        rv = self.client().post('/api/v1/feature', data=self.feature,content_type="application/json")
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/api/v1/feature/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('my cool new feature', str(result.data))

    def test_feature_can_be_edited(self):
        """Test API can edit an existing feature. (PUT request)"""
        rv = self.client().post(
            '/api/v1/feature',
            data=self.feature,
            content_type="application/json"
        )
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/api/v1/feature/1',
            data=self.feature_put,
            content_type="application/json"
        )
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/api/v1/feature/1')
        self.assertIn('my cool new feature plus more', str(results.data))

    def test_feature_deletion(self):
        """Test API can delete an existing feature. (DELETE request)."""
        rv = self.client().post(
            '/api/v1/feature',
            data=self.feature,content_type="application/json")
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/api/v1/feature/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/v1/feature/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
