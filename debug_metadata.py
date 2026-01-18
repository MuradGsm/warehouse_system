from app.db.base import Base
import app.models  # важно

print("tables:", list(Base.metadata.tables.keys()))
