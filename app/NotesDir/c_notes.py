from app import db

class Database(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

class Note(Database):
    __tablename__ = 'note_content'

    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(1024 * 8), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    tag = db.Column(db.String(128*4), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    user = db.relationship('User', backref=db.backref('auth_users', lazy='dynamic'))

    def __init__(self, title, content, category, tag, user_id):
        self.title = title
        self.content = content
        self.category = category
        self.tag = tag
        self.user_id = user_id

    def serialize(self):
        return dict(
            title=self.title,
            content=self.content,
            category=self.category,
            tag=self.tag,
            note_id=self.id,
            user_id=self.user_id
        )

    def getUserId(self):
        return self.user_id

    def __repr__(self):
        return '<Note %r>' % (self.title)
