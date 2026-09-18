from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="orders-svc-s14")

orders: dict[int, "Order"] = {}
next_id = 1


class OrderCreate(BaseModel):
    priority: int


class Order(OrderCreate):
    id: int


@app.get("/orders", response_model=list[Order])
def get_orders():
    return list(orders.values())


@app.post("/orders", response_model=Order, status_code=201)
def create_order(order: OrderCreate):
    global next_id
    new_order = Order(id=next_id, **order.model_dump())
    orders[next_id] = new_order
    next_id += 1
    return new_order


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return orders[order_id]