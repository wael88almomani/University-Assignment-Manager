"""
إضافة بيانات تجريبية للمعلمين والطلاب
جميع البيانات تستخدم بريد إلكتروني ينتهي بـ @test.local لسهولة حذفها لاحقاً
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta

# Import all models first to ensure relationships are configured
from app.data.models.user_model import User
from app.data.models.submission_model import Submission
from app.data.models.assignment_model import Assignment
from app.data.models.course_model import Course
from app.data.models.section_model import Section
from app.data.models.enrollment_model import Enrollment
from app.core.database import SessionLocal, Base
from app.core.security import get_password_hash

def seed_test_data():
    db = SessionLocal()
    
    try:
        print("🌱 إضافة بيانات تجريبية...\n")
        
        # التحقق من وجود بيانات تجريبية سابقة
        existing = db.query(User).filter(User.email.like('%@test.local')).count()
        if existing > 0:
            print(f"⚠️  يوجد {existing} مستخدمين تجريبيين سابقين")
            response = input("هل تريد حذفهم والبدء من جديد؟ (y/n): ")
            if response.lower() == 'y':
                print("🗑️  حذف البيانات التجريبية القديمة...")
                db.query(User).filter(User.email.like('%@test.local')).delete(synchronize_session=False)
                db.commit()
                print("✓ تم الحذف\n")
        
        # === المعلمين ===
        teachers = [
            {
                "name": "د. محمد أحمد",
                "email": "mohamed.ahmed@test.local",
                "password": "teacher123"
            },
            {
                "name": "د. فاطمة حسن",
                "email": "fatima.hassan@test.local",
                "password": "teacher123"
            },
            {
                "name": "د. علي خالد",
                "email": "ali.khaled@test.local",
                "password": "teacher123"
            },
            {
                "name": "د. نورة سعيد",
                "email": "noura.saeed@test.local",
                "password": "teacher123"
            }
        ]
        
        print("👨‍🏫 إضافة المعلمين...")
        teacher_objs = []
        for t in teachers:
            teacher = User(
                name=t["name"],
                email=t["email"],
                password=get_password_hash(t["password"]),
                role="teacher",
                created_at=datetime.utcnow()
            )
            db.add(teacher)
            teacher_objs.append(teacher)
            print(f"  ✓ {t['name']} - {t['email']}")
        
        db.commit()
        print(f"✅ تم إضافة {len(teachers)} معلمين\n")
        
        # === الطلاب ===
        students = [
            {"name": "أحمد عبدالله", "email": "ahmed.abdullah@test.local"},
            {"name": "سارة محمود", "email": "sara.mahmoud@test.local"},
            {"name": "يوسف إبراهيم", "email": "youssef.ibrahim@test.local"},
            {"name": "مريم عمر", "email": "mariam.omar@test.local"},
            {"name": "خالد سالم", "email": "khaled.salem@test.local"},
            {"name": "ليلى حمد", "email": "laila.hamad@test.local"},
            {"name": "عمر عادل", "email": "omar.adel@test.local"},
            {"name": "نورا فهد", "email": "nora.fahad@test.local"},
            {"name": "محمد صالح", "email": "mohammed.saleh@test.local"},
            {"name": "عائشة يوسف", "email": "aisha.youssef@test.local"},
            {"name": "فهد ناصر", "email": "fahad.nasser@test.local"},
            {"name": "هند عبدالعزيز", "email": "hind.abdulaziz@test.local"}
        ]
        
        print("👨‍🎓 إضافة الطلاب...")
        student_objs = []
        for s in students:
            student = User(
                name=s["name"],
                email=s["email"],
                password=get_password_hash("student123"),  # كلمة مرور موحدة: student123
                role="student",
                created_at=datetime.utcnow()
            )
            db.add(student)
            student_objs.append(student)
            print(f"  ✓ {s['name']} - {s['email']}")
        
        db.commit()
        print(f"✅ تم إضافة {len(students)} طلاب\n")
        
        # === المقررات والشعب ===
        print("📚 إضافة مقررات وشعب...")
        
        # مقرر 1: برمجة الويب (د. محمد)
        course1 = Course(
            name="برمجة الويب",
            code="CS301",
            teacher_id=teacher_objs[0].id,
            created_at=datetime.utcnow()
        )
        db.add(course1)
        db.commit()
        
        section1_1 = Section(name="الشعبة A", course_id=course1.id, created_at=datetime.utcnow())
        section1_2 = Section(name="الشعبة B", course_id=course1.id, created_at=datetime.utcnow())
        db.add_all([section1_1, section1_2])
        db.commit()
        
        # تسجيل طلاب في الشعبة A
        for student in student_objs[0:6]:  # أول 6 طلاب
            enrollment = Enrollment(
                student_id=student.id,
                section_id=section1_1.id,
                created_at=datetime.utcnow()
            )
            db.add(enrollment)
        
        # تسجيل طلاب في الشعبة B
        for student in student_objs[6:12]:  # باقي الطلاب
            enrollment = Enrollment(
                student_id=student.id,
                section_id=section1_2.id,
                created_at=datetime.utcnow()
            )
            db.add(enrollment)
        
        print(f"  ✓ {course1.code} - {course1.name} (شعبتين)")
        
        # مقرر 2: قواعد البيانات (د. فاطمة)
        course2 = Course(
            name="قواعد البيانات",
            code="CS302",
            teacher_id=teacher_objs[1].id,
            created_at=datetime.utcnow()
        )
        db.add(course2)
        db.commit()
        
        section2_1 = Section(name="الشعبة A", course_id=course2.id, created_at=datetime.utcnow())
        db.add(section2_1)
        db.commit()
        
        # تسجيل بعض الطلاب
        for student in student_objs[0:8]:
            enrollment = Enrollment(
                student_id=student.id,
                section_id=section2_1.id,
                created_at=datetime.utcnow()
            )
            db.add(enrollment)
        
        print(f"  ✓ {course2.code} - {course2.name} (شعبة واحدة)")
        
        # مقرر 3: خوارزميات (د. علي)
        course3 = Course(
            name="تصميم وتحليل الخوارزميات",
            code="CS303",
            teacher_id=teacher_objs[2].id,
            created_at=datetime.utcnow()
        )
        db.add(course3)
        db.commit()
        
        section3_1 = Section(name="الشعبة A", course_id=course3.id, created_at=datetime.utcnow())
        db.add(section3_1)
        db.commit()
        
        # تسجيل طلاب
        for student in student_objs[4:12]:
            enrollment = Enrollment(
                student_id=student.id,
                section_id=section3_1.id,
                created_at=datetime.utcnow()
            )
            db.add(enrollment)
        
        print(f"  ✓ {course3.code} - {course3.name} (شعبة واحدة)")
        
        db.commit()
        print(f"✅ تم إضافة 3 مقررات مع شعبها\n")
        
        # === الواجبات ===
        print("📝 إضافة واجبات تجريبية...")
        
        # واجبات لمقرر برمجة الويب
        assignments_course1 = [
            {
                "title": "واجب 1: HTML و CSS",
                "description": "إنشاء صفحة ويب باستخدام HTML و CSS",
                "due_date": datetime.utcnow() + timedelta(days=7),
                "section_id": section1_1.id
            },
            {
                "title": "واجب 2: JavaScript",
                "description": "تطبيق تفاعلي باستخدام JavaScript",
                "due_date": datetime.utcnow() + timedelta(days=14),
                "section_id": section1_1.id
            },
            {
                "title": "واجب 1: HTML و CSS",
                "description": "إنشاء صفحة ويب باستخدام HTML و CSS",
                "due_date": datetime.utcnow() + timedelta(days=7),
                "section_id": section1_2.id
            }
        ]
        
        for a in assignments_course1:
            assignment = Assignment(
                title=a["title"],
                description=a["description"],
                due_date=a["due_date"],
                teacher_id=teacher_objs[0].id,
                section_id=a["section_id"],
                created_at=datetime.utcnow()
            )
            db.add(assignment)
            print(f"  ✓ {a['title']}")
        
        # واجبات لمقرر قواعد البيانات
        assignments_course2 = [
            {
                "title": "واجب 1: تصميم قاعدة البيانات",
                "description": "تصميم ER Diagram لنظام مكتبة",
                "due_date": datetime.utcnow() + timedelta(days=10),
                "section_id": section2_1.id
            },
            {
                "title": "واجب 2: SQL Queries",
                "description": "كتابة استعلامات SQL متقدمة",
                "due_date": datetime.utcnow() + timedelta(days=20),
                "section_id": section2_1.id
            }
        ]
        
        for a in assignments_course2:
            assignment = Assignment(
                title=a["title"],
                description=a["description"],
                due_date=a["due_date"],
                teacher_id=teacher_objs[1].id,
                section_id=a["section_id"],
                created_at=datetime.utcnow()
            )
            db.add(assignment)
            print(f"  ✓ {a['title']}")
        
        db.commit()
        print(f"✅ تم إضافة 5 واجبات\n")
        
        print("=" * 60)
        print("✅ تم إضافة جميع البيانات التجريبية بنجاح!")
        print("=" * 60)
        print("\n📋 ملخص البيانات المضافة:")
        print(f"  • {len(teachers)} معلمين")
        print(f"  • {len(students)} طالب")
        print(f"  • 3 مقررات دراسية")
        print(f"  • 4 شعب")
        print(f"  • 5 واجبات")
        
        print("\n🔐 بيانات الدخول:")
        print("\n  المعلمين:")
        for t in teachers:
            print(f"    📧 {t['email']} | 🔑 {t['password']}")
        
        print("\n  الطلاب:")
        print(f"    📧 (أي طالب)@test.local | 🔑 student123")
        print(f"    مثال: ahmed.abdullah@test.local")
        
        print("\n⚠️  ملاحظة: جميع البيانات تستخدم @test.local في البريد الإلكتروني")
        print("   لحذف جميع البيانات التجريبية، شغّل: python cleanup_test_data.py")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ حدث خطأ: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_data()
