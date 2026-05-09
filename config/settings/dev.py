from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Development convenience: print OTP to terminal instead of sending SMS.
# To enable real SMS in dev, set OTP_DELIVERY=sms in your environment/.env.
OTP_DELIVERY = (os.environ.get("OTP_DELIVERY") or "console").strip().lower()
