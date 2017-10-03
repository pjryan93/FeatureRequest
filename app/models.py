from extension import db

class Feature(db.Model):

    __tablename__ = 'Feature'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(2500))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority
    def update(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority
    def save(self):
        db.session.add(self)
        db.session.commit()
    def incrementPriorities(self,new_priority,upper_bound):
        features_to_increment = Feature.query.filter((Feature.priority >= new_priority) & (Feature.priority < upper_bound))
        for feature in features_to_increment:
            feature.priority = feature.priority + 1
            feature.save()
    def decrementPriorities(self,new_priority,lower_bound):
        features_to_increment = Feature.query.filter((Feature.priority > lower_bound) & (Feature.priority <= new_priority))
        for feature in features_to_increment:
            feature.priority = feature.priority - 1
            feature.save()
    @staticmethod
    def get_all():
        return Feature.query.order_by(Feature.priority).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Feature: {}>".format(self.title)











