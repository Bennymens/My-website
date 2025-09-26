from django.test import TestCase
from django.urls import reverse
from django.core import mail
from .models import Project, Skill, ContactMessage, PersonalInfo
from .forms import ContactForm


class HomePageTest(TestCase):
    def setUp(self):
        self.personal_info = PersonalInfo.get_instance()
        self.skill = Skill.objects.create(name='Python', category='backend')
        self.project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            short_description='A test project',
            is_published=True
        )
    
    def test_home_page_loads(self):
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.personal_info.full_name)
    
    def test_home_page_shows_projects(self):
        response = self.client.get(reverse('main:home'))
        self.assertContains(response, self.project.title)


class ContactFormTest(TestCase):
    def test_contact_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message',
            'inquiry_type': 'general'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_contact_form_submission(self):
        response = self.client.post(reverse('main:contact'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Hello, this is a test message',
            'inquiry_type': 'general'
        })
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.first()
        self.assertEqual(message.name, 'Jane Doe')


class ProjectModelTest(TestCase):
    def test_project_str(self):
        project = Project(title='My Project')
        self.assertEqual(str(project), 'My Project')
    
    def test_project_absolute_url(self):
        project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            short_description='Test description'
        )
        self.assertEqual(project.get_absolute_url(), '/project/test-project/')