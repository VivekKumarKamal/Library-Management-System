from celery import Celery
from celery.schedules import crontab
import requests
from datetime import datetime, timedelta
from .models import User, Request, Ebook

celery = Celery('tasks', broker='redis://localhost:6555/0', backend='redis://localhost:6555/0')

def send_gchat_message(message):
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAZJPxISs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=59UjdPu-liJVdq5lLvEAWkoukUfuPw_Hspq6MQTA_wc"
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
    }
    data = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Message sent successfully! Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message. Error: {str(e)}")
        print(f"Response content: {e.response.content if e.response else 'No response'}")

@celery.task
def send_daily_reminders():
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    due_requests = Request.query.filter(Request.status == 'granted', Request.due_date <= tomorrow).all()
    
    if due_requests:
        message = "Reminder: The following books are due tomorrow:\n"
        for request in due_requests:
            user = User.query.get(request.user_id)
            ebook = Ebook.query.get(request.ebook_id)
            message += f"- {user.name}: '{ebook.title}' (Due: {request.due_date.strftime('%Y-%m-%d')})\n"
    else:
        message = "No books are due tomorrow, but this is a test message."
    
    send_gchat_message(message)

@celery.task
def send_monthly_report():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    borrowed_books = Request.query.filter(Request.status == 'granted', Request.issue_date >= start_date).count()
    returned_books = Request.query.filter(Request.status == 'returned', Request.return_date >= start_date).count()
    
    message = f"Monthly Library Activity Report\n"
    message += f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n\n"
    message += f"Summary:\n"
    message += f"- Books borrowed: {borrowed_books}\n"
    message += f"- Books returned: {returned_books}\n"
    
    if borrowed_books == 0 and returned_books == 0:
        message += "\nNo activity in the last 30 days, but this is a test message."
    
    send_gchat_message(message)

@celery.task
def test_task():
    print("Test task executed")
    send_gchat_message("Test message from Celery task")

celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'backend.python_files.celery_config.send_daily_reminders',
        'schedule': 60.0,  # Run every 60 seconds
    },
    'send-monthly-report': {
        'task': 'backend.python_files.celery_config.send_monthly_report',
        'schedule': 120.0,  # Run every 121 seconds
    },
    'test-task': {
        'task': 'backend.python_files.celery_config.test_task',
        'schedule': 29.0,  # Run every 29 seconds
    }
}

celery.conf.timezone = 'UTC'