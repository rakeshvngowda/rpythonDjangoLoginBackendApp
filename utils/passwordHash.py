import bcrypt
from utils.CustomError import CustomError

def hashPassword(password):
    salt = bcrypt.gensalt(10)
    bytes = password.encode('utf-8')
    hash = bcrypt.hashpw(bytes,salt)
    return hash

def verifyPassword(password,hashPassword):
    try:
        bytes = password.encode('utf-8')
        hashPasswordBytes = hashPassword.encode('utf-8')
        isPassMatch = bcrypt.checkpw(bytes,hashPasswordBytes)
        if (not isPassMatch):
            raise CustomError('Password Not Matching')
    except Exception as e:
        message = getattr(e,'messages','') or getattr(e,'args','')
        raise CustomError(message[0])

