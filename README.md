# Benedict Nii Odartey Mensah - Portfolio Website

A full-stack Django portfolio website showcasing projects, skills, and professional experience. Built with modern web technologies and responsive design principles.

## 🌟 Features

- **Responsive Design**: Mobile-first approach with optimized layouts for all devices
- **Dynamic Content**: Django-powered backend for easy content management
- **Project Showcase**: Detailed project pages with images, technologies, and links
- **Contact System**: Working contact form with email notifications
- **Admin Interface**: Full Django admin for content management
- **SEO Optimized**: Meta tags, Open Graph, and Twitter Card support
- **Modern UI**: Clean, professional design with smooth animations
- **Performance**: Optimized for fast loading and smooth interactions

## 🛠️ Technologies Used

### Backend

- **Django 4.2+**: Web framework
- **Python 3.8+**: Programming language
- **SQLite**: Database (PostgreSQL ready)
- **Pillow**: Image processing

### Frontend

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript**: Interactive functionality
- **Responsive Design**: Mobile-first approach

### Development

- **Django Debug Toolbar**: Development debugging
- **Whitenoise**: Static file serving
- **Gunicorn**: WSGI server for production

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd portfolio_project
   ```

2. **Create a virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Run the setup script**

   ```bash
   python setup.py
   ```

   This will:

   - Install all dependencies
   - Create database migrations
   - Set up the database
   - Create a superuser account
   - Collect static files

4. **Start the development server**

   ```bash
   python manage.py runserver
   ```

5. **Visit your portfolio**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
portfolio_project/
├── portfolio_project/          # Main project directory
│   ├── settings.py            # Django settings
│   ├── urls.py               # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── .env                 # Environment variables
├── main/                     # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View controllers
│   ├── forms.py             # Form definitions
│   ├── admin.py             # Admin configuration
│   └── urls.py              # App URLs
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── home.html           # Homepage
│   ├── project_detail.html # Project details
│   └── contact.html        # Contact page
├── static/                  # Static files
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Images
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
├── setup.py                # Setup script
└── README.md               # This file
```

## 🎨 Customization

### Adding Content

1. **Access the admin interface** at http://127.0.0.1:8000/admin/
2. **Add Personal Information**: Update your bio, contact details, and profile image
3. **Create Projects**: Add your projects with descriptions, images, and links
4. **Add Skills**: List your technical skills with proficiency levels
5. **Manage Messages**: View contact form submissions

### Styling

- Edit `static/css/styles.css` to customize the design
- Update color scheme in CSS custom properties
- Modify layout in templates for structural changes

### Configuration

Update the `.env` file with your settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📧 Contact Form Setup

To enable email notifications for contact form submissions:

1. **Gmail Setup**:

   - Enable 2-factor authentication
   - Generate an App Password
   - Update `.env` with your credentials

2. **Other Email Providers**:
   - Update `EMAIL_HOST` in settings.py
   - Adjust port and TLS settings as needed

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI** and create an app
2. **Set environment variables** in Heroku config
3. **Add Procfile**:
   ```
   web: gunicorn portfolio_project.wsgi
   ```
4. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Traditional Server

1. **Install dependencies** on your server
2. **Set up PostgreSQL** (recommended for production)
3. **Configure Nginx** for static file serving
4. **Use Gunicorn** as WSGI server
5. **Set up SSL** with Let's Encrypt

## 🧪 Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

## 📱 Responsive Breakpoints

- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1024px
- **Desktop**: 1025px - 1200px
- **Large Desktop**: 1201px+

## 🔧 Environment Variables

| Variable              | Description       | Default               |
| --------------------- | ----------------- | --------------------- |
| `DEBUG`               | Enable debug mode | `True`                |
| `SECRET_KEY`          | Django secret key | Required              |
| `ALLOWED_HOSTS`       | Allowed hostnames | `localhost,127.0.0.1` |
| `EMAIL_HOST`          | SMTP server       | `smtp.gmail.com`      |
| `EMAIL_HOST_USER`     | Email username    | Optional              |
| `EMAIL_HOST_PASSWORD` | Email password    | Optional              |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 About the Developer

**Benedict Nii Odartey Mensah (Benny)**

- Full-stack Developer
- Passionate about creating innovative web solutions
- Email: benymento4@gmail.com
- GitHub: [bennymensah](https://github.com/bennymensah)

---

Made with ❤️ using Django and modern web technologies.
