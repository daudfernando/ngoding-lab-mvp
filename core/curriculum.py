from core.models import Course, Lesson, Task, TaskOption


COURSE_TITLE = "Python Basic"


def mc(title, instruction, correct, wrong):
    options = [(text, True) for text in correct] + [(text, False) for text in wrong]
    return {
        "title": title,
        "instruction": instruction,
        "task_type": "multiple_choice",
        "options": options,
    }


def code(title, instruction, expected, starter):
    return {
        "title": title,
        "instruction": instruction,
        "task_type": "coding_output",
        "expected_answer": expected,
        "starter_code": starter,
    }


CURRICULUM = [
    {
        "title": "Perkenalan dengan bahasa pemrograman Python INDO",
        "description": "Memahami kegunaan Python, cara menjalankan program, dan output pertama.",
        "tasks": [
            mc("Kegunaan Python", "Pilih kegunaan Python yang tepat.", ["Membuat aplikasi", "Otomatisasi tugas", "Analisis data"], ["Mengatur hardware tanpa sistem operasi"]),
            code("Halo Dunia", "Tampilkan teks Halo Dunia.", "Halo Dunia", 'print("")'),
            mc("Perintah Output", "Fungsi apa yang digunakan untuk menampilkan output?", ["print()"], ["show()", "echo()", "display_only()"]),
            code("Nama Bahasa", "Tampilkan teks Python.", "Python", 'print("")'),
            mc("Ekstensi File", "Ekstensi file Python yang umum adalah...", [".py"], [".html", ".css", ".xlsx"]),
            code("Dua Baris Output", "Tampilkan Belajar dan Python di dua baris berbeda.", "Belajar\nPython", 'print("")\nprint("")'),
            mc("Interpreter", "Python menjalankan kode dengan bantuan...", ["interpreter"], ["browser saja", "spreadsheet", "gambar manual"]),
            code("Kalimat Semangat", "Tampilkan teks Saya bisa coding.", "Saya bisa coding", 'print("")'),
            mc("Sintaks Dasar", "Manakah contoh sintaks Python yang valid?", ['print("Halo")'], ["print Halo", "tampilkan(Halo)", "<print>Halo</print>"]),
            code("Angka Pertama", "Tampilkan angka 100.", "100", "print()"),
        ],
    },
    {
        "title": "Python. Tinjauan. Exception handling INDO",
        "description": "Mengenal error umum dan cara sederhana menangani exception.",
        "tasks": [
            mc("Jenis Error", "Error karena tanda kutip belum ditutup biasanya termasuk...", ["SyntaxError"], ["NameError", "KeyError", "ZeroDivisionError"]),
            code("Coba Bagi", "Tampilkan hasil 10 dibagi 2.", "5.0", "hasil = 10 / 2\nprint(hasil)"),
            mc("Blok Try", "Blok yang dipakai untuk mencoba kode yang mungkin error adalah...", ["try"], ["repeat", "when", "safe"]),
            code("Tangani Nol", "Gunakan try-except agar pembagian 10/0 menampilkan Error.", "Error", "try:\n    hasil = 10 / 0\n    print(hasil)\nexcept ZeroDivisionError:\n    print('')"),
            mc("Except", "Blok except dijalankan ketika...", ["terjadi exception"], ["program selalu benar", "loop selesai", "variabel dibuat"]),
            code("NameError Aman", "Tangani NameError dan tampilkan Variabel belum ada.", "Variabel belum ada", "try:\n    print(nama)\nexcept NameError:\n    print('')"),
            mc("ZeroDivisionError", "Exception untuk pembagian dengan nol adalah...", ["ZeroDivisionError"], ["ValueError", "TypeError", "IndexError"]),
            code("Finally Sederhana", "Gunakan try-finally agar tetap menampilkan Selesai.", "Selesai", "try:\n    angka = 5\nfinally:\n    print('')"),
            mc("Pesan Error", "Mengapa pesan error penting?", ["Membantu menemukan penyebab bug"], ["Agar program lebih lambat", "Agar kode tidak bisa dibaca", "Agar output selalu kosong"]),
            code("Konversi Aman", "Tangani ValueError saat int('abc') dan tampilkan Input salah.", "Input salah", "try:\n    angka = int('abc')\n    print(angka)\nexcept ValueError:\n    print('')"),
        ],
    },
    {
        "title": "Variabel INDO",
        "description": "Membuat variabel, memberi nilai, dan memakai variabel dalam output.",
        "tasks": [
            mc("Nama Variabel Valid", "Pilih nama variabel Python yang valid.", ["nama_siswa", "umur"], ["1nama", "nama siswa"]),
            code("Variabel Nama", 'Buat variabel nama berisi "Budi", lalu tampilkan.', "Budi", 'nama = ""\nprint(nama)'),
            mc("Operator Assignment", "Simbol untuk memberi nilai ke variabel adalah...", ["="], ["==", ":", "=>"]),
            code("Halo Nama", 'Buat nama = "Siti", lalu tampilkan Halo Siti.', "Halo Siti", 'nama = ""\nprint("Halo", nama)'),
            mc("Tipe Angka", "Nilai 17 biasanya disimpan sebagai tipe...", ["int"], ["str", "list", "dict"]),
            code("Umur", "Buat variabel umur berisi 15 lalu tampilkan.", "15", "umur = 0\nprint(umur)"),
            mc("Case Sensitive", "Python membedakan huruf besar dan kecil pada variabel.", ["Benar"], ["Salah"]),
            code("Jumlah Nilai", "Buat a=8 dan b=4 lalu tampilkan jumlahnya.", "12", "a = 0\nb = 0\nprint(a + b)"),
            mc("String", 'Nilai "Jakarta" bertipe...', ["str"], ["int", "float", "bool"]),
            code("Ganti Nilai", "Isi x=3 lalu ubah x menjadi 9 dan tampilkan x.", "9", "x = 3\nx = 0\nprint(x)"),
        ],
    },
    {
        "title": "Python. Tinjauan Daftar. INDO",
        "description": "Mengenal list, index, panjang list, dan operasi list dasar.",
        "tasks": [
            mc("Bentuk List", "Manakah contoh list Python?", ["[1, 2, 3]"], ["{1, 2, 3}", "(1, 2, 3)", "<1,2,3>"]),
            code("Item Pertama", "Tampilkan item pertama dari daftar buah.", "apel", "buah = ['apel', 'jeruk', 'mangga']\nprint(buah[0])"),
            mc("Index Awal", "Index pertama pada list Python adalah...", ["0"], ["1", "-1", "10"]),
            code("Panjang List", "Tampilkan panjang list angka.", "4", "angka = [2, 4, 6, 8]\nprint(len(angka))"),
            mc("Menambah Item", "Method untuk menambah item di akhir list adalah...", ["append()"], ["push()", "add_first()", "insert_end()"]),
            code("Append List", "Tambahkan 'biru' ke list warna lalu tampilkan list.", "['merah', 'biru']", "warna = ['merah']\nwarna.append('')\nprint(warna)"),
            mc("Index Terakhir", "Index -1 mengakses...", ["item terakhir"], ["item pertama", "panjang list", "list kosong"]),
            code("Item Terakhir", "Tampilkan item terakhir dari list angka.", "30", "angka = [10, 20, 30]\nprint(angka[-1])"),
            mc("List Bisa Diubah", "List di Python bersifat...", ["mutable"], ["selalu tetap", "hanya angka", "tidak bisa diakses"]),
            code("Ubah Item", "Ubah item pertama list nama menjadi Ana lalu tampilkan list.", "['Ana', 'Budi']", "nama = ['Ari', 'Budi']\nnama[0] = ''\nprint(nama)"),
        ],
    },
    {
        "title": "String INDO",
        "description": "Mengolah teks dengan indexing, penggabungan, method, dan format sederhana.",
        "tasks": [
            mc("Tipe String", "String digunakan untuk menyimpan...", ["teks"], ["hanya angka", "gambar", "database"]),
            code("Cetak String", "Tampilkan teks Belajar String.", "Belajar String", 'teks = ""\nprint(teks)'),
            mc("Gabung String", "Operator untuk menggabungkan string adalah...", ["+"], ["*", "-", "//"]),
            code("Gabung Nama", "Gabungkan depan dan belakang menjadi Ana Putri.", "Ana Putri", "depan = 'Ana'\nbelakang = 'Putri'\nprint(depan + ' ' + belakang)"),
            mc("Panjang String", "Fungsi untuk menghitung panjang string adalah...", ["len()"], ["count_all()", "size()", "long()"]),
            code("Panjang Kata", "Tampilkan panjang kata Python.", "6", "kata = 'Python'\nprint(len(kata))"),
            mc("Huruf Besar", "Method untuk mengubah string menjadi huruf besar adalah...", ["upper()"], ["big()", "capital_all()", "up()"]),
            code("Upper", "Ubah kata belajar menjadi BELAJAR.", "BELAJAR", "kata = 'belajar'\nprint(kata.upper())"),
            mc("Index String", "Index pertama karakter string adalah...", ["0"], ["1", "-2", "length"]),
            code("Karakter Pertama", "Tampilkan karakter pertama dari kata Kode.", "K", "kata = 'Kode'\nprint(kata[0])"),
        ],
    },
    {
        "title": "Kamus. INDO",
        "description": "Mengenal dictionary, key-value, update nilai, dan akses data.",
        "tasks": [
            mc("Dictionary", "Dictionary menyimpan data dalam bentuk...", ["key dan value"], ["baris saja", "gambar saja", "index tanpa nama"]),
            code("Akses Nama", "Tampilkan value dari key nama.", "Budi", "siswa = {'nama': 'Budi', 'umur': 15}\nprint(siswa['nama'])"),
            mc("Simbol Dictionary", "Dictionary biasanya ditulis dengan...", ["{}"], ["[]", "()", "<>"]),
            code("Akses Umur", "Tampilkan umur dari dictionary siswa.", "15", "siswa = {'nama': 'Budi', 'umur': 15}\nprint(siswa['umur'])"),
            mc("Key", "Pada {'nama': 'Ana'}, 'nama' disebut...", ["key"], ["value", "loop", "function"]),
            code("Tambah Key", "Tambahkan kota='Bandung' lalu tampilkan dictionary.", "{'nama': 'Ana', 'kota': 'Bandung'}", "data = {'nama': 'Ana'}\ndata['kota'] = ''\nprint(data)"),
            mc("Method Keys", "Method untuk melihat semua key adalah...", ["keys()"], ["items_only()", "names()", "labels()"]),
            code("Daftar Key", "Tampilkan semua key dari dictionary sebagai list.", "['nama', 'umur']", "siswa = {'nama': 'Budi', 'umur': 15}\nprint(list(siswa.keys()))"),
            mc("Update Value", "Nilai dictionary bisa diubah dengan...", ["data['key'] = nilai_baru"], ["data.key == nilai", "change data", "lock(data)"]),
            code("Ubah Nilai", "Ubah umur menjadi 16 lalu tampilkan.", "16", "siswa = {'umur': 15}\nsiswa['umur'] = 0\nprint(siswa['umur'])"),
        ],
    },
    {
        "title": "Konstruksi bersarang INDO",
        "description": "Menggunakan if dan loop bersarang secara sederhana.",
        "tasks": [
            mc("Nested If", "If di dalam if disebut...", ["if bersarang"], ["if kosong", "if global", "if list"]),
            code("If Bersarang", "Jika nilai=90 dan hadir=True, tampilkan Lulus.", "Lulus", "nilai = 90\nhadir = True\nif nilai >= 75:\n    if hadir:\n        print('')"),
            mc("Indentasi", "Blok bersarang di Python ditandai dengan...", ["indentasi"], ["tanda kurung kurawal saja", "warna teks", "nama file"]),
            code("Kategori Umur", "Jika umur 13 dan izin True, tampilkan Boleh.", "Boleh", "umur = 13\nizin = True\nif umur >= 12:\n    if izin:\n        print('')"),
            mc("Nested Loop", "Loop di dalam loop disebut...", ["loop bersarang"], ["loop mati", "loop tunggal", "loop komentar"]),
            code("Cetak Pasangan", "Cetak A1 dan A2 dengan loop bersarang.", "A1\nA2", "for huruf in ['A']:\n    for angka in [1, 2]:\n        print(huruf + str(angka))"),
            mc("Risiko Bersarang", "Terlalu banyak nesting dapat membuat kode...", ["lebih sulit dibaca"], ["selalu lebih cepat", "tidak bisa error", "menjadi gambar"]),
            code("Dua Kondisi", "Jika x=5 dan y=10, tampilkan OK jika keduanya positif.", "OK", "x = 5\ny = 10\nif x > 0:\n    if y > 0:\n        print('')"),
            mc("Else Bersarang", "Else pada if bersarang dipakai ketika...", ["kondisi pada level tersebut salah"], ["program selesai", "import gagal", "list kosong selalu"]),
            code("Nilai dan Remedial", "Jika nilai=60 dan remedial=True, tampilkan Coba Lagi.", "Coba Lagi", "nilai = 60\nremedial = True\nif nilai >= 75:\n    print('Lulus')\nelse:\n    if remedial:\n        print('')"),
        ],
    },
    {
        "title": "Struktur Data Bersarang. INDO",
        "description": "Mengakses list berisi dictionary dan dictionary berisi list.",
        "tasks": [
            mc("Data Bersarang", "Struktur data bersarang berarti...", ["struktur data di dalam struktur data"], ["kode tanpa variabel", "file dihapus", "angka tanpa operasi"]),
            code("List Dalam List", "Tampilkan angka 3 dari matrix.", "3", "matrix = [[1, 2], [3, 4]]\nprint(matrix[1][0])"),
            mc("List of Dict", "Data [{'nama':'Ana'}] adalah...", ["list berisi dictionary"], ["dictionary berisi string saja", "tuple kosong", "angka"]),
            code("Akses Nama Siswa", "Tampilkan nama Budi dari list siswa.", "Budi", "siswa = [{'nama': 'Ana'}, {'nama': 'Budi'}]\nprint(siswa[1]['nama'])"),
            mc("Dict of List", "Data {'nilai':[80,90]} adalah...", ["dictionary berisi list"], ["list berisi function", "string berisi list", "boolean"]),
            code("Akses Nilai", "Tampilkan nilai kedua dari data.", "90", "data = {'nilai': [80, 90, 100]}\nprint(data['nilai'][1])"),
            mc("Index Bertingkat", "Akses data bersarang sering memakai...", ["index dan key bertingkat"], ["warna", "nama folder", "print saja"]),
            code("Tambah Data Bersarang", "Tambahkan 95 ke data nilai lalu tampilkan list.", "[80, 95]", "data = {'nilai': [80]}\ndata['nilai'].append(95)\nprint(data['nilai'])"),
            mc("Manfaat Struktur Bersarang", "Struktur bersarang berguna untuk...", ["data yang lebih kompleks"], ["menghapus semua data", "membuat error", "mengganti Python"]),
            code("Jumlah Nilai", "Jumlahkan nilai pada dictionary dan tampilkan hasilnya.", "170", "data = {'nilai': [80, 90]}\nprint(sum(data['nilai']))"),
        ],
    },
    {
        "title": "Pengulangan. Algoritma dan struktur data INDO",
        "description": "Menggunakan for loop untuk memproses data dan algoritma sederhana.",
        "tasks": [
            mc("For Loop", "For loop digunakan untuk...", ["mengulang proses"], ["menghapus Python", "membuat password", "mengganti monitor"]),
            code("Cetak 1 sampai 3", "Tampilkan angka 1, 2, 3 di baris berbeda.", "1\n2\n3", "for i in range(1, 4):\n    print(i)"),
            mc("Range", "range(3) menghasilkan angka...", ["0, 1, 2"], ["1, 2, 3", "3 saja", "0 sampai 3 termasuk 3"]),
            code("Jumlah List", "Jumlahkan [2,4,6] dengan loop lalu tampilkan.", "12", "angka = [2, 4, 6]\ntotal = 0\nfor n in angka:\n    total += n\nprint(total)"),
            mc("Accumulator", "Variabel total dalam penjumlahan loop disebut...", ["accumulator"], ["decorator", "exception", "module"]),
            code("Hitung Genap", "Hitung jumlah angka genap dari [1,2,3,4].", "2", "angka = [1, 2, 3, 4]\njumlah = 0\nfor n in angka:\n    if n % 2 == 0:\n        jumlah += 1\nprint(jumlah)"),
            mc("Algoritma", "Algoritma adalah...", ["langkah-langkah menyelesaikan masalah"], ["nama bahasa", "jenis error", "file database"]),
            code("Cari Terbesar", "Cari angka terbesar dari [3,9,2] dengan loop.", "9", "angka = [3, 9, 2]\nterbesar = angka[0]\nfor n in angka:\n    if n > terbesar:\n        terbesar = n\nprint(terbesar)"),
            mc("Loop Data", "Struktur data yang sering diproses dengan loop adalah...", ["list"], ["warna layar", "keyboard", "folder saja"]),
            code("Filter Nama", "Cetak nama yang panjangnya lebih dari 3 dari list.", "Budi", "nama = ['Ana', 'Budi']\nfor n in nama:\n    if len(n) > 3:\n        print(n)"),
        ],
    },
    {
        "title": "Pengulangan. Fungsi dan OOP. INDO",
        "description": "Menggabungkan loop dengan fungsi dan pengenalan class sederhana.",
        "tasks": [
            mc("Fungsi", "Fungsi dibuat dengan kata kunci...", ["def"], ["func", "make", "classonly"]),
            code("Fungsi Sapa", "Buat fungsi sapa yang menampilkan Halo.", "Halo", "def sapa():\n    print('')\n\nsapa()"),
            mc("Parameter", "Nilai masukan ke fungsi disebut...", ["parameter"], ["folder", "syntax", "terminal"]),
            code("Fungsi Kuadrat", "Buat fungsi kuadrat dan tampilkan kuadrat dari 4.", "16", "def kuadrat(x):\n    return x * x\n\nprint(kuadrat(4))"),
            mc("Return", "return digunakan untuk...", ["mengembalikan nilai dari fungsi"], ["mencetak selalu", "menghapus class", "membuat list kosong"]),
            code("Loop Dalam Fungsi", "Buat fungsi jumlah yang menjumlahkan list [1,2,3].", "6", "def jumlah(data):\n    total = 0\n    for item in data:\n        total += item\n    return total\n\nprint(jumlah([1, 2, 3]))"),
            mc("Class", "Class dalam OOP adalah...", ["cetakan untuk membuat object"], ["angka tetap", "loop khusus", "error"]),
            code("Class Sederhana", "Buat class Siswa dengan atribut nama dan tampilkan Ana.", "Ana", "class Siswa:\n    def __init__(self, nama):\n        self.nama = nama\n\ns = Siswa('Ana')\nprint(s.nama)"),
            mc("Object", "Object adalah...", ["hasil dari class"], ["file teks", "operator tambah", "komentar"]),
            code("Method Sapa", "Buat method sapa yang mengembalikan Halo Budi.", "Halo Budi", "class Siswa:\n    def __init__(self, nama):\n        self.nama = nama\n    def sapa(self):\n        return 'Halo ' + self.nama\n\ns = Siswa('Budi')\nprint(s.sapa())"),
        ],
    },
]


