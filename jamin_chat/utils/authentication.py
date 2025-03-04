from django.contrib.auth.models import AnonymousUser
# from rest_framework.authtoken.models import Token
from channels.auth import AuthMiddlewareStack
from urllib.parse import parse_qs
from django.contrib.auth.models import User

async def get_user(query_string, headers):
    if b"token" in query_string:
        try:
            user_id=query_string[b"user_id"][0]
            user=await User.objects.aget(id=user_id)
            return user
        except:
            return AnonymousUser()
        
    elif b'authorization' in headers:

        try:
            key, value =headers[b'authorization'].decode().split()
            if key == 'user_id':
                user=await User.objects.aget(id=value)
                return user
        except User.DoesNotExist:
            return AnonymousUser()
    else:
        return AnonymousUser()
    

class TokenAuthMiddleware:
    def __init__(self,inner):
        self.inner=inner

    async def __call__(self,scope,receive,send):
        query_string=parse_qs(
        scope['query_string']
        )
        headers =dict(scope['headers'])
        print(headers)
        scope['user']=await get_user(query_string,headers)
        return await self.inner(scope,receive,send)
    

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))