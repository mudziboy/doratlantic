from datetime import datetime, timezone, timedelta
import json
import uuid
import base64
import qrcode
from typing import List
import time
import requests
from app.client.engsel import *
from app.client.encrypt import API_KEY, build_encrypted_field, decrypt_xdata, encryptsign_xdata, java_like_timestamp, get_x_signature_payment, get_x_signature_bounty
from app.type_dict import PaymentItem

def settlement_qris_v2(
    api_key: str,
    tokens: dict,
    items: List[PaymentItem],
    ask_overwrite: bool = True,
):  
    token_confirmation = items[0]["token_confirmation"]
    payment_targets = ""
    for item in items:
        if payment_targets != "":
            payment_targets += ";"
        payment_targets += item["item_code"]
    
    amount_int = items[-1]["item_price"]
    
    # Overwrite
# if ask_overwrite:
#     print(f"Total amount is {amount_int}.\nEnter new amount if you need to overwrite.")
#     amount_str = input("Press enter to ignore & use default amount: ")
#     if amount_str != "":
#         try:
#             amount_int = int(amount_str)
#         except ValueError:
#             print("Invalid overwrite input, using original price.")
    
    # Get payment methods
    payment_path = "payments/api/v8/payment-methods-option"
    payment_payload = {
        "payment_type": "PURCHASE",
        "is_enterprise": False,
        "payment_target": items[0]["item_code"],
        "lang": "en",
        "is_referral": False,
        "token_confirmation": token_confirmation
    }
    
    print("Getting payment methods...")
    payment_res = send_api_request(api_key, payment_path, payment_payload, tokens["id_token"], "POST")
    if payment_res["status"] != "SUCCESS":
        print("Failed to fetch payment methods.")
        print(f"Error: {payment_res}")
        return None
    
    token_payment = payment_res["data"]["token_payment"]
    ts_to_sign = payment_res["data"]["timestamp"]
    
    # Settlement request
    path = "payments/api/v8/settlement-multipayment/qris"
    settlement_payload = {
        "akrab": {
            "akrab_members": [],
            "akrab_parent_alias": "",
            "members": []
        },
        "can_trigger_rating": False,
        "total_discount": 0,
        "coupon": "",
        "payment_for": "BUY_PACKAGE",
        "topup_number": "",
        "is_enterprise": False,
        "autobuy": {
            "is_using_autobuy": False,
            "activated_autobuy_code": "",
            "autobuy_threshold_setting": {
            "label": "",
            "type": "",
            "value": 0
            }
        },
        "access_token": tokens["access_token"],
        "is_myxl_wallet": False,
        "additional_data": {},
        "total_amount": amount_int,
        "total_fee": 0,
        "is_use_point": False,
        "lang": "en",
        "items": items,
        "verification_token": token_payment,
        "payment_method": "QRIS",
        "timestamp": int(time.time()),
    }
    
    encrypted_payload = encryptsign_xdata(
        api_key=api_key,
        method="POST",
        path=path,
        id_token=tokens["id_token"],
        payload=settlement_payload
    )
    
    xtime = int(encrypted_payload["encrypted_body"]["xtime"])
    sig_time_sec = (xtime // 1000)
    x_requested_at = datetime.fromtimestamp(sig_time_sec, tz=timezone.utc).astimezone()
    settlement_payload["timestamp"] = ts_to_sign
    
    body = encrypted_payload["encrypted_body"]
    x_sig = get_x_signature_payment(
            api_key,
            tokens["access_token"],
            ts_to_sign,
            payment_targets,
            token_payment,
            "QRIS"
        )
    
    headers = {
        "host": BASE_API_URL.replace("https://", ""),
        "content-type": "application/json; charset=utf-8",
        "user-agent": UA,
        "x-api-key": API_KEY,
        "authorization": f"Bearer {tokens['id_token']}",
        "x-hv": "v3",
        "x-signature-time": str(sig_time_sec),
        "x-signature": x_sig,
        "x-request-id": str(uuid.uuid4()),
        "x-request-at": java_like_timestamp(x_requested_at),
        "x-version-app": "8.7.0",
    }
    
    url = f"{BASE_API_URL}/{path}"
    print("Sending settlement request...")
    resp = requests.post(url, headers=headers, data=json.dumps(body), timeout=30)
    
    try:
        decrypted_body = decrypt_xdata(api_key, json.loads(resp.text))
        if decrypted_body["status"] != "SUCCESS":
            print("Failed to initiate settlement.")
            print(f"Error: {decrypted_body}")
            return None
        
        transaction_id = decrypted_body["data"]["transaction_code"]
        
        return transaction_id
    except Exception as e:
        print("[decrypt err]", e)
        return resp.text

def get_qris_code(
    api_key: str,
    tokens: dict,
    transaction_id: str
):
    path = "payments/api/v8/pending-detail"
    payload = {
        "transaction_id": transaction_id,
        "is_enterprise": False,
        "lang": "en",
        "status": ""
    }
    
    res = send_api_request(api_key, path, payload, tokens["id_token"], "POST")
    if res["status"] != "SUCCESS":
        print("Failed to fetch QRIS code.")
        print(f"Error: {res}")
        return None
    
    return res["data"]["qr_code"]

def get_qris_payment_data(
    api_key: str,
    tokens: dict,
    items: List[PaymentItem],
    ask_overwrite: bool = True,
):
    """
    Membuat transaksi QRIS dan mengembalikan URL QRIS.
    Tidak ada lagi print() atau input() di sini.
    """
    transaction_id = settlement_qris_v2(
        api_key,
        tokens,
        items,
        ask_overwrite
    )
    
    if not transaction_id:
        # Jika gagal, kembalikan None
        return None
    
    qris_code = get_qris_code(api_key, tokens, transaction_id)
    if not qris_code:
        return None
    
    # Buat URL QRIS
    qris_b64 = base64.urlsafe_b64encode(qris_code.encode()).decode()
    qris_url = f"https://ki-ar-kod.netlify.app/?data={qris_b64}"
    
    return qris_url
