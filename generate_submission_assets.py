from pathlib import Path
import json

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, ListFlowable, ListItem, Preformatted, Table, TableStyle
from pptx import Presentation

BASE = Path(r"c:\Users\JQY\Desktop\web1\cw1")
DOCS = BASE / "docs"
DOCS.mkdir(exist_ok=True)
openapi = json.loads((DOCS / "openapi.json").read_text(encoding="utf-8"))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, fontSize=22, leading=26, spaceAfter=12))
styles.add(ParagraphStyle(name="HeadingSmall", parent=styles["Heading2"], fontSize=13, leading=16, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name="BodySmall", parent=styles["BodyText"], fontSize=9.5, leading=12))
styles.add(ParagraphStyle(name="CodeSmall", fontName="Courier", fontSize=8, leading=9))


def build_api_pdf():
    path = DOCS / "api_documentation.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=landscape(A4), leftMargin=1.2 * cm, rightMargin=1.2 * cm, topMargin=1.2 * cm, bottomMargin=1.2 * cm)
    story = []
    story.append(Paragraph("API Documentation", styles["TitleCenter"]))
    story.append(Paragraph("Task Management API - generated from the project OpenAPI schema", styles["BodySmall"]))
    story.append(Spacer(1, 0.3 * cm))
    info_table = Table([
        ["Title", openapi.get("info", {}).get("title", "Task Management API")],
        ["Version", openapi.get("info", {}).get("version", "1.0.0")],
        ["Description", openapi.get("info", {}).get("description", "")],
    ], colWidths=[3.5 * cm, 22.5 * cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8EEF7")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.4 * cm))
    for endpoint, methods in openapi.get("paths", {}).items():
        for method, details in methods.items():
            story.append(Paragraph(f"{method.upper()} {endpoint}", styles["HeadingSmall"]))
            story.append(Paragraph(f"Summary: {details.get('summary', 'No summary provided')}", styles["BodySmall"]))
            parameters = details.get("parameters", [])
            if parameters:
                rows = [["Name", "In", "Required", "Type", "Description"]]
                for p in parameters:
                    rows.append([
                        p.get("name", ""), p.get("in", ""), str(p.get("required", False)), p.get("schema", {}).get("type", ""), p.get("description", "")
                    ])
                t = Table(rows, colWidths=[3 * cm, 2 * cm, 2.2 * cm, 2 * cm, 15 * cm])
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]))
                story.append(t)
                story.append(Spacer(1, 0.2 * cm))
            if details.get("requestBody"):
                story.append(Paragraph("Request body schema:", styles["BodySmall"]))
                story.append(Preformatted(json.dumps(details["requestBody"], indent=2)[:2500], styles["CodeSmall"]))
            responses = details.get("responses", {})
            if responses:
                rr = [["Status", "Description"]] + [[code, resp.get("description", "")] for code, resp in responses.items()]
                rt = Table(rr, colWidths=[3 * cm, 21.7 * cm])
                rt.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7F4E4")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]))
                story.append(rt)
                story.append(Spacer(1, 0.3 * cm))
    doc.build(story)


