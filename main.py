from fastapi import FastAPI


from user_routes import router as user_router
from invoice_route import router as invoice_router
from agent_routes import router as agent_router


app = FastAPI(title="ORM Implementation")

app.include_router(user_router)
app.include_router(invoice_router)
app.include_router(agent_router)