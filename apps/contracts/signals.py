from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Contract
from apps.audit.models import AuditLog
from django.forms.models import model_to_dict

@receiver(post_save, sender=Contract)
def track_contract_changes (sender, instance, created, **kwargs):
    if created:
        action = 'created'
        extra_data = model_to_dict(instance)
    
    else:
        action = 'update'
        extra_data = {}

        try:
            old_instance = Contract.objects.get(pk=instance.pk)
            old_data=model_to_dict(old_instance)
            new_data=model_to_dict(instance)
            for field, new_value in new_data.items():
                old_value = old_data.get(field)
                if old_value != new_value:
                    extra_data={
                        'before': str(old_value),
                        'after': str(new_value)
                    }
        except Contract.DoesNotExist:
            pass

    AuditLog.objects.create(
        user=getattr(instance, '_current_user', None), 
        contract=instance,
        action=action,
        extra_data=extra_data
    )
@receiver(post_delete,sender=Contract)
def track_contract_deletion(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=getattr(instance, '_current_user', None), 
        contract=None,
        action='DELETE',
        extra_data={'deleted_contract_title': instance.title}
    )
