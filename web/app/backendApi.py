from flask_restful import abort, Api, Resource
from flask import request, jsonify
from marshmallow import Schema, fields, pprint, pre_dump, pre_load
from marshmallow_sqlalchemy import ModelSchema
from models import Feature
from datetime import datetime

class FeatureModelSchema(ModelSchema):
    class Meta:
        model = Feature
    @pre_dump
    def cast_date(self,data):
        if isinstance(data.target_date,datetime):
            data.target_date = data.target_date.date()
        return data

class FeatureSchema(Schema):
    title = fields.Str(strict = True)
    description = fields.Str(strict = True)
    priority = fields.Integer(strict = True)
    target_date = fields.Date()

class FeatureMetaDataSchema(Schema):
    feature_count = fields.Integer()

class FeatureMetaDataResource(Resource):
    def get(self):
        schema = FeatureMetaDataSchema()
        data = dict()
        data['feature_count'] = int(Feature.getFeatureCount())
        data =  schema.dump(data)
        return data, 200

class FeatureResource(Resource):
    def get(self,feature_id=None):
        if feature_id is None:
            schema = FeatureModelSchema(many=True)
            data =  schema.dump(Feature.get_all())
        else:
            feature = Feature.query.get(feature_id)
            if feature is None:
                return {'message': 'Does not exist'}, 404
            data =  toJson(Feature.query.get(feature_id),FeatureModelSchema())
        return data, 200

    def post(self):
        json = request.get_json()
        if not json:
            return {'message': 'No input data provided'}, 400
        data, errors = FeatureSchema().load(json)
        if errors:
            return jsonify(errors), 422
        data['priority'] = checkPriority(data['priority'],1)
        new_feature = Feature.createNewFeature(data)
        data_to_return = toJson(new_feature,FeatureModelSchema())
        return data_to_return , 201

    def put(self,feature_id=None):
        json = request.get_json()
        if not json or feature_id is None:
            return {'message': 'No input data provided'}, 400
        data, errors = FeatureSchema().load(json)
        if errors:
            return jsonify(errors), 422
        feature_to_update = Feature.query.get(feature_id)
        #update other feature priorities
        data['priority'] = checkPriority(data['priority'])
        Feature.updatePriorities(new_priority=data['priority'], current_priority=feature_to_update.priority)
        #update this feature to new state
        feature_to_update.update(data['title'],data['description'],data['priority'],data['target_date'])
        feature_to_update.save()
        data_to_return = toJson(feature_to_update,FeatureModelSchema())
        return data_to_return , 200

    def delete(self,feature_id=None):
        if feature_id is None:
            return {'message': 'No input data provided'}, 400
        feature_to_delete = Feature.query.get(feature_id)
        if feature_to_delete is None:
            return {'message': 'Invalid id'}, 400
        feature_to_delete.delete()
        return {'message': 'success'}, 200

def checkPriority(priority,priorityIncrease = 0):
    maxPriority = Feature.getFeatureCount() + priorityIncrease
    if priority > maxPriority:
        return maxPriority
    else:
        return priority

def toJson(feature_to_serialize,schema_to_use):
        data , errors = schema_to_use.dump(feature_to_serialize)
        return data

