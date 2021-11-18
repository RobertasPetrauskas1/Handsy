from fastapi import APIRouter, Response, Request, HTTPException
from sqlalchemy import exists
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import Session


from handsy.api.auth import encode_jwt
from handsy.api.models.auth import Credentials, Registration, CredentialsEntity
from handsy.api.models.user import User, UserEntity

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(data: Registration, req: Request):
    session: Session = req.state.db
    q = exists(select(CredentialsEntity).filter(CredentialsEntity.email == data.email)).select()
    if (await session.execute(q)).scalar():
        raise HTTPException(400, "Email already exists")

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        birth_date=data.birth_date,
        description=data.description
    )

    credentials = Credentials(
        email=data.email,
        password=data.password
    )
    user_id = await UserEntity.create(req.state.db, user)
    credentials_id = await CredentialsEntity.create(req.state.db, credentials)

    user_entity: UserEntity = await UserEntity.select(req.state.db, user_id)
    credentials_entity: CredentialsEntity = await CredentialsEntity.select(req.state.db, credentials_id)
    user_entity.credentials = credentials_entity

    return Response(status_code=201)


@router.post("/login")
async def login(credentials: Credentials, req: Request):
    session: Session = req.state.db
    q = select(CredentialsEntity).filter(
        CredentialsEntity.email == credentials.email,
        CredentialsEntity.password == credentials.password
    )

    try:
        credentials_entity: CredentialsEntity = (await session.execute(q)).scalar_one()
    except NoResultFound:
        raise HTTPException(400, "Bad email and/or password")

    token = encode_jwt(credentials_entity.user_id, credentials.email, credentials_entity.user.role)

    return {
        "value": {"token": str(token)}
    }
