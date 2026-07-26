from app.core.security import hash_password


class AuthService:

    def register(self, name: str, email: str, password: str):
        hashed_password = hash_password(password)

        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Hashed Password: {hashed_password}")

        return {"message": "User registered successfully"}