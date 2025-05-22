from flask import Flask, request, render_template
from otp_manager import generate_otp, verify_otp
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def send_email(to, code):
    msg = EmailMessage()
    msg.set_content(f"Your OTP code is: {code}")
    msg["Subject"] = "Your OTP Code"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")
        if action == "send":
            code = generate_otp(email)
            send_email(email, code)
            result = f"OTP sent to {email}"
        elif action == "verify":
            code = request.form.get("otp")
            if verify_otp(email, code):
                result = "✅ OTP Verified Successfully!"
            else:
                result = "❌ Invalid or Expired OTP."

    return render_template("index.html", result=result)


@app.route("/")
def hello():
    return "Hello, OTP Service!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
