from fastapi import FastAPI
from app.planner.plan_generator import TravelPlanner
from app.models.schemas import TripRequest

app = FastAPI(title="TripSage - AI Travel Planner")


@app.post("/plan-trip")
def plan_trip(data: TripRequest):
    result = TravelPlanner().plan_trip(
        destination=data.destination,
        budget=data.budget,
        days=data.days,
        style=data.style,
    )
    return {"plan": result}
