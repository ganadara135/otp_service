import pyotp
import time

otp_storage = {}

def generate_otp(email):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, digits=4)
    code = totp.now()

    # 이전 정보와 관계없이 덮어씀
    otp_storage[email] = {
        "secret": secret,
        "timestamp": time.time(),
        "used": False
    }
    return code

def verify_otp(email, code, valid_secs=120):
    entry = otp_storage.get(email)
    if not entry or entry["used"]:
        return False

    # 시간 제한 확인
    if time.time() - entry["timestamp"] > valid_secs:
        return False

    totp = pyotp.TOTP(entry["secret"], digits=4)
    if totp.verify(code, valid_window=1):
        entry["used"] = True
        return True
    return False


