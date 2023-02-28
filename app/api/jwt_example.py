import jwt
from jwt.exceptions import ExpiredSignatureError
import datetime
import time

expiration = 5


token = jwt.encode(
    {
        'id': 1,
        'exp': datetime.datetime.now().timestamp() + datetime.timedelta(seconds=expiration).seconds
    },
    '8743b52063cd84097a65d1633f5c74f5',
    algorithm='HS256'
)

# time.sleep(10)

try:
    print(jwt.decode(token, '8743b52063cd84097a65d1633f5c74f5', algorithms=['HS256']))
except ExpiredSignatureError as error:
    print(error)

