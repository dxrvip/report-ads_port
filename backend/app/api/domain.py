from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Any, List
from app.schemas.domain import Domain as DomainSchema
from app.schemas.domain import DomainCreate, DomainUpdate
from app.deps.users import CurrentUser
from app.crud import domain as crud
from app.deps.request_params import DomainRequestParams
from sqlalchemy.exc import IntegrityError
from app.deps.db import CurrentAsyncSession

router = APIRouter(prefix="/domain")


@router.get("", response_model=List[DomainSchema], status_code=201)
async def get_domains(
    response: Response,
    session: CurrentAsyncSession, 
    request_params: DomainRequestParams,
    user: CurrentUser)-> Any:

    total = await crud.total_domain(session)
    domains = await crud.list_domain(session, request_params)

    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(domains)}/{total}"
    return domains


@router.post("", response_model=DomainSchema, status_code=201)
async def create_domain(
    domain_in: DomainCreate, 
    session: CurrentAsyncSession,
    user: CurrentUser,
    )->Any:
    try:
        domain = await crud.create_domin(session, domain_in)
    except IntegrityError as err:
        print(err)
        raise HTTPException(402)
    return domain

@router.put("/{domain_id}", response_model=DomainSchema)
async def update_domain(
    domain_id: int,
    domain_in: DomainUpdate,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    domain = await crud.update_domain(session, domain_id, domain_in)
    return domain


@router.get("/{domain_id}", response_model=DomainSchema)
async def get_domain(
    domain_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    domain = await crud.get_domain(session, domain_id)
    return domain


@router.delete("/{domain_id}")
async def delete_domain(
    domain_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    await crud.del_domain(session, domain_id)
    return {"success": True}
