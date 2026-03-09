import sqlite3

conn = sqlite3.connect('university_assignment_manager.db')
cursor = conn.cursor()

# Delete the alembic version to reset migration state
cursor.execute("DELETE FROM alembic_version;")
conn.commit()

print("✓ Deleted alembic migration history")
print("  Migration records have been cleared")
print("  Ready to apply migrations fresh")

conn.close()
