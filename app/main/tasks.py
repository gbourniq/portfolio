from celery import shared_task
import time
import socket


def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return f"Hostname: {host_name} - IP: {host_ip}"
    except Exception:
        return "Unable to get Hostname and IP"


@shared_task
def celery_function_test():
    """ Time consumming task to be run asynchronously
    and Python3 code to display hostname and IP address """
    time.sleep(5)
    host_info = get_Host_name_IP()
    return f"Celery working fine on: {host_info}"
