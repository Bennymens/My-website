from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('work/', views.work, name='work'),
    
    # Projects
    path('projects/', views.projects_list, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # Blog (commented out until templates are ready)
    # path('blog/', views.BlogListView.as_view(), name='blog'),
    # path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    
    # API endpoints
    path('api/projects/', views.api_projects, name='api_projects'),
]