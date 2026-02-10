
import pandas as pd
from datetime import datetime, timedelta

def get_mock_plan_data(member_name):
    """
    Returns mock development plan data for visualization testing.
    In a real scenario, this would load from a database or Excel file.
    """
    today = datetime.now()
    
    # Create some date ranges relative to today
    last_week = today - timedelta(days=7)
    next_week = today + timedelta(days=7)
    next_month = today + timedelta(days=30)
    month_ago = today - timedelta(days=30)
    
    data = [
        {
            "Member": member_name,
            "Skill": "Python",
            "Category": "Backend",
            "Task": "Complete Advanced Python Course",
            "Start": month_ago,
            "Finish": last_week,
            "Status": "Done",
            "Completion": 100
        },
        {
            "Member": member_name, 
            "Skill": "Python",
            "Category": "Backend",
            "Task": "Refactor Legacy API Module",
            "Start": last_week,
            "Finish": next_week,
            "Status": "In Progress",
            "Completion": 45
        },
        {
            "Member": member_name,
            "Skill": "AWS",
            "Category": "DevOps",
            "Task": "Obtain AWS Practitioner Certification",
            "Start": today,
            "Finish": next_month,
            "Status": "In Progress",
            "Completion": 10
        },
        {
            "Member": member_name,
            "Skill": "React",
            "Category": "Frontend",
            "Task": "Build New Dashboard Component",
            "Start": next_week,
            "Finish": next_month + timedelta(days=15),
            "Status": "Not Started",
            "Completion": 0
        },
        {
            "Member": member_name,
            "Skill": "Docker",
            "Category": "DevOps",
            "Task": "Containerize Microservices",
            "Start": month_ago,
            "Finish": today - timedelta(days=1),
            "Status": "Overdue",
            "Completion": 80
        }
    ]
    
    return pd.DataFrame(data)
