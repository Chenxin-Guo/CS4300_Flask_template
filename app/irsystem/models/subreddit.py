from . import *
import flask
import praw
import datetime as dt

class Subreddit(Base):
  __tablename__ = 'subreddit'

  title             = db.Column(db.String(8000), nullable =False)
  score             = db.Column(db.Integer, nullable =False)
  url               = db.Column(db.String(1000), nullable =False)
  comments_number    = db.Column(db.Integer, nullable =False)
  post_created_time = db.Column(db.Date, nullable =False)
  body_text         = db.Column(db.TEXT, nullable =False)

  def __init__(self, **kwargs):
    self.title              = kwargs.get('title', None)
    self.score              = kwargs.get('score', None)
    self.url                = kwargs.get('url', None)
    self.comments_number    = kwargs.get('comments_number', None)
    self.post_created_time  = kwargs.get('post_created_time', None)    
    self.body_text          = kwargs.get('body_text', None)

  def __repr__(self):
    return str(self.__dict__)

  def insert_self(self):
    db.session.add(self)
    db.session.commit()

  def delete_all():
    db.session.query(Subreddit).delete()
    db.session.commit()


class SubredditSchema(ModelSchema):
  class Meta:
    model = Subreddit