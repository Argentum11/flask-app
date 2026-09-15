class UserModel:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_users(self):
        users = []
        with open(self.filepath, "r") as f:
            for line in f:
                user_id, username, age = line.strip().split(",")
                users.append({
                    "user_id": user_id,
                    "username": username,
                    "age": age
                })

        return users