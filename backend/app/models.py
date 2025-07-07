from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number=db.Column(db.String(15), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    stk_request = db.relationship('STKPushRequest', backref='user', lazy=True)


class STKPushRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    phone_number = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    account_reference = db.Column(db.String(100))
    transaction_desc = db.Column(db.Text)
    merchant_request_id = db.Column(db.String(100))
    checkout_request_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    response = db.relationship('STKPushResponse', backref='request', uselist=False)

class STKPushResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('stk_push_request.id'), nullable=False)
    result_code = db.Column(db.Integer)
    result_desc = db.Column(db.Text)
    mpesa_receipt_number = db.Column(db.String(50))
    transaction_date = db.Column(db.BigInteger)
    phone_number = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    response = db.relationship('STKPushResponse', backref='request', uselist=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reference = db.Column(db.String(100))
    type = db.Column(db.String(50))
    amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


