import jwt
from datetime import datetime
from dateutil.relativedelta import relativedelta

algorithm = "HS256"
key = "secret"  # TODO put this into env variables
NOW = datetime.now()
SIX_MONTHS_LATER = NOW + relativedelta(months=+6)


def encode_jwt(payload):
    """Encode JWT token with HS256 hashing algorithm"""

    payload.update({
        "exp": SIX_MONTHS_LATER,
        "iat": NOW
    })
    token = jwt.encode(
        payload=payload,
        key=key,
        algorithm=algorithm
        )
    return token


def decode_jwt(token):
    """Decode JWT token"""

    decoded_token = jwt.decode(jwt=token, key=key)

    return decoded_token


def validate_jwt(token):
    """Validate given JWT"""

    try:
        jwt.decode(jwt=token, key=key)
    except jwt.ExpiredSignatureError:
        return False
    
    return True


def extend_jwt(token):
    """Returns new JWT if given token is valid"""

    if validate_jwt(token):
        payload = decode_jwt(token)
        new_token = encode_jwt(payload)
        return new_token
    else:
        return "Provided token is invalid."


