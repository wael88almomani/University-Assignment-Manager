"""
Fix database schema - add missing section_id column to assignments table
"""
import sqlite3
import os

db_path = 'university_assignment_manager.db'

# Check if database exists
if not os.path.exists(db_path):
    print(f"✗ Database file '{db_path}' not found")
    exit(1)

print(f"🔧 Fixing database schema: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current schema
    cursor.execute("PRAGMA table_info(assignments);")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'section_id' in columns:
        print("✓ section_id column already exists - no changes needed")
    else:
        print("➜ Adding section_id column...")
        cursor.execute("""
            ALTER TABLE assignments 
            ADD COLUMN section_id INTEGER REFERENCES sections(id)
        """)
        conn.commit()
        print("✓ Successfully added section_id column to assignments table")
    
    # Verify the fix
    cursor.execute("PRAGMA table_info(assignments);")
    columns_after = [col[1] for col in cursor.fetchall()]
    print(f"\nFinal columns in assignments table:")
    for col in columns_after:
        print(f"  - {col}")
    
    conn.close()
    print("\n✅ Database schema is now correct!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
