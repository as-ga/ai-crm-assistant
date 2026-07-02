from sqlalchemy.orm import Session

from models import Customer
from schemas import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer: CustomerCreate):

    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        company=customer.company,
        notes=customer.notes,
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_customers(db: Session):

    return db.query(Customer).all()


def get_customer(db: Session, customer_id: int):

    return db.query(Customer).filter(Customer.id == customer_id).first()


def update_customer(
    db: Session,
    customer_id: int,
    customer: CustomerUpdate,
):

    db_customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not db_customer:
        return None

    for key, value in customer.model_dump(exclude_unset=True).items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer


def delete_customer(db: Session, customer_id: int):

    db_customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not db_customer:
        return None

    db.delete(db_customer)
    db.commit()

    return True
