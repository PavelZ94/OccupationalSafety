class UserInfoEvent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.data = {}

    def update(self, key, value):
        self.data[key] = value

async def save_user_info(event: UserInfoEvent):
    # Здесь реализуйте логику сохранения данных пользователя в базу данных
    pass

async def save_user_info_event(event: UserInfoEvent):
    await save_user_info(event)
