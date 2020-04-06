from . import *
import flask

class Subreddit_List(Base):
  __tablename__ = 'subreddit_list'

  subreddit  = db.Column(db.String(1000), nullable =False, unique =True)

  def __init__(self, **kwargs):
    self.subreddit = kwargs.get('subreddit', None)

  def __repr__(self):
    return str(self.__dict__)

  def insert_self(self):
    db.session.add(self)
    db.session.commit()
    
  def delete_all():
    db.session.query(Subreddit_List).delete()
    db.session.commit()

class Subreddit_ListSchema(ModelSchema):
  class Meta:
    model = Subreddit_List