class UserModel:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_users(self):
        users = []
        with open(self.filepath, "r") as f:
            for line in f:
                username, age = line.strip().split(",")
                users.append({
                    "username": username,
                    "age": age
                })

        return users