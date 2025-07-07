from flask import Blueprint, request, jsonify
#from .mpesa import handle_mpesa_callback




mpesa_routes = Blueprint("mpesa_routes", __name__)



@mpesa_routes.route("/", methods=["GET"])
def stkpush():
    return {"message" : "Backend is running "}, 200

#@mpesa_routes.route("/callback", methods=['POST'])
#def mpesa_callback():
 #   data = request.get_json()
  #  print("callback received:", data)



   # handle_mpesa_callback(data)
    #return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


@mpesa_routes.route('/callback', methods=['POST'], strict_slashes=False)
def callback():
    data = request.get_json()
    print("Received callback:", data)
    return {"message":"callbackreceived"}, 200