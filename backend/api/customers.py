from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

from services.customer import (
    create_customer,
    get_customers,
    get_customer,
    update_customer,
    delete_customer,
)

customer = APIRouter()


@customer.post("/", response_model=CustomerResponse)
def create(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)


@customer.get("/", response_model=list[CustomerResponse])
def get_all(db: Session = Depends(get_db)):
    return get_customers(db)


@customer.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_one(
    customer_id: int,
    db: Session = Depends(get_db),
):

    customer = get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@customer.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
):

    updated = update_customer(
        db,
        customer_id,
        customer,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return updated


@customer.delete("/{customer_id}")
def delete(
    customer_id: int,
    db: Session = Depends(get_db),
):

    deleted = delete_customer(
        db,
        customer_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return {
        "message": "Customer deleted successfully"
    }
