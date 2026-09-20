class UserModel:
    def __init__(self, filepath):
        self.filepath = filepath
        self.__load_users_from_file()

    def __load_users_from_file(self):
        users = {}
        with open(self.filepath, "r") as f:
            for line in f:
                user_id, username, age = line.strip().split(",")
                users[int(user_id)] = {
                    "user_id": user_id,
                    "username": username,
                    "age": age
                }
        self.__users = users
        self.__next_user_id = max(self.__users.keys()) + 1

    def get_users(self, user_id):
        if user_id is None:
            return self.__users
        return self.__users.get(user_id)

    def add_user(self, username, age):
        user_id = self.__next_user_id
        self.__users[user_id] = {
            "user_id": user_id,
            "username": username,
            "age": age
        }
        self.__next_user_id += 1

        return self.__users[user_id]
