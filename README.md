# Restaurant Project

A Django-based restaurant ordering app with menu browsing, cart management, order checkout, user registration, and a restaurant staff dashboard.

## Features

- Menu listing with categories
- Add menu items to a cart with quantity and notes
- Place orders as a registered user or guest
- Custom user model with username, email, and phone number
- Restaurant dashboard for staff to view and manage orders
- Order status updates: Pending, Accepted, Ready, Delivered
- Guest email notification when an order is accepted (console email backend by default)
- Order history for logged-in users

## Project Structure

- `restaurant/` - Django project settings and URL configuration
- `orders/` - Main application containing models, views, forms, templates, and URLs
- `templates/` - HTML templates for menu, cart, order flow, registration, and dashboard
- `static/` - Static assets such as CSS
- `media/` - Folder for uploaded menu images
- `db.sqlite3` - Default SQLite database file

## Requirements

- Python 3.11+ (recommended)
- Django 4.2
- requests

Dependencies are listed in `requirements.txt`.

## Setup

1. Activate the virtual environment:

   ```powershell
   .\env\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```powershell
   python manage.py migrate
   ```

4. Create a superuser for admin and restaurant dashboard access:

   ```powershell
   python manage.py createsuperuser
   ```

5. Run the development server:

   ```powershell
   python manage.py runserver
   ```

6. Open the app in your browser:

   - Main menu: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

- Browse menu items and filter by category
- Add items to the cart and proceed to checkout
- Register a new user or place an order as a guest
- Staff users can access the restaurant dashboard to update order status
- Logged-in users can view their order history

## Notes

- `DEBUG` is currently enabled in `restaurant/settings.py`. Disable it for production.
- The email backend is configured to use `console.EmailBackend` for development.
- Media settings are present but commented out in `restaurant/settings.py`; uncomment and configure `MEDIA_URL` and `MEDIA_ROOT` if you want to use uploaded images.
- The app uses `AUTH_USER_MODEL = 'orders.CustomUser'`.

## Customization

- Add menu items through the Django admin interface.
- Update categories and menu item details in `orders/models.py` if needed.
- Customize templates under `orders/templates/` to change the UI.

## Useful Commands

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```