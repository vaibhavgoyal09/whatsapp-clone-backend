from fastapi import Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials, initialize_app
from app.auth.auth_service import AuthService
import traceback


credential = credentials.Certificate('firebase-adminsdk.json')
initialize_app(credential)


def get_user_token(
    res: Response,
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Bearer authentication is needed",
        headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
    )

    if cred is None:
        raise credentials_exception

    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        print(traceback.print_exc())
        raise credentials_exception
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token


def get_current_user_uid(token=Depends(get_user_token)) -> str:
    return token['uid']


async def get_current_user(
    firebase_uid=Depends(get_current_user_uid),
    service: AuthService = Depends()
):
    user = await service.get_user_by_firebase_uid(firebase_uid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
