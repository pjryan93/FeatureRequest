from extension import db

class Feature(db.Model):

    __tablename__ = 'Feature'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(2500))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.Date(), default = db.func.current_timestamp.date())
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, title, description, priority,target_date):
        self.title = title
        self.description = description
        self.priority = priority
        self.target_date = target_date
    def update(self, title, description, priority,target_date):
        self.title = title
        self.description = description
        self.target_date = target_date
        self.priority = priority
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def createNewFeature(data):
        Feature.incrementPriorities(data['priority'])
        new_feature = Feature(data['title'],data['description'],data['priority'],data['target_date'])
        new_feature.save()
        return new_feature
    
    @staticmethod
    def incrementPriorities(new_priority,upper_bound = None):
        if upper_bound is None:
            features_to_increment = Feature.query.filter(Feature.priority >= new_priority)
        else:
            features_to_increment = Feature.query.filter((Feature.priority >= new_priority) & (Feature.priority < upper_bound))
        for feature in features_to_increment:
            feature.priority = feature.priority + 1
            feature.save()

    @staticmethod
    def decrementPriorities(new_priority,lower_bound):
        features_to_increment = Feature.query.filter((Feature.priority > lower_bound) & (Feature.priority <= new_priority))
        for feature in features_to_increment:
            feature.priority = feature.priority - 1
            feature.save()

    @staticmethod
    def updatePriorities(new_priority,current_priority):
         #move up the list
        if new_priority < current_priority:
            Feature.incrementPriorities(new_priority,current_priority)
        #move down the list
        elif new_priority > current_priority:
            Feature.decrementPriorities(new_priority,current_priority)

    @staticmethod
    def get_all():
        return Feature.query.order_by(Feature.priority).all()
    
    @staticmethod
    def getFeatureCount():
        #force sqlalchemy to use indexed primary key to count
        return  db.session.query(db.func.count(Feature.id)).scalar()

    def __repr__(self):
        return "<Feature: {}>".format(self.title)