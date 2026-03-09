"""
حذف جميع البيانات التجريبية - نسخة سريعة بدون تأكيد
يحذف جميع المستخدمين الذين يستخدمون @test.local
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.data.models.user_model import User
from app.data.models.submission_model import Submission
from app.data.models.assignment_model import Assignment
from app.data.models.course_model import Course
from app.data.models.section_model import Section
from app.data.models.enrollment_model import Enrollment

def cleanup_now():
    db = SessionLocal()
    
    try:
        print("🗑️  حذف البيانات التجريبية...\n")
        
        # عد المستخدمين التجريبيين
        test_users = db.query(User).filter(User.email.like('%@test.local')).all()
        
        if not test_users:
            print("✓ لا توجد بيانات تجريبية للحذف")
            return
        
        teachers = [u for u in test_users if u.role == "teacher"]
        students = [u for u in test_users if u.role == "student"]
        
        print(f"📊 تم العثور على:")
        print(f"  • {len(teachers)} معلم")
        print(f"  • {len(students)} طالب")
        print(f"  • المجموع: {len(test_users)} مستخدم\n")
        
        print("⚠️  جاري الحذف...\n")
        
        # الحذف (relationships ستحذف تلقائياً بسبب cascade)
        count = db.query(User).filter(User.email.like('%@test.local')).delete(synchronize_session=False)
        db.commit()
        
        print(f"✅ تم حذف {count} مستخدم وجميع البيانات المرتبطة بهم")
        print("  (المقررات، الشعب، الواجبات، التسليمات، التسجيلات)")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ حدث خطأ: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_now()
