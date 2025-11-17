# mameno_mtf Backend (Flask App)

This is the backend component of the **mameno_mtf** project, built using the Flask framework. It provides a web interface and RESTful API for managing internal documents, complaints, user authentication, and certification tracking.

## 🧩 Features

- User authentication (login/signup)
- CRUD operations for:
  - Internal memos (`tbl_memo`)
  - Purchase forms (`tbl_beli`)
  - Shared notes (`tbl_bersama`)
  - Complaints (`dbcomp`, `dbfucomp`)
  - Certification records (`dbsppi`)
- Dashboard with Plotly visualizations
- Export data to CSV
- REST API endpoint for adding SPPI records
- Admin-only historical data entry

## 🛠️ Tech Stack

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database models
- **Flask-WTF**: Form handling
- **Flask-Migrate**: Database migrations
- **Flask-Bootstrap**: UI styling
- **Plotly**: Data visualization
- **Pandas**: Data manipulation
- **SQLite / SQLAlchemy-compatible DB**: Database backend

## 📦 Installation

1. Clone the repository:
   ```
   git clone https://github.com/timgio26/mameno_mtf.git
   cd mameno_mtf/backend
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. Configure the app:
   - Create a `config.py` file with your database URI and secret key.

4. Run the app:
   ```
   flask run
   ```

## 🔐 Authentication

- Users can sign up and log in via `/daftar` and `/masuk`.
- Session-based authentication is used to restrict access to certain routes.

## 📊 Dashboard

- Accessible via `/dashboard`
- Displays complaint statistics using bar and pie charts.

## 📤 Exporting Data

- Use `/download/<type>` to export data as CSV.
  - Supported types: `nota`, `memo`, `beli`, `sppi`, `telecol`

## 📮 REST API

- `POST /api/<inp_nip>/<inp_nama>`: Add new SPPI record

## 📁 File Structure

```
backend/
├── flask_app.py         # Main Flask application
├── templates/           # HTML templates
├── static/              # Static assets
├── requirements.txt     # Python dependencies
└── config.py            # Configuration file (user-defined)
```

## 🧪 Development Notes

- All database models are defined in `flask_app.py`
- Routes are grouped by functionality (complaints, memos, SPPI, etc.)
- Form classes are defined using Flask-WTF
- Plotly charts are embedded using JSON serialization

## 📜 License

This project is open-source under the MIT License.

---
