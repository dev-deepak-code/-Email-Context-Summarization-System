from app.db.base import Base
from app.models.firm import Firm
from app.models.accountant import Accountant, Role
from app.models.client import Client
from app.models.email import Email
from app.models.email_summary import EmailSummary

# This file explicitly exports the models so Alembic and other tools
# can easily find them for metadata and imports.
