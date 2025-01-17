# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# from datetime import datetime, timedelta
# # from sqlalchemy.orm import Session
# from . import models

# # The function that will be called by APScheduler
# def delete_old_items(db):
#     """Delete items that are created more than 5 minutes ago."""
#     five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
#     deleted_count = db.query(models.CachedStudy).filter(models.CachedStudy.created_date < five_minutes_ago).delete(synchronize_session=False)
#     db.commit()
#     print(f"{deleted_count} items deleted.")

# # Initialize the scheduler
# def start_scheduler(db):
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(
#         delete_old_items,
#         trigger=IntervalTrigger(seconds=60),  # Run every 60 seconds
#         args=[db],  # Pass the db session as argument to the function
#         id='delete_old_items_job',
#         replace_existing=True
#     )

#     # Start the scheduler
#     scheduler.start()

#     print("Scheduler started.")