def _get_or_create_course(db):
    course = db.query(Course).filter(Course.title == COURSE_TITLE).first()
    if course:
        return course
    course = Course(
        title=COURSE_TITLE,
        description="Kursus dasar Python untuk pemula.",
        level_name="Beginner",
        is_active=True,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def _deactivate_old_demo_lessons(db, course_id):
    old_titles = [
        "Pertemuan 1 - Mengenal Python",
        "Pertemuan 2 - Variabel dan Output",
        "Pertemuan 3 - Operasi Matematika",
    ]
    changed = False
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id, Lesson.title.in_(old_titles)).all()
    for lesson in lessons:
        if lesson.is_active:
            lesson.is_active = False
            changed = True
    if changed:
        db.commit()


def ensure_curriculum(db):
    course = _get_or_create_course(db)
    _deactivate_old_demo_lessons(db, course.id)

    for lesson_index, lesson_data in enumerate(CURRICULUM, start=1):
        lesson = (
            db.query(Lesson)
            .filter(Lesson.course_id == course.id, Lesson.title == lesson_data["title"])
            .first()
        )
        if not lesson:
            lesson = Lesson(
                course_id=course.id,
                title=lesson_data["title"],
                description=lesson_data["description"],
                lesson_order=lesson_index,
                is_active=True,
            )
            db.add(lesson)
            db.commit()
            db.refresh(lesson)
        else:
            lesson.description = lesson_data["description"]
            lesson.lesson_order = lesson_index
            lesson.is_active = True
            db.commit()

        for task_index, task_data in enumerate(lesson_data["tasks"], start=1):
            task = (
                db.query(Task)
                .filter(Task.lesson_id == lesson.id, Task.title == task_data["title"])
                .first()
            )
            if not task:
                task = Task(
                    lesson_id=lesson.id,
                    title=task_data["title"],
                    instruction=task_data["instruction"],
                    task_type=task_data["task_type"],
                    task_order=task_index,
                    expected_answer=task_data.get("expected_answer", ""),
                    starter_code=task_data.get("starter_code", ""),
                    is_active=True,
                )
                db.add(task)
                db.commit()
                db.refresh(task)
            else:
                task.instruction = task_data["instruction"]
                task.task_type = task_data["task_type"]
                task.task_order = task_index
                task.expected_answer = task_data.get("expected_answer", "")
                task.starter_code = task_data.get("starter_code", "")
                task.is_active = True
                db.commit()

            if task.task_type == "multiple_choice" and not task.options:
                db.add_all(
                    [
                        TaskOption(task_id=task.id, option_text=option_text, is_correct=is_correct)
                        for option_text, is_correct in task_data["options"]
                    ]
                )
                db.commit()
