import sqlite3

# Connect to the database
conn = sqlite3.connect('university_assignment_manager.db')
cursor = conn.cursor()

print("Adding section_id column to assignments table...")

# Add section_id column to assignments table
try:
    cursor.execute("""
        ALTER TABLE assignments 
        ADD COLUMN section_id INTEGER REFERENCES sections(id)
    """)
    conn.commit()
    print("✓ Successfully added section_id column to assignments table")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e):
        print("✓ section_id column already exists")
    else:
        print(f"✗ Error: {e}")

conn.close()
