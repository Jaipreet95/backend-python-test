from alayatodo import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    todo = db.relationship('Todo', backref='users', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), index=True)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Todo {} {}>'.format(self.id,self.description)

