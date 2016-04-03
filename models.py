from appflask import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True)
	artist_q = db.Column(db.String())
	date_sent = db.Column(db.Date)

	def __init__(self, artist_q, date_sent):
		self.artist_q = artist_q
		self.date_sent = date_sent

	def __repr__(self):
		return '<id {}'.format(self.id)
