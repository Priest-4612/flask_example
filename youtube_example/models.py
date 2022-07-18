from app import Base, db, session


class Video(Base):
    __tablename__ = 'videos'
    __table_args__ = {
        'schema': 'content',
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
