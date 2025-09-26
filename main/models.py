from django.db import models
from django.core.validators import URLValidator, EmailValidator
from django.utils import timezone


class Skill(models.Model):
    """Model for technical skills"""
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('frontend', 'Frontend'),
            ('backend', 'Backend'),
            ('database', 'Database'),
            ('framework', 'Framework'),
            ('tool', 'Tool'),
            ('other', 'Other'),
        ],
        default='other'
    )
    proficiency_level = models.IntegerField(
        choices=[
            (1, 'Beginner'),
            (2, 'Intermediate'),
            (3, 'Advanced'),
            (4, 'Expert'),
        ],
        default=2
    )
    is_featured = models.BooleanField(default=True, help_text="Show on main page")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    """Model for portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="URL-friendly version of title")
    short_description = models.TextField(
        max_length=300,
        help_text="Brief description for project cards"
    )
    detailed_description = models.TextField(
        blank=True,
        help_text="Detailed project description"
    )
    
    # Project links
    live_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="Live project URL"
    )
    github_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="GitHub repository URL"
    )
    
    # Project media
    featured_image = models.ImageField(
        upload_to='projects/',
        blank=True,
        help_text="Main project screenshot"
    )
    demo_video = models.FileField(
        upload_to='projects/videos/',
        blank=True,
        help_text="Optional demo video"
    )
    
    # Project metadata
    technologies = models.ManyToManyField(
        Skill,
        blank=True,
        help_text="Technologies used in this project"
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # Display settings
    is_featured = models.BooleanField(
        default=False,
        help_text="Show as featured project"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Show on website"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order for displaying projects (lower numbers first)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('project_detail', kwargs={'slug': self.slug})

    @property
    def is_ongoing(self):
        return self.start_date and not self.end_date


class ContactMessage(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    
    # Optional fields for categorization
    inquiry_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Inquiry'),
            ('job', 'Job Opportunity'),
            ('collaboration', 'Collaboration'),
            ('feedback', 'Feedback'),
            ('other', 'Other'),
        ],
        default='general'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject or 'Contact Message'}"

    @property
    def short_message(self):
        return self.message[:100] + "..." if len(self.message) > 100 else self.message


class PersonalInfo(models.Model):
    """Model for personal information (singleton pattern)"""
    full_name = models.CharField(max_length=100, default="Benedict Nii Odartey Mensah")
    preferred_name = models.CharField(max_length=50, default="Benny")
    title = models.CharField(max_length=100, default="Full-Stack Developer")
    
    # Bio sections
    hero_description = models.TextField(
        help_text="Main description for hero section"
    )
    about_description = models.TextField(
        help_text="Detailed about section"
    )
    
    # Contact information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Social media links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Professional links
    resume_file = models.FileField(upload_to='documents/', blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Profile image
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Personal Information'
        verbose_name_plural = 'Personal Information'

    def __str__(self):
        return f"{self.full_name} - Personal Info"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        if not self.pk and PersonalInfo.objects.exists():
            raise ValueError('PersonalInfo instance already exists')
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get the single PersonalInfo instance"""
        instance, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'full_name': 'Benedict Nii Odartey Mensah',
                'preferred_name': 'Benny',
                'title': 'Full-Stack Developer',
                'hero_description': "Hi, I'm Benny! I'm a full-stack developer skilled in Python, Django, HTML, CSS, and JavaScript.",
                'about_description': "I began with backend development but expanded into full-stack so I could design and build complete web applications.",
                'email': 'benymento4@gmail.com',
            }
        )
        return instance


class BlogPost(models.Model):
    """Model for optional blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    
    # Categories and tags
    category = models.CharField(
        max_length=50,
        choices=[
            ('tech', 'Technology'),
            ('tutorial', 'Tutorial'),
            ('personal', 'Personal'),
            ('project', 'Project Update'),
        ],
        default='tech'
    )
    tags = models.ManyToManyField(Skill, blank=True)
    
    # Publishing
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)