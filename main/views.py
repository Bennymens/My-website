from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Q
import json
import logging

from .models import Project, Skill, ContactMessage, PersonalInfo, BlogPost
from .forms import ContactForm

logger = logging.getLogger(__name__)


def home(request):
    """Home page view with all sections"""
    try:
        personal_info = PersonalInfo.get_instance()
        featured_projects = Project.objects.filter(
            is_published=True, 
            is_featured=True
        )[:1]  # Get only the most featured project
        
        projects = Project.objects.filter(is_published=True)[:6]
        skills = Skill.objects.filter(is_featured=True).order_by('category', 'name')
        
        # Group skills by category
        skills_by_category = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(skill)
        
        context = {
            'personal_info': personal_info,
            'featured_project': featured_projects.first() if featured_projects else None,
            'projects': projects,
            'skills': skills,
            'skills_by_category': skills_by_category,
            'contact_form': ContactForm(),
        }
        
        return render(request, 'home.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        # Return a minimal context in case of error
        context = {
            'personal_info': PersonalInfo.get_instance(),
            'projects': [],
            'skills': [],
            'contact_form': ContactForm(),
        }
        return render(request, 'home.html', context)


def projects_list(request):
    """All projects page"""
    projects = Project.objects.filter(is_published=True)
    
    # Filter by technology if specified
    tech_filter = request.GET.get('tech')
    if tech_filter:
        projects = projects.filter(technologies__name__icontains=tech_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(detailed_description__icontains=search_query)
        )
    
    # Get all technologies for filter dropdown
    all_technologies = Skill.objects.filter(
        project__is_published=True
    ).distinct().order_by('name')
    
    # Redirect to home page for now since we don't have a projects list template
    return redirect('home')

    context = {
        'projects': projects,
        'all_technologies': all_technologies,
        'current_tech_filter': tech_filter,
        'search_query': search_query,
    }


def project_detail(request, slug):
    """Individual project detail page"""
    project = get_object_or_404(Project, slug=slug, is_published=True)
    
    # Get related projects (same technologies)
    related_projects = Project.objects.filter(
        technologies__in=project.technologies.all(),
        is_published=True
    ).exclude(id=project.id).distinct()[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'project_detail.html', context)


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact form handling"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save the contact message
                contact_message = form.save()
                
                # Send email notification (optional)
                try:
                    send_mail(
                        subject=f"New Contact Form Submission: {contact_message.subject}",
                        message=f"""
                        New message from your portfolio website:
                        
                        Name: {contact_message.name}
                        Email: {contact_message.email}
                        Subject: {contact_message.subject}
                        
                        Message:
                        {contact_message.message}
                        """,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.EMAIL_HOST_USER],
                        fail_silently=True,
                    )
                except Exception as email_error:
                    logger.warning(f"Failed to send email notification: {str(email_error)}")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Thank you for your message! I\'ll get back to you soon.'
                    })
                else:
                    messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
                    return redirect('home')
                    
            except Exception as e:
                logger.error(f"Error saving contact form: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Sorry, there was an error sending your message. Please try again.'
                    })
                else:
                    messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please check your form for errors.',
                    'errors': form.errors
                })
            else:
                messages.error(request, 'Please check your form for errors.')
    
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'personal_info': PersonalInfo.get_instance(),
    }
    
    return render(request, 'contact.html', context)


# TODO: Implement these views when templates are ready
# class BlogListView(ListView):
#     """Blog posts list view"""
#     model = BlogPost
#     template_name = 'blog.html'
#     context_object_name = 'posts'
#     paginate_by = 6
    
#     def get_queryset(self):
#         return BlogPost.objects.filter(is_published=True)


# class BlogDetailView(DetailView):
#     """Individual blog post view"""
#     model = BlogPost
#     template_name = 'blog_detail.html'
#     context_object_name = 'post'
    
#     def get_queryset(self):
#         return BlogPost.objects.filter(is_published=True)


def about(request):
    """About page - redirect to home for now"""
    return redirect('home')


def work(request):
    """Work/Portfolio page showcasing all projects"""
    try:
        projects = Project.objects.filter(is_published=True).order_by('-created_at')
        featured_projects = projects.filter(is_featured=True)
        
        context = {
            'projects': projects,
            'featured_projects': featured_projects,
        }
        
        return render(request, 'work.html', context)
        
    except Exception as e:
        logger.error(f"Error in work view: {str(e)}")
        messages.error(request, "An error occurred loading the work page.")
        return redirect('main:home')


def api_projects(request):
    """API endpoint for projects (for AJAX loading)"""
    projects = Project.objects.filter(is_published=True)
    
    projects_data = []
    for project in projects:
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'slug': project.slug,
            'description': project.description,
            'url': project.url,
            'github_url': project.github_url,
            'image': project.image.url if project.image else '',
            'technologies': [tech.name for tech in project.technologies.all()],
            'is_featured': project.is_featured,
        })
    
    return JsonResponse({'projects': projects_data})


def handler404(request, exception):
    """Custom 404 error handler - redirect to home for now"""
    return redirect('home')


def handler500(request):
    """Custom 500 error handler - redirect to home for now"""
    return redirect('home')