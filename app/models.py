from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)
    name = db.Column(db.Text, nullable=False)
    embed = db.Column(db.Text, nullable=False)
    imagelink = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'embed': self.embed,
            'imagelink': self.imagelink,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }