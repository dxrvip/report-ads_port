from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.domain import DomainCreate
from app.models.domain import Domain
from sqlalchemy import select, func
from app.deps.request_params import DomainRequestParams


async def create_domin(db: Session, domain_in: DomainCreate):
    domain: Domain = Domain(**domain_in.dict())
    db.add(domain)
    await db.commit()
    return domain


async def list_domain(db: Session, request_params: DomainRequestParams):
    domains = (
        (
            await db.execute(
                select(Domain)
                .offset(request_params.skip)
                .limit(request_params.limit)
                .order_by(request_params.order_by)
            )
        )
        .scalars()
        .all()
    )
    return domains


async def total_domain(db: Session):
    total = await db.scalar(select(func.count(Domain.id)))
    return total


async def update_domain(db: Session, id, domain_in):
    domain: Optional[Domain] = await db.get(Domain, id)
    update_data = domain_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(domain, field, value)
    db.add(domain)
    await db.commit()
    return domain

async def get_domain(db: Session, id:int):
    domain: Optional[Domain] = await db.get(Domain, id)
    return domain


async def get_domain_by_host(db: Session, host):
    
    _orm = select(Domain).filter(Domain.base_url.like(f"%{host}%"))
    domain: Optional[Domain] = (await db.execute(_orm)).scalar()
    return domain

async def del_domain(db: Session, id:int):
    domain: Optional[Domain] = await db.get(Domain, id)
    await db.delete(domain)
    await db.commit()
    return db