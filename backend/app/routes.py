from flask import Blueprint, request, jsonify
from .mpesa import stk_push
from .models import db, STKPushRequest, STKPushResponse, Transaction
import os
import requests




mpesa_routes = Blueprint("mpesa_routes", __name__)



@mpesa_routes.route("/", methods=["GET"])
def stkpush():
    return {"message" : "Backend is running "}, 200



@mpesa_routes.route('/callback', methods=['POST'], strict_slashes=False)
def callback():
    data = request.get_json()
    print("Received callback:", data)
    return {"message":"callbackreceived"}, 200


@mpesa_routes.route('/stk-push', methods=['POST'])
def initiate_stk_push():
    data = request.get_json()
    phone = data.get("phone_number")
    amount = data.get("amount")

    response_json, status_code, password, timestamp = stk_push(phone, amount)


    #save the STKPushRequest

    checkout_request_id = response_json.get("CheckoutRequestID")
    merchant_request_id = response_json.get("MerchantRequestID")
    response_code = response_json.get("ResponseCode")
    response_description = response_json.get("ResponseDescription")
    customer_message = response_json.get("CustomerMessage")

    print("DEBUG STK PUSH DATA")
    print("phone_number:", phone)
    print("business_shortcode:", os.getenv("BUSINESS_SHORTCODE"))
    print("amount:", amount)
    print("password:", password)
    print("timestamp:", timestamp)
    print("checkout_request_id",checkout_request_id)
    print("merchant_request_id",merchant_request_id)
    print("party_a:", phone)
    print("party_b:", os.getenv("BUSINESS_SHORTCODE"))

    stk_request = STKPushRequest(

        phone_number=phone,
        business_shortcode=os.getenv("BUSINESS_SHORTCODE"),
        amount=amount,   
        password=password,
        timestamp=timestamp,
        checkout_request_id=checkout_request_id,
        merchant_request_id=merchant_request_id,
        party_a=phone,
        party_b=os.getenv("BUSINESS_SHORTCODE"),
    )
    db.session.add(stk_request)
    db.session.commit()




    #save STKPushResponse
    stk_response = STKPushResponse(
        request_id=stk_request.id,
        merchant_request_id=merchant_request_id,
        checkout_request_id=checkout_request_id,
        response_code=response_code,
        response_description=response_description,
        customer_message=customer_message
    )
    db.session.add(stk_response)
    db.session.commit()
    return jsonify({"message":"successful"})


@mpesa_routes.route('/stk_callback', methods=['POST'])
def stk_callback():
    data = request.get_json()
    callback = data['Body']['stkCallback']

    #Extract data
    merchant_id = callback['MerchantRequestID']
    checkout_id = callback['CheckoutRequestID']
    result_code =callback['ResultCode']
    result_desc = callback['ResultDesc']

    
    if result_code == 0:
        metadata = callback['CallbackMetadata']['Item']

        #extract metadata
        receipt = next((item['Value'] for item in metadata if item['Name'] == 'MpesaReceiptNumber'), None)
        amount = next((item['Value'] for item in metadata if item['Name'] == 'Amount'), 0)
        phone = next((item['Value'] for item in metadata if item['Name'] == 'PhoneNumber'), None)
        date = next((item['Value'] for item in metadata if item['Name'] == 'TransactionDate'), None)
    
    #find the response in the STKPushResponse
    response = STKPushResponse.query.filter_by(
        merchant_request_id=merchant_id,
        checkout_request_id=checkout_id

    ).first()

    if response:
        transaction = Transaction(
            merchant_request_id=merchant_id,
            checkout_request_id=checkout_id,
            result_code=str(result_code),
            result_desc=result_desc,
            mpesa_receipt_number=receipt,
            amount=amount,
            phone_number=phone,
            transaction_date=str(date),
            response=response
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction saved successfully"})


    else:

      return jsonify({"error": "No matching STKPushResponse found"})


@mpesa_routes.route('/display_transaction/<phone_number>', methods=['GET'])
def display_transaction(phone_number):
    try:
        transaction = Transaction.query.filter_by(phone_number=phone_number).all()

        if not transaction:
            return jsonify({"error":"No transaction found for this phone number"}),404
        
        result = []
        for t in transaction:
            result.append({
                "transaction_id":t.id,
                "merchant_request_id":t.merchant_request_id,
                "checkout_request_id":t.checkout_request_id,
                "result_code":t.result_code,
                "result_desc":t.result_desc,
                "mpesa_receipt_number":t.mpesa_receipt_number,
                "amount":t.amount,
                "phone_number":t.phone_number,
                "transaction_date":t.transaction_date,
                "created_at":t.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
            return jsonify(result),200
    except Exception as e:
        return jsonify({"error":f"Ab error occured: {str(e)}"}),500