# MEMBACA LANJUTAN KELAS II SD/MI — 144 SESI

Pendamping Akademik | Paket awal media interaktif mandiri

## ISI PAKET
- index.html — halaman utama media interaktif
- style.css — desain hijau-emas responsif
- app.js — navigasi, guru virtual sintesis suara, kuis, penilaian, rekaman opsional, laporan
- data-latihan.js — seluruh konten yang langsung dibaca browser, termasuk saat dibuka tanpa server
- data-latihan.json — data terstruktur agar mudah diubah atau digunakan ulang
- daftar-144-sesi.csv — daftar bab, subbab, materi, submateri, pertanyaan, dan kunci
- latihan-cetak.html — latihan seluruh bab untuk dicetak melalui browser
- BLOGGER_IFRAME_SIAP_TEMPEL.html — kode iframe untuk Blogger
- pratinjau.png — pratinjau tampilan dalam pengujian
- build_data.py dan create_print.py — generator konten dan buku cetak untuk pengembangan berikutnya

## SUSUNAN
12 Bab / 36 Subbab / 72 Materi / 144 Submateri.
Tiap submateri mempunyai 4 aktivitas:
1. Mendengarkan bacaan dan soal pilihan ganda (otomatis benar/salah)
2. Membaca nyaring dengan contoh suara sintesis dan rubrik pendamping 1–4
3. Menulis jawaban terbuka dan mencocokkan contoh jawaban
4. Berbicara / menceritakan kembali dengan cek rubrik
Total: 576 aktivitas, 144 soal pemahaman pilihan ganda, dan 144 latihan menulis jawaban singkat beserta kegiatan lisan.
Setiap bab memiliki 1 proyek PjBL, total 12 proyek.

## UNGGAH KE GITHUB PAGES
Repositori kelas I sebelumnya: `asyiknyabelajar/mmp-cerdas`.
1. Buat folder baru `membaca-lanjutan-2` pada cabang yang dipublikasikan melalui GitHub Pages.
2. Letakkan file `index.html`, `style.css`, `app.js`, dan `data-latihan.js` pada tingkat folder yang sama.
3. Opsional, unggah juga `latihan-cetak.html`, `data-latihan.json`, dan file dokumentasi.
4. URL target setelah deployment berhasil:
   https://asyiknyabelajar.github.io/mmp-cerdas/membaca-lanjutan-2/
5. Buka URL dan uji bab 1, bab 6, dan bab 12; cek soal, suara, progres, dan laporan.
6. Tempel isi `BLOGGER_IFRAME_SIAP_TEMPEL.html` ke halaman Blogger dalam mode HTML.

KODE IFRAME PER SUBMATERI
Gunakan alamat seperti ini (ganti kode sesi):
https://asyiknyabelajar.github.io/mmp-cerdas/membaca-lanjutan-2/?lesson=ML2-01.1.1.1
Jika sedang berpindah sesi melalui media, URL akan menandai sesi dengan hash, misalnya #ML2-12.3.2.2.

## FITUR DAN BATASAN
- Contoh suara guru virtual 'Bu Rani' memakai suara sintesis bawaan perangkat berbahasa Indonesia jika ada. Tidak ada berkas suara manusia yang direkam sebelumnya.
- Perekaman suara memerlukan mikrofon aktif, izin browser, dan konteks aman HTTPS. TIDAK wajib untuk menyelesaikan latihan.
- Transkripsi otomatis membutuhkan dukungan browser dan mungkin layanan pengenalan ucapan; hasilnya bukan ukuran pasti ketepatan membaca anak.
- Papan tulis digital dapat dipakai menggunakan mouse atau sentuhan. Tulisan tidak dikenali otomatis, dinilai pendamping.
- Jawaban pilihan ganda dinilai otomatis. Membaca, menulis, berbicara, dan proyek dinilai melalui rubrik pendamping.
- Kemajuan disimpan dalam localStorage browser perangkat yang dipakai. Belum tersambung Supabase; data dan rekaman tidak dikirim ke server.
- Rekaman suara hanya tersedia dalam sesi browser saat ini. Pilih 'Unduh rekaman' bila ingin menyimpan; file rekaman tidak otomatis tersimpan dalam progres.
- Cadangkan kemajuan melalui 'Laporan Kemajuan' > 'Cadangkan JSON', atau ekspor ke CSV. Belum tersedia impor cadangan dari antarmuka.
- Perubahan browser, penghapusan data situs, atau pemakaian perangkat lain dapat menghilangkan kemajuan lokal.
- Konten berupa teks asli; paket ini tidak menyertakan foto pembelajaran, audio rekaman, atau aset berlisensi pihak ketiga.

## PENILAIAN
Menyimak: benar/salah berdasarkan satu soal per submateri.
Membaca: 1 perlu bantuan banyak; 2 mulai berkembang; 3 baik; 4 sangat baik.
Menulis: contoh jawaban merupakan satu kemungkinan. Terima jawaban lain yang setara maknanya.
Berbicara: minimal 2 dari 3 cek (isi cerita sesuai, alasan/informasi, ucapan jelas).

## PANDUAN BELAJAR
1. Anak memilih Bab > Subbab > Materi > Submateri.
2. Simak bacaan. Jika suara tidak tersedia, guru/orang tua membacakannya.
3. Kerjakan pertanyaan menyimak.
4. Latihan membaca nyaring, lalu beri penilaian dengan rubrik.
5. Tulis jawaban dan cocokkan bersama pendamping.
6. Ceritakan kembali teks; catat hasilnya.
7. Kerjakan proyek per bab dan tandai jika sudah diperiksa.
8. Buka laporan untuk melihat perkembangan, serta simpan CSV bila diperlukan.

## CATATAN PENGEMBANGAN
Versi ini adalah aplikasi mandiri khusus kelas II, tidak mengubah MMP Cerdas kelas I yang sudah ada. Jika ingin integrasi backend Supabase proyek `pendamping-akademik` pada tahap berikutnya, perlu pemetaan identitas siswa, tabel progres ML2, aturan RLS, dan persetujuan orang tua. Jangan menaruh service_role key dalam kode frontend.
