from flask import Blueprint, request, jsonify
from .mpesa import stk_push
from .models import db, STKPushRequest, STKPushResponse
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

    #if status_code != 200:
     #   print("STK response failed")
      #  return jsonify({"error": "STK response failed"}), 400
    
    #else:
     #   print("STK response successfully saved")
      #  return jsonify({"message": "STK response successfully saved"}), 200