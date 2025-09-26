#!/usr/bin/env python
"""
Django Project Setup Script
Run this script to set up the Django project for the first time.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(e.stderr if e.stderr else str(e))
        return False

def main():
    print("🚀 Benedict's Portfolio - Django Setup Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("❌ Error: manage.py not found. Please run this script from the Django project root directory.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️ Warning: Failed to install dependencies. You may need to install them manually.")
    
    # Make migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        print("❌ Failed to create migrations. Please check your models.")
        return
    
    # Apply migrations
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("❌ Failed to apply migrations. Please check your database configuration.")
        return
    
    # Create superuser prompt
    print("\n👤 Creating superuser account...")
    print("You'll be prompted to create an admin account for the Django admin interface.")
    try:
        subprocess.run([sys.executable, "manage.py", "createsuperuser"], check=True)
        print("✅ Superuser created successfully!")
    except subprocess.CalledProcessError:
        print("⚠️ Superuser creation was skipped or failed.")
    
    # Collect static files (for production-like setup)
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Your Django portfolio is ready to use!")
    print("\nNext steps:")
    print("1. Run 'python manage.py runserver' to start the development server")
    print("2. Visit http://127.0.0.1:8000/ to view your portfolio")
    print("3. Visit http://127.0.0.1:8000/admin/ to manage content")
    print("4. Add your projects, skills, and personal info through the admin interface")
    print("\n📝 Note: Remember to update your .env file with your actual configuration.")

if __name__ == "__main__":
    main()