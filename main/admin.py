from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Skill, Project, ContactMessage, PersonalInfo, BlogPost


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency_level', 'is_featured', 'created_at']
    list_filter = ['category', 'proficiency_level', 'is_featured']
    search_fields = ['name']
    list_editable = ['is_featured', 'proficiency_level']
    ordering = ['category', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'category')
        }),
        ('Skill Level', {
            'fields': ('proficiency_level', 'is_featured')
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_published', 'display_order', 'created_at']
    list_filter = ['is_featured', 'is_published', 'technologies', 'created_at']
    search_fields = ['title', 'short_description']
    list_editable = ['is_featured', 'is_published', 'display_order']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    date_hierarchy = 'created_at'
    ordering = ['display_order', '-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description')
        }),
        ('Detailed Information', {
            'fields': ('detailed_description', 'technologies'),
            'classes': ('collapse',)
        }),
        ('Project Links', {
            'fields': ('live_url', 'github_url')
        }),
        ('Media', {
            'fields': ('featured_image', 'demo_video')
        }),
        ('Project Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_published', 'display_order')
        }),
    )
    
    def get_featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover;" />',
                obj.featured_image.url
            )
        return "No image"
    get_featured_image_preview.short_description = 'Image Preview'
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'inquiry_type', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'inquiry_type', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_replied']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'inquiry_type')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied', 'created_at')
        }),
    )
    
    def get_short_message(self, obj):
        return obj.short_message
    get_short_message.short_description = 'Message Preview'
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(is_replied=True)
        self.message_user(request, f"{queryset.count()} messages marked as replied.")
    mark_as_replied.short_description = "Mark selected messages as replied"


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'email', 'is_active', 'updated_at']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'preferred_name', 'title', 'profile_image')
        }),
        ('Descriptions', {
            'fields': ('hero_description', 'about_description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Media', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Professional Links', {
            'fields': ('resume_file', 'portfolio_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not PersonalInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of the single instance
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'published_at', 'created_at']
    list_filter = ['category', 'is_published', 'tags', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'featured_image')
        }),
        ('Classification', {
            'fields': ('category', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_published_status(self, obj):
        if obj.is_published:
            return format_html('<span style="color: green;">✓ Published</span>')
        return format_html('<span style="color: red;">✗ Draft</span>')
    get_published_status.short_description = 'Status'


# Customize admin site
admin.site.site_header = "Benedict's Portfolio Administration"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to your Portfolio Admin Panel"