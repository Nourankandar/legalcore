from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Notification
from apps.contracts.models import Contract

@shared_task
def check_upcoming_deadlines():
    today = timezone.now().date()
    seven_days_later = today + timedelta(days=7)

    upcoming_contracts = Contract.objects.filter(
        status ='ACTIVE' ,
        deadline__range=[today, seven_days_later]
        ).prefetch_related('parties')
    
    # print(upcoming_contracts)
    notifications_to_create = []
    for contract in upcoming_contracts:
        for user in contract.parties.all():
            already_notified = Notification.objects.filter(
                recipient=user,
                contract=contract,
                is_read=False
            ).exists()
            if not already_notified:
                notification = Notification(
                    recipient=user,
                    contract=contract,
                    message=f"The contract '{contract.title}' is approaching its deadline on {contract.deadline}."
                )
                notifications_to_create.append(notification)
    if notifications_to_create:
        Notification.objects.bulk_create(notifications_to_create)