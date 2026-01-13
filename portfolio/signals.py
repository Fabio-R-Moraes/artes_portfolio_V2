import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from portfolio.models import Photos

def delete_image(instance):
    try:
        os.remove(instance.photo_image.path)
    except(ValueError, FileNotFoundError) as e:
        print(e)

@receiver(pre_delete, sender=Photos)
def photo_image_delete(sender, instance, *args, **kwargs):
    #print('Signal chamado pela Photo...')
    old_instance = Photos.objects.filter(pk = instance.pk).first()

    if old_instance:
        delete_image(old_instance)

@receiver(pre_save, sender=Photos)
def photo_image_update(sender, instance, *args, **kwargs):
    old_instance = Photos.objects.filter(pk = instance.pk).first()
    #print(old_instance.photo_image, instance.photo_image)

    if not old_instance:
        return
    
    new_image = old_instance.photo_image != instance.photo_image
    #print('Troquei a image??', new_image)

    if new_image:
        delete_image(old_instance)