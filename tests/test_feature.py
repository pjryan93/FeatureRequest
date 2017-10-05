# test_feature.py
import unittest
import os
import json
from app import create_app
from app.extension import db
import json
from app.models import Feature
import datetime

class FeatureModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()

    def test_create_feature(self):
        with self.app.app_context():
            featureDict = {'title': 'title','description':'My test description','priority':1,'target_date':datetime.date(2010, 5, 24)}
            for i in range(1,5):
                featureDict['title'] = 'title ' + str(i)
                Feature.createNewFeature(featureDict)
            for i in range(1,5):
                feature = Feature.query.filter(Feature.priority == i).all()
                #check no duplicates
                self.assertEqual(len(feature), 1)
                #check priority matches correct feature
                correctTitle = 'title ' + str((5 - i))
                self.assertIn(feature[0].title, correctTitle)
    
    def test_update_feature_priorities(self):
        
        with self.app.app_context():
            featureDict = {'title': 'title','description':'My test description','priority':1,'target_date':datetime.date(2010, 5, 24)}
            
            for i in range(1,5):
                featureDict['title'] = 'title ' + str(i)
                Feature.createNewFeature(featureDict)

            #input priorites
            input_data = [
                [1,4],
                [3,2],
                [3,1],
                [4,1],
                [2,3],
            ]
            #correct title endings
            correct_data = [
                ['3','2','1','4'],
                ['3','1','2','4'],
                ['2','3','1','4'],
                ['4','2','3','1'],
                ['4','3','2','1']
            ]
            
            for i in range(0,len(input_data)):

                old_prioirty = input_data[i][0]
                new_priority = input_data[i][1]
                
                feature = Feature.query.filter(Feature.priority == old_prioirty).all()[0]

                #update data 
                featureDict['priority'] = new_priority 
                featureDict['title'] = feature.title

                Feature.updatePriorities(new_priority=featureDict['priority'],current_priority=feature.priority)
                feature.update(featureDict['title'],featureDict['description'],featureDict['priority'],featureDict['target_date'])
                feature.save()
                
                correctTitles = correct_data[i]
                
                for i in range(1,5):
                    feature = Feature.query.filter(Feature.priority == i).all()
                    #check no duplicates
                    self.assertEqual(len(feature), 1)
                    #check priority matches correct feature
                    correctTitle = 'title ' + correctTitles[i-1]
                    self.assertIn(feature[0].title, correctTitle)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

class FeatureTestCase(unittest.TestCase):
    """This class represents the feature test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.feature = json.dumps({'title': 'my cool new feature','description':'My test description','priority':'1','target_date':'2017-10-04'})
        self.feature_put = json.dumps({'title': 'my cool new feature plus more' ,'description':'My test description plus more','priority':'2','target_date':'2017-10-04'})
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_feature_creation(self):
        """Test API can create a feature (POST request)"""
        res = self.client().post('/api/v1/feature', data=self.feature,content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn('my cool new feature', str(res.data))
    def test_feature_count(self):
        """Test API can create a feature (POST request)"""
        res = self.client().get('/api/v1/meta')
        self.assertEqual(res.status_code, 200)
        self.assertIn('0', str(res.data))
        res = self.client().post('/api/v1/feature', data=self.feature,content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn('my cool new feature', str(res.data))
        res = self.client().get('/api/v1/meta')
        self.assertEqual(res.status_code, 200)
        self.assertIn('1', str(res.data))

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
