# MMP Cerdas — Sahabat Belajar Membaca dan Menulis

**Versi:** 1.0 (prototipe interaktif)  
**Sasaran:** Anak usia sekitar 5–7 tahun, kelas I SD/MI, dengan pendampingan orang tua atau guru.  
**Kurikulum:** Program penguatan keterampilan MMP berbasis CP Bahasa Indonesia Fase A; pembagian bab dan soal merupakan pengembangan Pendamping Akademik, bukan format resmi mata pelajaran terpisah.

## Isi paket

- `index.html` — aplikasi utama untuk seluruh materi dan latihan.
- `contoh-integrasi.html` — demonstrasi satu halaman induk menampilkan semua materi dalam **satu iframe** yang berganti sumber.
- `js/course-data.js` — **8 bab, 24 subbab, 48 materi, 96 submateri**. Masing-masing memiliki latihan mendengar, membaca, menulis, berbicara: **384 aktivitas**. Bab 7–8 juga berisi bacaan tiga kalimat dan pertanyaan pemahaman.
- `js/app.js` — navigasi, sapaan personal, suara guru virtual, penilaian, mikrofon, perekam sementara, tulisan tangan, statistik, dan penyimpanan.
- `js/config.js` — konfigurasi opsional Supabase; **sengaja masih kosong**.
- `css/style.css` — tampilan hijau–emas yang responsif.
- `assets/guru-virtual.jpg` — potret guru virtual **buatan AI**, bukan foto guru nyata.
- `materi/MMP-.../index.html` — **96 tautan pintas** ke sesi tertentu. Untuk digunakan di Blogger, lebih praktis memakai parameter `lesson` langsung.
- `docs/daftar-96-sesi.csv` — indeks sesi untuk katalog atau bank soal.
- `supabase/setup.sql` — skema dan kebijakan keamanan database beserta penghapusan otomatis setiap 5 menit untuk profil yang tidak aktif selama empat hari.

## Apa yang sudah berjalan

| Fitur | Status | Catatan |
|---|---|---|
| 96 sesi / 384 latihan | Dibuat | Satu latihan ringkas per jenis aktivitas di setiap submateri; dapat diperkaya lagi untuk asesmen formal. |
| Sapaan nama anak | Dibuat | Menyesuaikan waktu pagi/siang/sore/malam dan progres. Nama panggilan saja. |
| Guru berbicara menjelaskan fokus dan ATP | Dibuat | Menggunakan suara `speechSynthesis` sistem dalam bahasa Indonesia; kualitas suara bergantung pada suara perangkat. Perlu klik anak karena kebijakan autoplay. |
| Mendengarkan | Dibuat | Anak mendengar kata/bunyi lalu memilih kartu dengan bantuan audio pilihan. |
| Membaca | Dibuat | Anak membaca tulisan dan dapat mencoba pengenalan suara; Bab 7–8 juga ada pemahaman bacaan. |
| Berbicara | Dibuat | Mendengar contoh, berbicara dengan pengenal suara atau pendamping. |
| Merekam suara lalu memutar ulang | Dibuat | Memakai MediaRecorder; **tidak disimpan** di database atau perangkat secara permanen. Durasi maksimal 12 detik. |
| Uji volume mikrofon | Dibuat | Kalibrasi volume saja; **tidak meningkatkan akurasi model pengenalan suara**. |
| Menulis via ketikan | Dibuat | Pencocokan sederhana setelah normalisasi tanda baca. |
| Menulis via papan digital | Dibuat | Anak menulis dengan mouse, jari, atau stylus. |
| Pengenal tulisan tangan | Integrasi OCR | Tesseract.js v5 dimuat dari CDN saat diminta; akurasi tulisan tangan anak rendah/bervariasi, hasil perlu dicek pendamping. |
| Progres per kegiatan | Dibuat | Menandai latihan otomatis atau latihan bersama pendamping, serta proyek per bab. |
| Simpan 4 hari | Lokal siap | Masa aktif diperbarui saat ada tindakan nyata anak. Jika tidak aktif selama 96 jam, data perangkat dibersihkan **pada pembukaan berikutnya**. |
| Database daring Supabase | Kode integrasi siap | Tidak aktif sampai URL, publishable key, anonymous sign-in, dan SQL dipasang. |
| Penghapusan daring 4 hari | SQL disiapkan | Setelah cron diaktifkan, penghapusan pada server dijadwalkan setiap 5 menit. Terlambat beberapa menit mungkin terjadi; perlu pemantauan job. |
| Percakapan bebas layaknya manusia | Belum | Umpan balik adalah naskah yang diprogram; bukan AI dialog bebas. |
| Model ASR khusus anak 5–7 tahun | Belum | Web Speech API browser adalah fondasi, bukan pengenal fonem anak yang telah dilatih dan divalidasi. |

