# Ngoding Lab MVP

Ngoding Lab MVP adalah aplikasi web latihan coding berbasis Streamlit untuk siswa. MVP1 menyediakan role Admin dan Student, manajemen course, pertemuan, latihan, pengecekan jawaban, progres siswa, dan laporan sederhana.

## Fitur MVP1

- Login Admin dan Student dengan password hash.
- Admin membuat akun siswa, course, lesson, task, opsi jawaban, test case, kode kelas, dan melihat laporan.
- Student hanya melihat course yang di-enroll oleh admin atau melalui kode kelas.
- Student mengerjakan task berurutan. Soal berikutnya terbuka setelah jawaban benar.
- Lesson berikutnya terbuka setelah semua task lesson sebelumnya selesai.
- Checker Python sederhana untuk `coding_output` dan `coding_function`.
- SQLite lokal default di `data/ngoding_lab.db`, atau PostgreSQL/Supabase jika `DATABASE_URL` tersedia.

## Struktur Folder

```text
ngoding-lab-mvp/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── data/
├── pages/
├── core/
└── scripts/
```

## Cara Install Lokal

```bash
python -m venv venv
source venv/bin/activate
```

Untuk Windows:

```powershell
venv\Scripts\activate
```

Lalu install dependency:

```bash
pip install -r requirements.txt
```

Jika di Windows muncul folder `venv\bin` dan bukan `venv\Scripts`, kemungkinan Python yang dipakai bukan installer resmi Windows. Gunakan Python 3.11+ resmi dari python.org atau jalankan:

```powershell
py -3.11 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dependency PostgreSQL `psycopg2-binary` dilewati otomatis di Windows untuk mode lokal SQLite. Untuk deploy Linux/Streamlit Cloud dengan Supabase/PostgreSQL, dependency ini tetap terpasang.

Jika muncul error `error reading bcrypt version` atau `password cannot be longer than 72 bytes` saat init database, jalankan:

```powershell
pip install --force-reinstall bcrypt==4.0.1
```

## Cara Init Database

```bash
python scripts/init_db.py
```

## Cara Run

```bash
streamlit run app.py
```

## Akun Default

- Admin: `admin@ngodinglab.id` / `admin123`
- Student: `student@ngodinglab.id` / `student123`

## Cara Admin Membuat Siswa Baru

Login sebagai admin, buka halaman **Admin Students**, isi nama siswa, email, password awal, pilih course, lalu klik **Buat Siswa**.

## Cara Admin Membuat Course Baru

Buka halaman **Admin Courses**, isi judul course, deskripsi, level, status aktif, lalu klik **Buat Course**.

## Cara Admin Membuat Lesson dan Latihan

Buka halaman **Admin Lessons & Tasks**. Buat lesson terlebih dahulu, lalu buat task. Untuk `multiple_choice`, tambahkan opsi jawaban. Untuk task coding, tambahkan expected answer atau test case.

## Cara Student Mengerjakan Latihan

Login sebagai student, buka **Student Dashboard**, masuk ke course dan pertemuan yang terbuka, lalu kerjakan task di halaman **Lesson Task**.

## Daftar Mandiri dengan Kode Kelas

Di halaman awal aplikasi, pilih tab **Daftar dengan Kode Kelas** dan gunakan kode:

```text
PYTHON-MVP-01
```

## Deploy ke Streamlit Community Cloud

1. Push project ke GitHub.
2. Deploy `app.py` di Streamlit Community Cloud.
3. Jika memakai Supabase/PostgreSQL, set `DATABASE_URL` di Streamlit secrets.
4. Jika `DATABASE_URL` kosong, aplikasi memakai SQLite lokal.

## Catatan Keamanan

Checker kode MVP1 masih terbatas dan hanya cocok untuk latihan ringan. Untuk production, gunakan Docker sandbox, Judge0, atau autograder service terpisah.

## Roadmap MVP2

- Supabase Auth.
- Class management lebih lengkap.
- Mentor review.
- Leaderboard.
- Reward/coin.
- Certificate.
- Docker autograder.
