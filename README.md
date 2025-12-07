# University Open Day System (FastAPI)

⚠️ **Archival Project**
*An event management system built to support University Open Days. This project demonstrates the implementation of a modular REST API using Python and FastAPI.*

## 🛠 Tech Stack
* **Framework:** FastAPI (Modern, high-performance web framework for building APIs).
* **Architecture:** Modular design using `APIRouter` (located in `src/routers`).
* **Templating:** Jinja2 for frontend rendering.

## 📂 Project Structure
The project follows a scalable structure separating routing logic from templates:
* `src/routers/` - Contains separate route modules (separation of concerns).
* `templates/` - HTML templates used for the web interface.
* `prepare_database_templates/` - Scripts for initial database setup.

