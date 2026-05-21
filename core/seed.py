from core.auth import hash_password
from core.models import Course, CourseCode, Enrollment, Lesson, Task, TaskOption, User


def normalize_seed_branding(db):
    changed = False
    course = db.query(Course).filter(Course.title == "Python Basic MVP").first()
    if course:
        course.title = "Python Basic"
        changed = True
    code = db.query(CourseCode).filter(CourseCode.code == "PYTHON-MVP-01").first()
    existing_new_code = db.query(CourseCode).filter(CourseCode.code == "PYTHON-01").first()
    if code and not existing_new_code:
        code.code = "PYTHON-01"
        changed = True
    if changed:
        db.commit()


def _get_or_create_user(db, email, name, password, role):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_if_empty(db):
    normalize_seed_branding(db)
    if db.query(User).count() > 0:
        return

    admin = _get_or_create_user(db, "admin@ngodinglab.id", "Admin Ngoding Lab", "admin123", "admin")
    student = _get_or_create_user(db, "student@ngodinglab.id", "Student Demo", "student123", "student")

    course = Course(
        title="Python Basic",
        description="Kursus dasar Python untuk pemula.",
        level_name="Beginner",
        is_active=True,
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    db.add(Enrollment(user_id=student.id, course_id=course.id, status="active"))
    db.add(CourseCode(course_id=course.id, code="PYTHON-01", max_users=50, used_count=0, is_active=True))
    db.commit()

    lessons = [
        Lesson(course_id=course.id, title="Pertemuan 1 - Mengenal Python", description="Kenalan dengan fungsi Python dan output teks.", lesson_order=1, is_active=True),
        Lesson(course_id=course.id, title="Pertemuan 2 - Variabel dan Output", description="Belajar menyimpan nilai dan menampilkan hasil.", lesson_order=2, is_active=True),
        Lesson(course_id=course.id, title="Pertemuan 3 - Operasi Matematika", description="Menggunakan Python untuk operasi hitung sederhana.", lesson_order=3, is_active=True),
    ]
    db.add_all(lessons)
    db.commit()
    for lesson in lessons:
        db.refresh(lesson)

    t1 = Task(
        lesson_id=lessons[0].id,
        title="Fungsi Python",
        instruction="Pilih kegunaan Python yang benar.",
        task_type="multiple_choice",
        task_order=1,
        is_active=True,
    )
    t2 = Task(
        lesson_id=lessons[0].id,
        title="Menampilkan Teks",
        instruction="Buat program yang menampilkan teks Halo Python",
        task_type="coding_output",
        task_order=2,
        expected_answer="Halo Python",
        starter_code='print("")',
        is_active=True,
    )
    t3 = Task(
        lesson_id=lessons[1].id,
        title="Variabel Nama",
        instruction='Buat variabel nama berisi "Budi", lalu tampilkan Halo Budi',
        task_type="coding_output",
        task_order=1,
        expected_answer="Halo Budi",
        starter_code='nama = ""\nprint("Halo", nama)',
        is_active=True,
    )
    t4 = Task(
        lesson_id=lessons[1].id,
        title="Nama Variabel",
        instruction="Pilih nama variabel yang benar di Python.",
        task_type="multiple_choice",
        task_order=2,
        is_active=True,
    )
    t5 = Task(
        lesson_id=lessons[2].id,
        title="Penjumlahan",
        instruction="Buat program yang menampilkan hasil 5 + 7",
        task_type="coding_output",
        task_order=1,
        expected_answer="12",
        starter_code="hasil = 5 + 7\nprint(hasil)",
        is_active=True,
    )
    db.add_all([t1, t2, t3, t4, t5])
    db.commit()
    for task in [t1, t2, t3, t4, t5]:
        db.refresh(task)

    db.add_all(
        [
            TaskOption(task_id=t1.id, option_text="Membuat aplikasi sederhana", is_correct=True),
            TaskOption(task_id=t1.id, option_text="Otomatisasi proses rutin", is_correct=True),
            TaskOption(task_id=t1.id, option_text="Membuat logika permainan", is_correct=True),
            TaskOption(task_id=t1.id, option_text="Hanya untuk menggambar manual di kertas", is_correct=False),
            TaskOption(task_id=t4.id, option_text="nama_siswa", is_correct=True),
            TaskOption(task_id=t4.id, option_text="umur", is_correct=True),
            TaskOption(task_id=t4.id, option_text="1nama", is_correct=False),
            TaskOption(task_id=t4.id, option_text="nama siswa", is_correct=False),
        ]
    )
    db.commit()
