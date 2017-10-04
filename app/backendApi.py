from flask_restful import abort, Api, Resource
from flask import request, jsonify
from marshmallow import Schema, fields, pprint, pre_dump
from marshmallow_sqlalchemy import ModelSchema
from models import Feature

class FeatureModelSchema(ModelSchema):
    class Meta:
        model = Feature
    @pre_dump
    def cast_date(self,data):
        print "post"
        data.target_date = data.target_date.date()
        return data
class FeatureSchema(Schema):
    title = fields.Str(strict = True)
    description = fields.Str(strict = True)
    priority = fields.Integer(strict = True)
    target_date = fields.Date()
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
        print json
        data, errors = FeatureSchema().load(json)
        if errors:
            return jsonify(errors), 422
        print data
        new_feature = Feature(data['title'],data['description'],data['priority'],data['target_date'])
        new_feature.incrementPriorities(data['priority'])
        new_feature.save()
        data_to_return = toJson(new_feature,FeatureModelSchema())
        return data_to_return , 201

    def put(self,feature_id=None):
        json = request.get_json()
        if not json or feature_id is None:
            return {'message': 'No input data provided'}, 400
        data, errors = FeatureSchema().load(json)
        if errors:
            return jsonify(errors), 422
        updated_feature = Feature.query.get(feature_id)
        #move up the list
        if data['priority'] < updated_feature.priority:
            updated_feature.incrementPriorities(data['priority'],updated_feature.priority)
        #move down the list
        elif data['priority'] > updated_feature.priority:
            updated_feature.decrementPriorities(data['priority'],updated_feature.priority)
        updated_feature.update(data['title'],data['description'],data['priority'],data['target_date'])
        updated_feature.save()
        data_to_return = toJson(updated_feature,FeatureModelSchema())
        return data_to_return , 200

    def delete(self,feature_id=None):
        if feature_id is None:
            return {'message': 'No input data provided'}, 400
        feature_to_delete = Feature.query.get(feature_id)
        if feature_to_delete is None:
            return {'message': 'Invalid id'}, 400
        feature_to_delete.delete()
        return {'message': 'success'}, 200

def toJson(feature_to_serialize,schema_to_use):
        data , errors = schema_to_use.dump(feature_to_serialize)
        return data

