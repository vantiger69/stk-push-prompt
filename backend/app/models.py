from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"


    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number=db.Column(db.String(15), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    stk_request = db.relationship('STKPushRequest', back_populates='user', lazy=True)


class STKPushRequest(db.Model):

    __tablename__ = "stk_push_request"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
 
     #requered by saf
    business_shortcode = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False, default='CustomerPayBillOnline')
    amount = db.Column(db.Float, nullable=False)

    #customer information
    phone_number = db.Column(db.String(20), nullable=False)
    party_a = db.Column(db.String(20), nullable=False)
    party_b = db.Column(db.String(20), nullable=False)
    

    #other information
    account_reference = db.Column(db.String(100), nullable=True)
    transaction_desc = db.Column(db.String(255), nullable=True)


    #to store what safaricom returns
    merchant_request_id = db.Column(db.String(100), nullable=True)
    checkout_request_id = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #relationship
    user = db.relationship('User', back_populates='stk_request')
    response = db.relationship('STKPushResponse', back_populates='request', uselist=False, cascade="all, delete-orphan")



class STKPushResponse(db.Model):

    __tablename__ = "stk_push_response"

    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(db.Integer, db.ForeignKey('stk_push_request.id'), nullable=False)


    merchant_request_id = db.Column(db.String(100), nullable=False)
    checkout_request_id = db.Column(db.String(100), nullable=False)
    response_code = db.Column(db.String(10), nullable=False)
    response_description = db.Column(db.String(255), nullable=False)
    customer_message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    request = db.relationship('STKPushRequest', back_populates="response")

    transaction = db .relationship("Transaction", back_populates="response", uselist=False, cascade="all, delete-orphan")



class Transaction(db.Model):

    __tablename__ = "transaction"
    
    id = db.Column(db.Integer, primary_key=True)

    merchant_request_id = db.Column(db.String(100), nullable=False)
    checkout_request_id = db.Column(db.String(100), nullable=False)

    result_code = db.Column(db.String(10), nullable=False)
    result_desc = db.Column(db.String(255), nullable=True)


    mpesa_receipt_number = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Numeric(10, 2))
    phone_number = db.Column(db.String(20), nullable=True)
    transaction_date = db.Column(db.String(20), nullable=True)

    response_id = db.Column(db.Integer, db.ForeignKey('stk_push_response.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.relationship('STKPushResponse', back_populates='transaction')




