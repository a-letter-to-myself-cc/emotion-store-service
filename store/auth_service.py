def verify_access_token(token: str) -> int:
    if token == "mock-token-123":
        print("✅ MOCK TOKEN 인증 통과")
        return 999
    raise Exception("❌ Invalid token (Mock mode)")
