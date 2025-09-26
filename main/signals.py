from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Project, Skill, PersonalInfo, ContactMessage
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Project)
def clear_project_cache(sender, instance, **kwargs):
    """Clear cache when project is saved"""
    cache.delete('featured_projects')
    cache.delete('all_projects')
    logger.info(f"Cache cleared for project: {instance.title}")


@receiver(post_save, sender=Skill)
def clear_skills_cache(sender, instance, **kwargs):
    """Clear cache when skill is saved"""
    cache.delete('featured_skills')
    cache.delete('all_skills')
    logger.info(f"Cache cleared for skill: {instance.name}")


@receiver(post_save, sender=PersonalInfo)
def clear_personal_info_cache(sender, instance, **kwargs):
    """Clear cache when personal info is updated"""
    cache.delete('personal_info')
    logger.info("Personal info cache cleared")


@receiver(post_save, sender=ContactMessage)
def log_new_contact_message(sender, instance, created, **kwargs):
    """Log when a new contact message is received"""
    if created:
        logger.info(f"New contact message received from {instance.name} ({instance.email})")