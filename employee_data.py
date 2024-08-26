import random
import json
from faker import Faker

fake = Faker()

def get_employee_data(employeeId):
    print("Executing get_employee_data ...")

    departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations']
    roles = ['Software Engineer', 'Product Manager', 'HR Specialist', 'Sales Executive', 'Marketing Analyst', 'Data Scientist']
    locations = ['New York', 'San Francisco', 'London', 'Berlin', 'Sydney', 'Toronto']

    employee_data = {
        "employee_id": fake.uuid4(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "department": random.choice(departments),
        "role": random.choice(roles),
        "location": random.choice(locations),
        "hire_date": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
        "salary": round(random.uniform(50000, 150000), 2),
        "is_active": random.choice([True, False])
    }

    return json.dumps(employee_data, indent=4)
