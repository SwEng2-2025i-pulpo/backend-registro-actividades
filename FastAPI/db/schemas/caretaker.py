
def caretaker_schema(user) -> dict:
    return{
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "passwordHash": user["passwordHash"],
        "role": user["role"]
        }


def caretakers_schema(users) -> list:
    return [caretaker_schema(user) for user in users]
