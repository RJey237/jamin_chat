from .models import Chat


async def chats_to_json(chats):
    return [await chat_to_json(chat) async  for chat in chats]


async def chat_to_json(chat:Chat):
    return {
        "id":chat.id,
        "title":chat.title,
        "type":chat.type,
    }