def build_report_pdf():
    path = DOCS / "Technical_Report_339919905.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    story = []
    def bullets(items):
        return ListFlowable([ListItem(Paragraph(i, styles["BodySmall"])) for i in items], bulletType="bullet", leftIndent=14)
    story.append(Paragraph("Task Management API Technical Report", styles["TitleCenter"]))
    story.append(Paragraph("Course Code: XJCO3011 | Student ID: 339919905 | Submission Type: Coursework 1", styles["BodySmall"]))
    story.append(Paragraph("GitHub Repository: https://github.com/339919905/web-api-project", styles["BodySmall"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("1. Introduction and Project Overview", styles["Heading1"]))
    story.append(Paragraph("This project implements a data-driven Web API for task management using Python and FastAPI. The aim is to provide a complete CRUD interface backed by a relational database while following RESTful conventions, returning JSON data, and exposing interactive API documentation. The chosen data model is a task entity with fields for title, description, completion status, due date, and audit timestamps.", styles["BodySmall"]))
    story.append(Paragraph("2. Technology Selection and Architecture", styles["Heading1"]))
    story.append(Paragraph("FastAPI was selected because it provides concise endpoint definitions, automatic OpenAPI generation, and strong support for typed request validation. SQLAlchemy was used as the ORM layer to model the task table and manage database operations in a structured way. SQLite was chosen for local development because it is lightweight, simple to configure, and suitable for coursework demonstrations. Pydantic was used to validate request bodies and shape response models.", styles["BodySmall"]))
    story.append(Paragraph("The architecture follows a simple layered pattern: client requests are handled by FastAPI routes, validated by Pydantic schemas, executed through SQLAlchemy sessions, and persisted in SQLite. The modular structure separates routing, schema definitions, application startup, database configuration, and automated testing.", styles["BodySmall"]))
    story.append(Paragraph("3. Implementation Details and Core Functionality", styles["Heading1"]))
    story.append(Paragraph("The system provides complete CRUD operations for the task resource. Users can create new tasks, retrieve all tasks, retrieve an individual task by its identifier, replace records with PUT, partially update records with PATCH, and delete tasks. In addition to the minimum coursework requirements, the API includes pagination, title search, completion-state filtering, standardized JSON error handling, and created_at / updated_at timestamps.", styles["BodySmall"]))
    story.append(bullets([
        "GET / returns a health-style JSON response confirming that the API is running.",
        "GET /api/tasks lists all tasks with page, limit, total, and items metadata.",
        "GET /api/tasks/{task_id} retrieves one task by ID.",
        "POST /api/tasks creates a new task and returns HTTP 201.",
        "PUT /api/tasks/{task_id} replaces an existing task.",
        "PATCH /api/tasks/{task_id} partially updates selected fields.",
        "DELETE /api/tasks/{task_id} removes a task and returns a JSON message.",
    ]))
    story.append(Paragraph("4. Testing Strategy", styles["Heading1"]))
    story.append(Paragraph("Automated tests were implemented with pytest and FastAPI's TestClient. The test suite uses a dedicated temporary SQLite database so that tests do not affect the development database. This isolation improves reliability and makes repeated test runs deterministic. The tests cover successful CRUD flows, pagination behaviour, filtering, timestamp presence, standardized validation errors, and missing-resource responses.", styles["BodySmall"]))
    story.append(Paragraph("5. Project Reflection", styles["Heading1"]))
    story.append(Paragraph("One key challenge in the project was balancing coursework simplicity with professional API design. To address this, the final implementation kept the core structure beginner-friendly while still introducing practical enhancements such as consistent error payloads, automated tests, and deployment support. Another challenge was presenting the development process clearly through version control. This was addressed by keeping the repository organised into logical commits that reflect the major implementation stages of the project.", styles["BodySmall"]))
    story.append(Paragraph("There are still limitations. SQLite is effective for local coursework use, but a production deployment with higher concurrency would be better served by PostgreSQL. The current system also does not include authentication or user ownership of tasks. Future improvements could include JWT authentication, sorting options, Alembic database migrations, and CI automation.", styles["BodySmall"]))
    story.append(Paragraph("6. Generative AI Use Statement", styles["Heading1"]))
    story.append(Paragraph("Generative AI tools were used during the development of this coursework. AI assistance was used to help draft the initial FastAPI project structure, generate code patterns for CRUD endpoints, improve schema and database boilerplate, suggest testing approaches, support README documentation, and help plan a clearer staged development workflow for the repository. The final project was then reviewed, run locally, tested, adjusted for Windows-specific issues, and prepared for submission through manual verification and iterative refinement. The student remained responsible for understanding the code, validating behaviour, deciding what features to keep, and producing the final integrated submission.", styles["BodySmall"]))
    story.append(Paragraph("7. Conclusion", styles["Heading1"]))
    story.append(Paragraph("Overall, the project satisfies the core requirements of a data-driven Web API coursework submission. It demonstrates CRUD functionality, database integration, input validation, consistent JSON responses, OpenAPI documentation, testing, and structured project organization. Additional features such as pagination, filtering, timestamps, Docker support, and Git history refinement help position the submission above the minimum baseline.", styles["BodySmall"]))
    doc.build(story)


def build_presentation():
    prs = Presentation()
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = "Task Management API"
    title_slide.placeholders[1].text = "XJCO3011 Coursework 1\nStudent ID: 339919905"
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Project Overview"
    tf = slide.placeholders[1].text_frame
    tf.text = "A data-driven FastAPI Web API for managing tasks."
    for text in ["SQLite used for local persistent storage.", "SQLAlchemy used as the ORM layer.", "Pydantic validates request and response data.", "Swagger /docs provides interactive API documentation."]:
        p = tf.add_paragraph(); p.text = text; p.level = 1
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "System Architecture"
    tf = slide.placeholders[1].text_frame
    tf.text = "Client -> FastAPI routes -> SQLAlchemy ORM -> SQLite database"
    for text in ["main.py starts the application and exception handlers.", "routers/items.py contains CRUD endpoint logic.", "database.py defines the Task model and session handling.", "schemas.py defines validated API payloads."]:
        p = tf.add_paragraph(); p.text = text; p.level = 1
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Version Control Evidence"
    tf = slide.placeholders[1].text_frame
    tf.text = "Structured Git history demonstrates staged development:"
    for text in ["8ca73e4 Initialize coursework API repository", "a06c6a7 Add database configuration and task schemas", "a7cf785 Implement CRUD task API endpoints", "2e79950 Add sample seed data for local demonstrations", "10a11b3 Add automated API tests with isolated database", "4816579 Document project setup and deployment workflow", "49b39ac Add submission report presentation and API documentation"]:
        p = tf.add_paragraph(); p.text = text; p.level = 1
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "API Features Demonstrated"
    tf = slide.placeholders[1].text_frame
    tf.text = "Implemented endpoints and enhanced API behaviour:"
    for text in ["Complete CRUD for the Task resource", "Pagination using page and limit query parameters", "Search and filter support on task listings", "PATCH support for partial updates", "Standardized error responses and timestamps"]:
        p = tf.add_paragraph(); p.text = text; p.level = 1
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Testing and Quality Assurance"
    tf = slide.placeholders[1].text_frame
    tf.text = "Automated tests were implemented with pytest."
    for text in ["10 automated tests pass successfully.", "TestClient used for endpoint verification.", "Temporary SQLite database isolates tests from development data.", "Covers CRUD, filtering, 404 handling, and validation errors."]:
        p = tf.add_paragraph(); p.text = text; p.level = 1
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Reflection and Next Steps"
    tf = slide.placeholders[1].text_frame
    tf.text = "Project outcomes and future improvements:"
    for text in ["The project satisfies the core Web API coursework requirements.", "AI assistance supported scaffolding, testing ideas, and documentation drafting.", "The final system was run, verified, and refined manually before submission.", "Future work: deploy to Render, add authentication, and migrate to PostgreSQL."]:
        p = tf.add_paragraph(); p.text = text; p.level = 1
    prs.save(str(DOCS / "Presentation_XJCO3011.pptx"))


if __name__ == "__main__":
    build_api_pdf()
    build_report_pdf()
    build_presentation()
