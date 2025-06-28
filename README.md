# Web Mirror & Cleaner Application

Aplikasi Flask untuk mirroring dan membersihkan halaman web dengan menghapus iklan, tracker, dan konten yang tidak diinginkan.

## Fitur Utama

- **Mirroring Halaman Web**: Input URL dan dapatkan versi bersih dari halaman tersebut
- **Pembersihan Otomatis**: Menghapus iklan, banner, pop-up, dan iframe iklan
- **Filter Script**: Memblokir script dari domain iklan seperti Google Ads, Taboola, Outbrain
- **Tampilan Modern**: UI responsif menggunakan Bootstrap 5
- **Dark/Light Mode**: Toggle tema dengan penyimpanan preferensi
- **Reading Options**: Kontrol ukuran font dan jarak baris
- **Focus Mode**: Mode baca tanpa gangguan
- **Print Support**: Fungsi cetak yang dioptimalkan

## Instalasi

1. Install dependensi Python:
```bash
pip install flask beautifulsoup4 requests gunicorn
```

2. Jalankan aplikasi:
```bash
python app.py
```

3. Buka browser dan akses: `http://localhost:5000`

## Struktur File

- `app.py` - Aplikasi Flask utama
- `content_cleaner.py` - Engine pembersihan konten
- `main.py` - Entry point untuk production
- `templates/` - Template HTML dengan Jinja2
- `static/` - CSS dan JavaScript
- `pyproject.toml` - Konfigurasi dependensi

## Cara Penggunaan

1. Masukkan URL website di form input
2. Klik "Clean & Mirror Page"
3. Tunggu proses pembersihan selesai
4. Nikmati konten bersih tanpa iklan

## Teknologi

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Parsing**: BeautifulSoup4
- **HTTP Client**: Requests
- **Server**: Gunicorn (Production)

## Keamanan

- Validasi URL input
- Timeout untuk request HTTP
- Limit redirect untuk mencegah loop
- Sanitasi konten HTML

## Deployment

Untuk production, gunakan Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Lisensi

Open source - dapat digunakan dan dimodifikasi sesuai kebutuhan.