## 1. Menggunakan aplikasi di komputer

1. Ekstrak ZIP.
2. Buka terminal pada folder `mmp-cerdas`.
3. Jalankan server lokal sederhana (Python): `python -m http.server 8000`.
4. Buka `http://localhost:8000/index.html` di Chrome atau Edge.
5. Isi **nama panggilan**, centang persetujuan orang tua/wali, lalu tekan **Mulai belajar dengan Bu Rani**.
6. Klik **Mulai pelajaran & dengarkan ATP**; pilih latihan di empat tab dan gunakan navigasi daftar isi.

> Jalankan melalui `http://localhost` atau `https://` GitHub Pages, bukan dengan klik ganda `file://`, karena mikrofon dan OCR memerlukan izin browser dan konteks aman.

## 2. Publikasikan ke GitHub Pages

1. Buat repositori GitHub, contoh `mmp-cerdas`.
2. Unggah **isi folder** `mmp-cerdas/` ke root repositori (pastikan `index.html` berada di root). Tidak perlu mengunggah `build_data.py` atau skrip pengujian.
3. Buka **Settings → Pages → Build and deployment → Deploy from a branch**. Pilih `main` dan folder `/ (root)`.
4. Setelah situs aktif, buka: `https://USERNAME.github.io/mmp-cerdas/`.
5. Latihan tertentu: `https://USERNAME.github.io/mmp-cerdas/index.html?embed=1&lesson=MMP-3.2.2-B`.
6. Untuk revisi, ganti berkas di lokasi yang sama, lakukan commit, lalu muat ulang halaman secara paksa jika browser masih menampilkan versi lama.

**Jangan menyimpan data siswa atau secret key di repositori GitHub.** GitHub Pages hanya menyajikan berkas statis, bukan database.

## 3. Menampilkan aplikasi di satu halaman Blogger/HTML lain

Ganti `USERNAME` dan nama repositori, kemudian tempel kode HTML berikut di halaman yang mendukung iframe.

```html
<div style="max-width:1200px;margin:auto">
  <iframe
    src="https://USERNAME.github.io/mmp-cerdas/index.html?embed=1&lesson=MMP-1.1.1-A"
    title="Guru Virtual MMP Cerdas Kelas I"
    allow="microphone; autoplay"
    loading="lazy"
    style="width:100%;height:900px;border:0;border-radius:14px;background:#fff">
  </iframe>
</div>
```

Aplikasi **tetap satu file `index.html` sebagai mesin**, sementara isi berubah sesuai `lesson=MMP-...`. Untuk portal berisi pilihan semua 96 sesi, lihat `contoh-integrasi.html`.

Apabila iframe diblokir oleh template Blogger/fitur browser, gunakan tautan langsung ke GitHub Pages sebagai alternatif. Penyimpanan lokal di iframe lintas-situs dapat dibatasi oleh pengaturan privasi browser; gunakan alamat aplikasi langsung jika progres tidak bertahan.

## 4. Database daring gratis dengan Supabase

### A. Persiapan

1. Buat proyek di https://supabase.com/ . Paket gratis memiliki batas penggunaan dan ketentuan yang dapat berubah.
2. Buka **Authentication → Providers** dan aktifkan **Anonymous Sign-Ins**. Anak tidak diminta email/password.
3. Di **SQL Editor**, jalankan seluruh isi `supabase/setup.sql` menggunakan akun admin proyek. Pastikan query berhasil, termasuk pemasangan `pg_cron` dan job. Jika cron tidak tersedia di proyek/paket Anda, jalankan tugas penghapusan melalui layanan penjadwalan tepercaya di sisi server.
4. Buka **Project Settings / Connect / API** dan salin **Project URL** serta **publishable key** (atau legacy anon key yang dibolehkan untuk sisi klien).
5. Edit `js/config.js`:

```js
window.MMP_CONFIG = {
  url: 'https://PROJECT_ID.supabase.co',
  publishableKey: 'sb_publishable_XXXXXXXX'
};
```

6. Unggah revisi `js/config.js` ke GitHub. Pada halaman awal, orang tua/wali boleh mencentang **Simpan juga ke database daring**.
7. Pastikan log Supabase memperlihatkan upsert profil di `public.child_profiles` dan cron berjalan. **Jangan** gunakan `service_role`, `sb_secret_...`, atau kredensial database dalam file JavaScript publik.

### B. Keamanan database

`child_profiles` menyimpan nama panggilan, progres kegiatan, proyek, pelajaran terakhir, dan waktu aktivitas. **Tidak ada audio atau gambar coretan disimpan di Supabase.** RLS memfilter data berdasarkan `auth.uid()` milik akun anonim browser.

