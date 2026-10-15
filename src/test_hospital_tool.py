from hospital_tool import hospitals_db_tool

result = hospitals_db_tool.invoke({
    "location": "Dhaka",
    "facility_type": "Specialized Hospital",
    "limit": 3,
})

print(result)
