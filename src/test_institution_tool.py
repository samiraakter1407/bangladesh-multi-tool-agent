
from institution_tool import institutions_db_tool

result = institutions_db_tool.invoke({
    "location": "Dhaka",
    "institution_type": "College",
    "limit": 3,
})

print(result)
