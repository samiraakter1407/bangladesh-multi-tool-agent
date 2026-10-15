
from restaurant_tool import restaurants_db_tool

result = restaurants_db_tool.invoke({
    "location": "Dhaka",
    "min_rating": 4,
    "limit": 3,
})

print(result)