Akun anonim hanya dapat melanjutkan profil di browser/perangkat yang menyimpan sesi autentikasi yang sama. Untuk pemulihan lintas perangkat, diperlukan sistem akun orang tua/wali yang terpisah dan persetujuan khusus. Jangan menganggap anonymous sign-in sebagai identitas anak yang tervalidasi.

### C. Penghapusan empat hari

- **Lokal:** pada akses berikutnya setelah `lastActive` melewati 96 jam, nama dan kemajuan lokal dihapus; browser yang tidak dibuka tidak bisa mengeksekusi pembersihan.
- **Daring:** cron setiap lima menit menjalankan penghapusan baris `child_profiles` yang `last_active`-nya sudah lebih dari empat hari; timestamp diatur database pada setiap simpan hasil latihan nyata. Hapus nama dan progres, tetapi catatan autentikasi anonim Supabase mungkin masih ada dan memerlukan kebijakan retensi admin tersendiri.
- **Aktivitas berkelanjutan:** klik navigasi, latihan, proyek, rekam, atau mulai pelajaran memperbarui waktu aktif dan memperpanjang penyimpanan.
- **Tombol hapus manual:** menghapus perangkat langsung; bila terhubung, aplikasi meminta Supabase menghapus baris profil. Periksa status jaringan agar tahu apakah penghapusan server berhasil.

Saran implementasi nyata untuk data anak: peninjauan hukum perlindungan data pribadi, persetujuan wali yang dapat diverifikasi, kebijakan akses, monitoring cron, backup retention policy, dan uji keamanan terpisah.

## 5. Kualitas pengenal suara anak

- Web Speech API adalah pengenal ucapan bahasa Indonesia yang disediakan browser. `interimResults`, `maxAlternatives = 5`, dan normalisasi sederhana digunakan untuk membantu latihan. **Tidak ada parameter sensitivitas yang dapat membuatnya otomatis setara model pengenal suara khusus anak.**
- Cek mikrofon terlebih dahulu. Ruangan tenang, jarak mikrofon dekat tetapi tidak menempel, ucapan perlahan, dan pendampingan memperbaiki pengalaman.
- Sebagian browser mengirim audio ke pengenal suara berbasis server. Hal ini bergantung pada browser, penyedia, dan kebijakan perangkat; karena itu aplikasi meminta persetujuan orang tua/wali.
- Kalau respons salah, tersedia ulangan dan penandaan *latihan bersama pendamping* tanpa berpura-pura memberi nilai akurasi tinggi.
- Untuk fase produksi, pengenal bahasa Indonesia berbasis model suara anak, kalibrasi mikrofon, serta evaluasi terstandar pada beragam pelafalan dan dialek harus dikembangkan secara terpisah. Jangan menyimpan contoh suara anak tanpa persetujuan khusus yang terinformasi.

## 6. Pengenalan tulisan tangan

Tesseract.js mendukung OCR di browser, tetapi bukan mesin pengenal tulisan tangan anak yang telah dioptimalkan. Untuk huruf tunggal gunakan goresan besar dan jelas. Untuk kata/kalimat, ketikan atau pemeriksaan orang tua/guru lebih andal. Tulisan yang dibuat pada kanvas berada di memori hingga kartu latihan diganti; tidak tersimpan permanen.

## 7. Memperkaya seluruh isi

Modifikasi judul, target, narasi, bacaan, dan pilihan soal melalui `build_data.py`, kemudian jalankan `python build_data.py` untuk membentuk kembali `js/course-data.js` serta indeks CSV. Untuk setiap submateri tersedia objek `practice.listen`, `practice.read`, `practice.write`, dan `practice.speak`. Jangan mengubah ID setelah aplikasi dipakai siswa karena ID berfungsi sebagai kunci progres.

Setiap bab memiliki satu proyek dan setiap submateri empat kegiatan. Versi ini adalah **program awal interaktif yang bekerja dengan contoh latihan ringkas**, bukan paket asesmen psikometrik, guru AI generatif dua arah, atau model pengenal suara anak tersertifikasi.

## 8. Referensi teknis

- GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- Supabase RLS: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase Anonymous Sign-In: https://supabase.com/docs/guides/auth/auth-anonymous
- Supabase Cron: https://supabase.com/docs/guides/cron
- Web Speech API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- Tesseract.js: https://github.com/naptha/tesseract.js

**Pengembang konten:** Pendamping Akademik. Desain dan potret guru virtual merupakan ilustrasi AI, tanpa klaim identitas orang nyata. Seluruh contoh latihan adalah konten orisinal pengembangan dan tidak mengambil soal berhak cipta dari lembaga bimbingan belajar.
