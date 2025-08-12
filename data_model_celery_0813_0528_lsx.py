# 代码生成时间: 2025-08-13 05:28:26
import os
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configure the Celery application
os.environ.setdefault('CELERY_BROKER_URL', 'amqp://guest:guest@localhost//')
os.environ.setdefault('CELERY_RESULT_BACKEND', 'rpc://')
app = Celery('data_model_celery', broker=os.environ['CELERY_BROKER_URL'])
app.conf.broker_url = os.environ['CELERY_BROKER_URL']
app.conf.result_backend = os.environ['CELERY_RESULT_BACKEND']

# Data Model Configuration
DATABASE_URI = 'sqlite:///./celery_data_model.db'  # Using SQLite for simplicity
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the data model
class DataModel(Base):
    __tablename__ = 'data_model'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DataModel(id={self.id}, name='{self.name}', created_at='{self.created_at}')>"

# Initialize the database tables
Base.metadata.create_all(engine)

# Celery task to create a new data model entry
@app.task(bind=True, soft_time_limit=10)
def create_data_model_entry(self, name):
    """Create a new data model entry in the database."""
    try:
        # Create a new session
        session = Session()
        # Create a new data model instance
        data_model = DataModel(name=name)
        # Add the instance to the session
        session.add(data_model)
        # Commit the transaction
        session.commit()
        # Return the created data model id
        return data_model.id
    except Exception as e:
        # Handle any exceptions and re-raise them to be caught by Celery
        self.retry(exc=e)
    finally:
        # Close the session
        session.close()

# Example usage of the task
if __name__ == '__main__':
    try:
        # Start the Celery worker
        app.worker_main()
    except SoftTimeLimitExceeded:
        print("The Celery worker timed out.")
    