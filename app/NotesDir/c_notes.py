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
    category_id = db.Column(db.Integer, db.ForeignKey('note_category.id'))
    category = db.relationship('NoteCategory', backref=db.backref('note_category', lazy='dynamic'))
    tag_id = db.Column(db.Integer, db.ForeignKey('note_tag.id'))
    tag = db.relationship('NoteTag', backref=db.backref('note_tag', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    user = db.relationship('User', backref=db.backref('auth_users', lazy='dynamic'))

    def __init__(self, title, content, category_id, tag_id, user_id):
        self.title = title
        self.content = content
        self.category_id = category_id
        self.tag_id = tag_id
        self.user_id = user_id

    def serialize(self):
        return dict(
            title=self.title,
            content=self.content,
            category_id=self.category_id,
            tag_id=self.tag_id,
            user_id=self.user_id
        )

    def getUserId(self):
        return self.user_id

    def __repr__(self):
        return '<Note %r>' % (self.title)


class NoteCategory(Database):
    __tablename__ = 'note_category'

    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<NoteCategory %r>' % (self.name)

class NoteTag(Database):
    __tablename__ = 'note_tag'

    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<NoteTag %r>' % (self.name)