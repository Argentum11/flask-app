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

    def get_user(self, user_id):
        return self.__users.get(user_id)

    def list_users(self, limit: int = None, offset: int = None, filter_by=None):
        offset = 0 if offset is None else offset
        end = None if limit is None else offset+limit
        users = list(self.__users.values())
        if filter_by is not None:
            field, compare, value_casted = filter_by
            cast = type(value_casted)
            users = [user for user in users if compare(
                cast(user[field]), value_casted)]
        return users[offset:end]

    def add_user(self, username, age):
        user_id = self.__next_user_id
        self.__users[user_id] = {
            "user_id": user_id,
            "username": username,
            "age": age
        }
        self.__next_user_id += 1

        return self.__users[user_id]

    def delete_user(self, user_id):
        return self.__users.pop(user_id, None) is not None

    def update_user(self, user_id, new_username, new_age):
        if self.__users.get(user_id, None) is None:
            return None
        else:
            target_user = self.__users[user_id]
            if new_username is not None:
                target_user["username"] = new_username
            if new_age is not None:
                target_user["age"] = new_age
            return target_user
