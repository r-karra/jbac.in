import base64
import json
from urllib import parse, request

from django.conf import settings
from django.core.mail import send_mail


class OTPDeliveryError(Exception):
    pass


def _send_twilio_sms(mobile_number, code):
    if not settings.OTP_TWILIO_ACCOUNT_SID or not settings.OTP_TWILIO_AUTH_TOKEN or not settings.OTP_TWILIO_FROM_NUMBER:
        raise OTPDeliveryError("Twilio credentials are not fully configured.")

    endpoint = (
        f"https://api.twilio.com/2010-04-01/Accounts/"
        f"{settings.OTP_TWILIO_ACCOUNT_SID}/Messages.json"
    )
    payload = parse.urlencode(
        {
            "To": mobile_number,
            "From": settings.OTP_TWILIO_FROM_NUMBER,
            "Body": f"Your JBAC OTP is {code}. It expires in 10 minutes.",
        }
    ).encode("utf-8")
    req = request.Request(endpoint, data=payload)
    auth_token = base64.b64encode(
        f"{settings.OTP_TWILIO_ACCOUNT_SID}:{settings.OTP_TWILIO_AUTH_TOKEN}".encode("utf-8")
    ).decode("ascii")
    req.add_header("Authorization", f"Basic {auth_token}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with request.urlopen(req, timeout=10) as response:
            if response.status >= 300:
                raise OTPDeliveryError("Twilio request failed.")
    except Exception as exc:
        raise OTPDeliveryError(f"Twilio delivery failed: {exc}") from exc


def _send_msg91_sms(mobile_number, code):
    if not settings.OTP_MSG91_AUTH_KEY:
        raise OTPDeliveryError("MSG91 auth key is not configured.")

    endpoint = "https://control.msg91.com/api/v5/otp"
    payload = {
        "template_id": settings.OTP_MSG91_TEMPLATE_ID,
        "mobile": f"91{mobile_number}",
        "otp": code,
        "sender": settings.OTP_MSG91_SENDER_ID,
    }
    req = request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("authkey", settings.OTP_MSG91_AUTH_KEY)

    try:
        with request.urlopen(req, timeout=10) as response:
            if response.status >= 300:
                raise OTPDeliveryError("MSG91 request failed.")
    except Exception as exc:
        raise OTPDeliveryError(f"MSG91 delivery failed: {exc}") from exc


def send_otp_code(user, code):
    provider = settings.OTP_PROVIDER
    if provider == "twilio":
        _send_twilio_sms(user.mobile_number, code)
        return "sms"
    if provider == "msg91":
        _send_msg91_sms(user.mobile_number, code)
        return "sms"

    if user.email:
        send_mail(
            subject="JBAC OTP Login Code",
            message=f"Your JBAC OTP code is {code}. It will expire in 10 minutes.",
            from_email="no-reply@jbac.in",
            recipient_list=[user.email],
        )
        return "email"

    return "console"