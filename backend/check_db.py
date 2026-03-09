import sqlite3

conn = sqlite3.connect('assignment_manager.db')
cursor = conn.cursor()

# Check if alembic_version table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version';")
result = cursor.fetchone()

if result:
    print("✓ alembic_version table exists")
    cursor.execute("SELECT * FROM alembic_version;")
    versions = cursor.fetchall()
    print(f"  Recorded versions: {versions}")
else:
    print("✗ alembic_version table does not exist")

# Check if section_id column exists in assignments table
cursor.execute("PRAGMA table_info(assignments);")
columns = cursor.fetchall()
print("\nAssignments table columns:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

section_id_exists = any(col[1] == 'section_id' for col in columns)
print(f"\n{'✓' if section_id_exists else '✗'} section_id column {'exists' if section_id_exists else 'MISSING'}")

conn.close()
