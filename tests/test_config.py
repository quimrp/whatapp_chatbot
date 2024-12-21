from config import settings

def test_config():
    print(f"ALVOCHAT_TOKEN: {settings.ALVOCHAT_TOKEN}")
    print(f"ALVOCHAT_INSTANCE_ID: {settings.ALVOCHAT_INSTANCE_ID}")
    print(f"ALVOCHAT_API_URL: {settings.ALVOCHAT_API_URL}")
    print(f"ALVOCHAT_WEBHOOK_URL: {settings.ALVOCHAT_WEBHOOK_URL}")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"TEST_PHONE_NUMBER: {settings.TEST_PHONE_NUMBER}")
    print(f"WEBHOOK_TOKEN: {settings.WEBHOOK_TOKEN}")

if __name__ == "__main__":
    test_config()

