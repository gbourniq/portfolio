from celery import shared_task
import time


@shared_task
def celery_function_test():
    """ Time consumming task to be run asynchronously """
    time.sleep(5)
    return "Celery working fine!"
