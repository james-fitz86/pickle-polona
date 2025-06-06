# 🥒 Homemade Pickle Store – Admin Web App

A full-featured Flask web application for managing a homemade pickle store. The app allows admins to manage products, stock batches, orders, and customer messages through a clean, accessible dashboard. Designed with usability, accessibility, and maintainability in mind. Deployed on **Render.com**.

## ✨ Features
- 📦 **Order Management** – View, fulfill, ship orders, and generate picklists  
- 🥫 **Stock Tracking** – Add/edit batches with expiry, location, and quantity  
- 🛍️ **Product Management** – Add/edit product info and categorise inventory  
- 🗃️ **Database-Backed** – SQLAlchemy models for products, orders, and batches  
- 🧑‍💻 **Admin Access Only** – All routes protected by environment-secured login  
- ♿ **Accessible UI** – ARIA labels, semantic headings, and keyboard-friendly  
- 🖨️ **Printable Picklists** – Generate real-time picklists from stock batches  
- 💬 **Contact Messages** – Paginated user feedback viewer for admins  
- 🗺️ **SEO Aware** – Includes `robots.txt` and `sitemap.xml`  
- 🚀 **Live on Render** – Deployed online with environment configuration  

## 🧰 Technologies Used
- **Backend:** Flask, SQLAlchemy, Python  
- **Frontend:** HTML, CSS (Bootstrap), JavaScript  
- **Deployment:** Render.com  
- **Database:** PostgreSQL
- **Forms:** Flask-WTF with CSRF protection  


## 📁 File Structure

```plaintext
pickle-polona/
├── app.py                    # Flask app entry point
├── config.py                 # Config settings
├── .env                      # Environment variables (not committed)
├── .gitignore                # Excludes .env, .DS_Store, etc.
├── requirements.txt          # Python dependencies
├── extensions.py             # Initialises shared extensions (e.g. SQLAlchemy) to avoid circular imports
├── static/                   # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── errors/               
│   │   ├── 404.html
│   │   └── 500.html
│   ├── admin/                       # Admin-facing templates
│   │   ├── add_product.html
│   │   ├── admin_login.html
│   │   ├── dashboard.html
│   │   ├── edit_product.html
│   │   ├── login.html
│   │   ├── messages.html
│   │   ├── order_detail.html
│   │   ├── orders.html
│   │   ├── picklist.html
│   │   ├── product_detail.html
│   │   ├── products.html
│   │   ├── stock_batch_add.html
│   │   ├── stock_batch_edit.html
│   │   └── stock_batches.html
│   ├── about.html
│   ├── base_admin.html       # Shared layout for admin pages
│   ├── base.html
│   ├── cart.html
│   ├── checkout.html
│   ├── contact.html
│   ├── index.html
│   ├── item.html
│   ├── order_success.html
│   └── store.html
├── models/                   # SQLAlchemy models
│   ├── __init__.py
│   ├── admin_model.py
│   ├── main_model.py
│   ├── product.py
│   └── store_model.py
├── forms/                    # Flask-WTF form classes
│   ├── checkout_form.py
│   ├── contact_form.py
│   ├── product_form.py
│   └── stock_form.py
├── routes/                   # Blueprints
│   ├── __init__.py
│   ├── admin.py
│   ├── main.py
│   └── store.py
├── README.md                 # Project Documentation
├── robots.txt
└── sitemap.xml
```

## Setup & Installation
### 1. Clone the Repository
```bash
git clone https://github.com/james-fitz86/pickle-polona.git
cd pickle-polona
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

#### Activate Virtual Environment
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Create a `.env` file
Create a `.env` file in the root of the project directory to store sensitive configuration values. The following variables are required:

- **ADMIN_USERNAME**: Set the username for the admin login page.
- **ADMIN_PASSWORD**: Set the password for the admin login page.
- **SECRET_KEY**: Set a secret key for Flask's session management (used for securing cookies and sessions).
- **MESSAGES_PER_PAGE**: Set the number of messages displayed **per page** in the admin messages panel for pagination. 
- **DATABASE_URL**: Provide the connection string for your PostgreSQL database in the format:
`postgresql://your_username:your_password@localhost:5432/your_database_name`

Example `.env` file

```dotenv
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_admin_password
SECRET_KEY=your_secret_key
MESSAGES_PER_PAGE=10
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database_name
```


### 5. Run the Flask Application
In `app.py`, ensure you have the following at the bottom of your file to run the app locally:

```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

Then run the app with:
```bash
python app.py
```

Access the website locally at `http://127.0.0.1:8080/`

## Deployment to Render

1. Push your code to **GitHub**  
2. Sign up or log in at [Render.com](https://render.com/)  
3. Click **"New +"** and select **"Web Service"**  
4. Connect your **GitHub repository** and choose the appropriate branch  
5. Fill in the **Web Service** setup:
   - **Name:** e.g., `pickle-admin`
   - **Runtime:** `Python 3`
   - **Build Command:**  
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**  
     ```bash
     gunicorn app:app
     ```

6. Under the **Environment** tab, set the following environment variables (click **"Add Environment Variable"** for each one):
   - `ADMIN_USERNAME=your_username`  
   - `ADMIN_PASSWORD=your_password`  
   - `SECRET_KEY=your_secret_key`
   - `MESSAGES_PER_PAGE=set_messages_per_page` 
   - `DATABASE_URL` (you'll set this after creating the database in step 7)

7. In a new tab on Render:
   - Click **"New +"** > **"PostgreSQL"**
   - Give it a name (e.g., `pickle-db`)
   - Choose your **region** and **plan** (the free plan is fine for testing)
   - Once created, go to the **"Connection"** tab
   - Copy the **Internal Database URL** or **External Database URL**
   - Return to your **Web Service** settings and **add this as the value for `DATABASE_URL`**

8. Click **"Save Changes"** and then **"Deploy"** your web service  
9. Your app will build and deploy — visit the live link provided by Render when it's complete 🚀

> 🛑 **Important:** Never commit your `.env` file to GitHub — it should be listed in `.gitignore`.


## 🌐 Live Demo

Check out the live version of this project on Render:  
👉 [https://picklepolona.onrender.com/]