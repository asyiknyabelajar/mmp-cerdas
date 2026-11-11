import json, csv, re, random, pathlib
ROOT=pathlib.Path(__file__).parent
CHAPTERS=[]
def add(title, bloom, project, subbabs, materi, raw):
    lines=[x.strip() for x in raw.strip().splitlines() if x.strip() and not x.strip().startswith('#')]
    rows=[]
    for i,line in enumerate(lines,1):
        parts=[x.strip() for x in line.split('||')]
        if len(parts)!=6: raise ValueError((title,i,len(parts),line))
        subt, passage, q, ans, w1, w2=parts
        if len({ans.lower(),w1.lower(),w2.lower()})!=3: raise ValueError((title,i,'options nonunique'))
        rows.append({'submateri':subt,'bacaan':passage,'pertanyaan':q,'jawaban':ans,'pengecoh':[w1,w2]})
    assert len(rows)==12,(title,len(rows))
    assert len(subbabs)==3 and len(materi)==6
    CHAPTERS.append({'title':title,'bloom':bloom,'project':project,'subbabs':subbabs,'materi':materi,'items':rows})

add('Aku Pembaca yang Semakin Lancar','C1–C3','Rekam bacaan terbaikmu. Bandingkan ketepatan kata, jeda, dan intonasi bersama pendamping.',
['Membaca Kata dengan Tepat','Membaca Kalimat dengan Lancar','Membaca Nyaring dan Memahami Makna'],
['Mengenali Pola Kata','Ketepatan Membaca Kata','Membaca Kelompok Kata','Membaca dengan Intonasi','Membaca Teks Pendek','Memantau Pemahaman Sendiri'],r'''
Membaca kata dua sampai empat suku kata||Pagi ini Rani membawa sepeda ke halaman. Di sana ada kupu-kupu dan pepohonan. Rani membaca nama benda-benda itu dengan teliti.||Kata apa yang dibaca Rani dengan teliti?||Nama benda||Nama kota||Nama hari
Membaca kata dengan ng dan ny||Nyamuk hinggap di dekat bunga. Burung bernyanyi di atas ranting. Beni mengucapkan kata nyamuk, bernyanyi, dan ranting dengan jelas.||Kata mana yang memakai bunyi ny?||Bernyanyi||Bunga||Ranting
Membedakan kata mirip||Di kelas ada kata buku dan bubu pada kartu. Mira membaca buku, bukan bubu. Ia memeriksa setiap huruf sebelum menjawab.||Kata mana yang dibaca Mira?||Buku||Bubu||Baku
Memperbaiki kesalahan membaca||Dito mula-mula membaca kata 'kelapa' menjadi 'kepala'. Setelah melihat ulang, Dito membaca 'kelapa' dengan benar. Ia tidak malu memperbaiki bacaan.||Apa yang dilakukan Dito setelah salah membaca?||Membaca ulang dengan benar||Menutup bukunya||Berhenti belajar
Membaca kalimat tanpa mengeja||Ibu menata buah di meja. Sari membaca kalimat itu sekaligus, bukan huruf demi huruf. Setelah itu ia tahu siapa yang menata buah.||Siapa yang menata buah?||Ibu||Sari||Kakak
Mengatur jeda kelompok kata||Di taman kota, adik bermain bola bersama ayah. Ana memberi jeda sesudah kata 'kota'. Bacaan Ana menjadi mudah dipahami.||Di mana adik bermain bola?||Di taman kota||Di dapur||Di sekolah
Membaca tanda titik dan koma||Ayah membeli apel, pisang, dan jeruk. Ayah lalu pulang. Lani berhenti sebentar pada koma dan berhenti penuh pada titik.||Tanda apa yang memisahkan nama buah?||Koma||Tanda tanya||Tanda seru
Membaca tanda tanya dengan intonasi||'Di mana tasmu?' tanya Raka. 'Di atas kursi,' jawab Nisa. Raka membaca pertanyaan dengan nada bertanya.||Kalimat mana yang merupakan pertanyaan?||Di mana tasmu?||Di atas kursi.||Tas itu biru.
Membaca nyaring kegiatan sehari-hari||Setiap pagi Farel menyiram tanaman. Setelah itu, ia sarapan bersama keluarga. Farel membaca cerita kecil ini dengan suara jelas.||Apa yang Farel lakukan sebelum sarapan?||Menyiram tanaman||Bermain sepeda||Tidur siang
Membaca ulang agar lebih lancar||Pada bacaan pertama, Tika beberapa kali berhenti. Ia membaca kembali cerita tentang kucing. Bacaan kedua menjadi lebih lancar.||Mengapa Tika membaca kembali?||Agar lebih lancar||Agar bukunya rusak||Agar lupa cerita
Menyadari kata belum dipahami||Nanda membaca kata 'teduh' dalam cerita. Nanda belum tahu artinya. Ia bertanya kepada guru dan memahami bahwa teduh berarti tidak terkena panas matahari secara langsung.||Apa yang Nanda lakukan saat belum paham?||Bertanya kepada guru||Mengabaikan semua bacaan||Menutup mata
Menjelaskan isi kalimat||'Rusa minum air di tepi sungai.' Setelah membaca, Rino menjelaskan bahwa rusa sedang minum dekat sungai. Rino memahami isi kalimat.||Apa yang dilakukan rusa?||Minum air||Memanjat pohon||Memasak nasi
''')

add('Petualangan Kosakata Baru','C1–C3','Buat Kamus Foto Mini berisi kata pilihan, arti dalam bahasamu, dan contoh penggunaannya.',
['Menemukan Makna Kata','Memahami Hubungan Makna Kata','Memperkaya Kosakata Membaca'],
['Kosakata dalam Kehidupan','Menebak Makna dari Konteks','Kata Bermakna Mirip dan Berlawanan','Memilih Kata Sesuai Bacaan','Kelompok Kosakata','Menggunakan Kosakata Baru'],r'''
Kosakata benda dan kegiatan||Di dapur ada panci, sendok, dan gelas. Ibu mengaduk sup memakai sendok. Panci digunakan untuk memasak.||Alat apa yang dipakai Ibu mengaduk sup?||Sendok||Sepatu||Sisir
Menghubungkan kata dan peristiwa||Setelah hujan, halaman menjadi basah. Beni melihat genangan air di dekat pagar. Ia memahami kata 'genangan' dari air yang berkumpul.||Apa arti genangan pada bacaan?||Air yang berkumpul||Pasir yang beterbangan||Daun yang kering
Menebak makna melalui gambar||Foto memperlihatkan anak memakai payung di bawah hujan. Teksnya berbunyi 'Ayu berteduh'. Ayu melindungi tubuhnya dari hujan.||Apa arti berteduh di sini?||Berlindung dari hujan||Bermain di kolam||Menjemur baju
Menebak makna dari kalimat||Pak Tono rajin merawat kebun. Setiap hari ia menyiram tanaman dan mencabut rumput. Dari kalimat itu, kita tahu arti 'merawat'.||Apa maksud merawat kebun?||Menjaga kebun agar baik||Membiarkan kebun kotor||Menutup kebun selamanya
Menemukan kata bermakna mirip||Jalan menuju rumah Nia sangat sepi. Hanya sedikit orang lewat sehingga suasananya sunyi. Kata sepi dan sunyi memiliki makna mirip.||Kata mana yang mirip dengan sepi?||Sunyi||Ramai||Terang
Menemukan kata berlawanan||Pagi hari udara terasa dingin. Saat siang, udara menjadi panas. Dua kata ini menunjukkan keadaan berlawanan.||Lawan kata dingin adalah ...||Panas||Sejuk||Beku
Memilih kata dalam kalimat||Dina membawa botol air karena cuaca sangat panas. Ia merasa haus setelah bermain. Dina lalu minum air putih.||Kata apa yang tepat untuk keadaan Dina?||Haus||Kenyang||Mengantuk
Membedakan makna berdasarkan konteks||Kaki meja itu patah. Di lain waktu, kaki Toni sakit setelah berlari. Kata 'kaki' dapat menunjuk bagian meja atau tubuh.||Kaki pada 'kaki meja' berarti ...||Bagian penyangga meja||Bagian tubuh Toni||Kaki ayam di halaman
Mengelompokkan kata bertema sekolah||Di kelas ada papan tulis, meja, dan buku. Di kebun ada sekop dan selang. Farah memilah nama benda berdasarkan tempat.||Kata mana termasuk benda di kelas?||Papan tulis||Selang||Sekop
Membuat hubungan kata dan foto||Foto pertama menunjukkan wortel, foto kedua menunjukkan bayam. Keduanya termasuk sayuran yang dapat dimakan. Bima mengelompokkan kedua kata itu.||Wortel dan bayam termasuk ...||Sayuran||Alat musik||Kendaraan
Menjelaskan makna dengan kata sendiri||Kucing itu lincah. Ia melompat dan bergerak cepat saat bermain. Dara menjelaskan bahwa lincah berarti mudah bergerak.||Apa arti lincah?||Mudah bergerak cepat||Diam sepanjang hari||Sangat berat
Menggunakan kosakata pada bacaan lain||Dalam cerita pertama, kata 'rimbun' menggambarkan pohon dengan banyak daun. Dalam cerita kedua, Niko menemukan hutan yang rimbun. Ia memakai makna kata yang sudah dipelajari.||Apa ciri pohon yang rimbun?||Daunnya lebat||Tidak punya daun||Batangnya terbuat dari besi
''')

add('Detektif Informasi dalam Bacaan','C1–C3','Buat Kartu Detektif Bacaan. Temukan jawaban dan tunjukkan bagian teks yang menjadi bukti.',
['Menemukan Informasi Penting','Menjawab Pertanyaan Berdasarkan Teks','Menyajikan Informasi Bacaan'],
['Informasi Tokoh dan Peristiwa','Informasi Tambahan','Pertanyaan Langsung','Bukti Jawaban','Memilah Informasi','Menyampaikan Hasil Membaca'],r'''
Menemukan siapa dan apa||Pada hari Senin, Siska membawa bibit cabai ke sekolah. Ia akan menanam bibit itu bersama teman sekelas. Guru menyiapkan tanah dan pot.||Siapa yang membawa bibit cabai?||Siska||Guru||Penjaga sekolah
Menemukan tempat dan waktu||Sabtu pagi, Bayu pergi ke pasar bersama nenek. Mereka membeli sayur dan buah sebelum pulang.||Kapan Bayu pergi ke pasar?||Sabtu pagi||Minggu malam||Senin siang
Mengidentifikasi benda dalam teks||Rina menyiapkan tiga benda untuk melukis: kuas, cat air, dan kertas. Ia mengeluarkan semuanya dari tas.||Benda apa yang dipakai Rina untuk mengoles cat?||Kuas||Sendok||Sapu
Menemukan keterangan penting||Kereta wisata berangkat pukul sembilan pagi. Penumpang diminta datang lebih awal. Lala dan ayah tiba pukul delapan tiga puluh.||Pukul berapa kereta berangkat?||Pukul sembilan pagi||Pukul tujuh pagi||Pukul sebelas malam
Menjawab siapa apa di mana||Rudi menemukan dompet di depan perpustakaan. Ia menyerahkannya kepada petugas agar pemiliknya dapat mengambilnya.||Di mana Rudi menemukan dompet?||Di depan perpustakaan||Di kantin||Di lapangan bola
Menjawab berdasarkan kalimat||Bunga melati tumbuh di pot dekat jendela. Setiap pagi, Tia menyiraminya dengan air secukupnya.||Tanaman apa yang disiram Tia?||Melati||Mawar||Anggrek
Menunjukkan tempat jawaban||Di baris pertama tertulis, 'Doni berangkat sekolah dengan sepeda.' Baris berikutnya bercerita tentang jalan yang dilalui. Guru meminta anak menemukan kalimat tentang kendaraan Doni.||Di kalimat yang mana kendaraan Doni disebutkan?||Kalimat pertama||Kalimat terakhir tentang pulang||Tidak ada kalimatnya
Memilih jawaban sesuai bacaan||Sapi milik Pak Hadi makan rumput di padang. Setiap sore sapi itu kembali ke kandang. Pak Hadi menyiapkan air minum.||Apa makanan sapi dalam cerita?||Rumput||Roti cokelat||Ikan goreng
Informasi disebutkan atau tidak||Cerita menyebutkan bahwa Lili memakai topi merah dan membawa tas biru. Cerita tidak menyebutkan warna sepatunya.||Informasi apa yang tidak disebutkan?||Warna sepatu Lili||Warna topi Lili||Warna tas Lili
Mengelompokkan jawaban dari teks||Nisa membeli mangga di pasar hari Minggu. Nisa pergi bersama ibu. Semua keterangan dapat dipisah menjadi siapa, apa, kapan, dan di mana.||Keterangan 'hari Minggu' menjawab pertanyaan ...||Kapan||Siapa||Di mana
Mengisi kartu informasi bacaan||Seekor kelinci putih tinggal di kebun. Setiap pagi ia memakan daun segar. Seno menulis kartu tokoh: kelinci putih.||Siapa tokoh dalam cerita?||Kelinci putih||Ikan biru||Burung merah
Menceritakan temuan informasi||Putri membaca berita sekolah tentang lomba kebersihan. Lomba diadakan Jumat di halaman sekolah. Ia menyampaikan kedua informasi itu kepada teman.||Di mana lomba kebersihan diadakan?||Halaman sekolah||Kolam renang||Terminal bus
''')

add('Memahami Kalimat dan Paragraf','C2–C4','Susun Puzzle Paragraf, lalu ceritakan kembali isinya dengan satu kalimat utama.',
['Menemukan Makna Kalimat','Memahami Paragraf Pendek','Mengurutkan dan Menyimpulkan Isi'],
['Informasi dalam Kalimat','Hubungan Antarkalimat','Topik Paragraf','Informasi dalam Paragraf','Mengurutkan Informasi','Menyampaikan Kembali Isi'],r'''
Menjelaskan arti kalimat||'Ibu mengangkat jemuran sebelum hujan.' Kalimat ini berarti ibu mengambil pakaian yang dijemur agar tidak basah saat hujan.||Mengapa ibu mengangkat jemuran?||Agar tidak kehujanan||Agar pakaian kotor||Agar halaman kosong untuk mobil
Menghubungkan kalimat dengan keadaan||'Lantai basah setelah dipel.' Di depan kelas ada papan bertuliskan hati-hati. Anak-anak berjalan pelan agar tidak terpeleset.||Apa yang sebaiknya dilakukan saat lantai basah?||Berjalan hati-hati||Berlari sangat cepat||Melompat tanpa melihat
Mengenali hubungan dua kalimat||Rafa membawa bekal dari rumah. Ia makan bekal itu saat istirahat. Kata 'itu' mengacu pada bekal Rafa.||Apa yang dimakan Rafa saat istirahat?||Bekalnya||Penggaris||Papan tulis
Melengkapi hubungan antarkalimat||Lampu kamar padam. Ayah memeriksa sakelar dan menyalakan lampu kembali. Ruangan menjadi terang.||Apa yang terjadi setelah ayah menyalakan lampu?||Kamar menjadi terang||Kamar banjir||Jendela tertutup sendiri
Menentukan topik paragraf||Di kebun sekolah tumbuh cabai, tomat, dan bayam. Siswa merawat tanaman itu setiap hari. Mereka senang melihat sayur tumbuh.||Apa topik paragraf?||Kebun sayur sekolah||Jadwal kereta||Bermain bola
Memilih judul paragraf||Setiap sore, Dedi memberi makan ikan. Ia juga mengganti air akuarium jika kotor. Ikan-ikan Dedi tampak sehat.||Judul mana paling sesuai?||Merawat Ikan di Rumah||Pergi ke Gunung||Membuat Layang-Layang
Menemukan informasi penting||Perpustakaan kelas buka saat istirahat. Semua murid boleh meminjam satu buku. Buku dikembalikan paling lambat hari Jumat.||Berapa buku yang boleh dipinjam satu murid?||Satu buku||Lima buku||Tidak boleh meminjam
Menghubungkan topik dan informasi||Kelinci membutuhkan makanan dan tempat yang bersih. Tono memberinya sayur dan membersihkan kandang setiap hari. Kelinci pun sehat.||Kalimat mana yang mendukung topik merawat kelinci?||Tono membersihkan kandang setiap hari||Tono membeli sepeda baru||Tono berenang di sungai
Mengurutkan tiga peristiwa||Pertama, Rani mencuci tangan. Kedua, ia duduk di meja makan. Ketiga, ia menikmati sarapan. Setelah itu, Rani merapikan piring.||Apa yang dilakukan Rani sebelum duduk makan?||Mencuci tangan||Merapikan piring||Tidur siang
Menentukan urutan kalimat||Mula-mula Ika menyiapkan pot. Lalu ia memasukkan tanah. Terakhir, ia menanam bibit dan menyiramnya.||Apa kegiatan setelah memasukkan tanah?||Menanam bibit||Membeli meja||Menyalakan lampu
Menceritakan isi paragraf||Pagi hari sekolah mengadakan kerja bakti. Semua siswa memungut sampah dan menyapu halaman. Halaman sekolah menjadi bersih.||Apa inti kegiatan dalam paragraf?||Membersihkan sekolah bersama||Berkemah di pantai||Belanja di pasar
Menyatakan isi utama satu kalimat||Rama berlatih bersepeda setiap sore. Ia memakai helm dan berlatih di tempat aman. Setelah beberapa hari, ia semakin seimbang.||Apa inti paragraf tentang Rama?||Rama berlatih bersepeda dengan aman||Rama membuat kue||Rama tidur sepanjang hari
''')

add('Menjelajahi Cerita Bergambar','C1–C4','Buat Buku Cerita Berurutan berisi empat sampai enam adegan dan bacakan kepada keluarga.',
['Mengenal Isi Cerita','Memahami Jalan Cerita','Menceritakan Kembali'],
['Tokoh dan Latar','Peristiwa dalam Cerita','Urutan Cerita','Masalah dan Penyelesaian','Peta Cerita','Retelling atau Cerita Ulang'],r'''
Mengenali tokoh utama||Suatu pagi, Nala menolong anak kucing yang terjebak di balik pagar. Ia meminta bantuan ayah untuk membuka pintu pagar. Anak kucing kembali kepada induknya.||Siapa tokoh utama cerita?||Nala||Penjual roti||Petugas kereta
Mengenali tempat dan waktu||Minggu sore, Nino dan adiknya bermain di taman desa. Mereka melihat kupu-kupu hinggap pada bunga. Saat langit gelap, mereka pulang.||Di mana Nino bermain?||Di taman desa||Di perpustakaan kota||Di stasiun
Menemukan peristiwa awal||Pagi hari, Mia menemukan biji mangga di halaman. Ia menanamnya di pot kecil. Seminggu kemudian, biji itu mulai bertunas.||Apa peristiwa pertama?||Mia menemukan biji mangga||Biji mangga bertunas||Mia memetik mangga matang
Mengenali kejadian tokoh||Kiki membawa layang-layang ke lapangan. Angin bertiup kencang, sehingga layang-layangnya terbang tinggi. Tiba-tiba benang putus dan Kiki mengejarnya.||Apa yang terjadi pada layang-layang Kiki?||Benangnya putus||Warnanya berubah||Layang-layang basah oleh hujan
Membedakan awal tengah akhir||Pada awal cerita, Bimo kehilangan pensil. Di bagian tengah, ia mencari di tas dan meja. Pada akhir cerita, pensil ditemukan di dalam buku.||Apa yang terjadi di akhir cerita?||Pensil ditemukan di dalam buku||Bimo pergi ke kebun binatang||Bimo membeli topi
Mengurutkan cerita dari teks dan gambar||Pertama, Seli menyiapkan adonan. Lalu, ia membentuk bola-bola kecil. Sesudah dipanggang bersama ibu, kue siap dimakan.||Apa yang dilakukan sesudah membentuk adonan?||Memanggang kue||Mencuci sepeda||Menyiram pohon
Mengenali masalah tokoh||Rio ingin meminjam buku cerita, tetapi buku yang ia cari sedang dipinjam teman. Ia bertanya kepada pustakawan dan memilih cerita lain sementara waktu.||Apa masalah yang dialami Rio?||Buku yang dicari sedang dipinjam||Bukunya terlalu berat||Perpustakaan tutup selama setahun
Menjelaskan penyelesaian masalah||Hujan turun ketika Sasa akan pulang. Ia tidak membawa payung. Sasa menunggu di tempat aman, kemudian ayah menjemputnya.||Bagaimana masalah Sasa selesai?||Ayah menjemputnya||Sasa berjalan saat hujan deras||Sasa membuang tasnya
Membuat peta tokoh dan tempat||Lulu si kelinci tinggal di tepi hutan. Suatu hari Lulu mengunjungi Tobi si kura-kura di kolam. Mereka bermain sampai sore.||Siapa teman Lulu?||Tobi si kura-kura||Nina si ayam||Momo si kuda
Memilih gambar yang sesuai cerita||Cerita menyebutkan Andi memakai jas hujan kuning sambil berjalan di halaman yang basah. Gambar yang tepat perlu menunjukkan keadaan itu.||Gambar mana paling cocok?||Anak berjas hujan kuning di halaman basah||Anak berenang di kolam kering||Anak tidur di kamar cerah
Menceritakan urutan peristiwa||Dani menemukan burung kecil yang kehausan. Dani meletakkan air pada wadah dangkal. Burung itu minum lalu terbang kembali.||Urutan cerita yang benar adalah ...||Menemukan burung, memberi air, burung terbang||Burung terbang, Dani tidur, wadah pecah||Memberi makan ikan, berenang, pulang
Menyampaikan cerita dengan kata sendiri||Dara dan Lala menanam bunga bersama. Mereka bergantian menyiram dan merawat tanaman. Beberapa minggu kemudian, bunga bermekaran dan keduanya gembira.||Cerita ini paling tepat tentang ...||Dua teman merawat bunga bersama||Dua teman membeli telepon||Dua teman kehilangan sepatu
''')

add('Membaca Petunjuk dalam Kehidupan Sehari-hari','C2–C3','Buat Permainan Kecil berdasarkan petunjuk tertulis dan periksa apakah temanmu dapat mengikutinya.',
['Membaca Petunjuk Sederhana','Membaca Informasi Praktis','Menggunakan Informasi dalam Tindakan'],
['Mengenali Kalimat Petunjuk','Mengikuti Urutan Petunjuk','Tanda dan Pengumuman','Jadwal dan Daftar','Mempraktikkan Bacaan','Memecahkan Masalah'],r'''
Membaca petunjuk sehari-hari||Petunjuk mencuci tangan: basahi tangan, gunakan sabun, gosok telapak tangan, kemudian bilas hingga bersih. Lakukan sebelum makan.||Apa yang dipakai setelah membasahi tangan?||Sabun||Pasir||Tepung
Memahami tujuan petunjuk||Di pintu laboratorium tertulis: 'Gunakan alas kaki dan berjalan perlahan.' Petunjuk itu membantu pengunjung tetap aman.||Apa tujuan petunjuk itu?||Menjaga keselamatan||Membuat orang berlari||Mengundang bermain bola
Mengikuti petunjuk tiga langkah||Cara menyiapkan meja belajar: pertama rapikan buku, kedua letakkan pensil di tempatnya, ketiga bersihkan permukaan meja.||Apa langkah kedua?||Letakkan pensil di tempatnya||Rapikan buku||Nyalakan televisi
Melaksanakan kegiatan berurutan||Petunjuk menanam kacang: isi gelas dengan kapas basah, taruh biji di atasnya, lalu letakkan di tempat terang. Amati pertumbuhannya.||Apa yang dilakukan sesudah mengisi gelas dengan kapas?||Meletakkan biji di atas kapas||Memakan biji||Membuang gelas
Membaca tanda keselamatan||Pada tangga sekolah ada tulisan 'Pegang pegangan tangga'. Anak-anak membaca dan mengikuti petunjuk saat naik dan turun.||Apa yang perlu dilakukan di tangga?||Memegang pegangan tangga||Berlari sambil mendorong||Melompat melewati anak lain
Membaca pengumuman pendek||Pengumuman: 'Kerja bakti kelas II dilaksanakan Jumat pukul tujuh pagi. Bawa kain lap.' Murid membaca agar tidak lupa perlengkapan.||Apa yang harus dibawa?||Kain lap||Jaring ikan||Payung pantai
Membaca jadwal kegiatan||Jadwal perpustakaan kelas: Senin membaca cerita, Rabu membaca pengetahuan, Jumat berbagi buku. Lani ingin membaca buku pengetahuan.||Hari apa untuk membaca pengetahuan?||Rabu||Senin||Minggu
Membaca daftar perlengkapan||Daftar untuk kegiatan menggambar: kertas, pensil warna, penghapus, dan alas gambar. Edo mencocokkan isi tas dengan daftar itu.||Benda mana ada dalam daftar?||Penghapus||Panci||Sikat gigi
Membuat benda sesuai petunjuk||Petunjuk membuat penanda buku: gunting kertas tebal berbentuk panjang, tulis nama, lalu hias dengan gambar. Gunakan gunting dengan pengawasan orang dewasa.||Apa yang ditulis pada penanda buku?||Nama||Nomor kendaraan||Harga tiket
Memeriksa kesesuaian petunjuk||Lita membaca petunjuk: 'Simpan buku pada rak setelah dibaca.' Setelah membaca, ia meletakkan buku di lantai. Temannya mengingatkan isi petunjuk.||Apa yang seharusnya Lita lakukan?||Menaruh buku di rak||Meninggalkan buku di lantai||Melempar buku ke luar
Memilih petunjuk sesuai kebutuhan||Sepatu Dani basah setelah hujan. Ia membaca dua petunjuk: cara mengeringkan sepatu dan cara merawat tanaman. Ia memilih petunjuk yang sesuai.||Petunjuk mana yang dipilih Dani?||Cara mengeringkan sepatu||Cara menyiram tanaman||Cara membuat pesawat kertas
Menjelaskan akibat jika petunjuk diabaikan||Di kebun sekolah tertulis 'Jangan menginjak tanaman'. Jika anak-anak mengabaikannya, tanaman bisa rusak. Semua diminta melewati jalan setapak.||Mengapa tidak boleh menginjak tanaman?||Tanaman dapat rusak||Tanaman menjadi lebih tinggi||Tanah berubah menjadi es
''')

add('Memahami Perasaan dan Pesan Cerita','C2–C5','Pentaskan Teater Cerita Mini dan jelaskan pilihan tindakan tokoh dengan bukti cerita.',
['Membaca Dongeng dan Fabel','Memahami Perasaan dalam Bacaan','Menemukan Pesan Cerita'],
['Mengenali Cerita Imajinatif','Memahami Tindakan Tokoh','Mengenali Perasaan Tokoh','Membaca Puisi Anak','Pesan dan Nilai Kebaikan','Memberikan Tanggapan'],r'''
Membaca fabel pendek||Kelinci dan kura-kura berteduh di bawah pohon. Ketika hujan turun, kelinci mengajak kura-kura masuk ke lubang yang aman. Keduanya saling membantu.||Siapa yang diajak berteduh kelinci?||Kura-kura||Elang||Kupu-kupu
Mengenali sifat tokoh dari tindakan||Beruang kecil menemukan madu. Ia membaginya kepada teman-temannya yang belum makan. Teman-teman berterima kasih.||Sifat beruang kecil paling tepat adalah ...||Suka berbagi||Suka merebut||Tidak peduli teman
Menjelaskan alasan tindakan||Tupai mengumpulkan buah sebelum musim hujan. Ia menyimpannya di tempat aman agar tetap ada makanan saat hujan deras.||Mengapa tupai menyimpan buah?||Untuk persediaan makanan||Untuk membuang semua buah||Agar temannya lapar
Menghubungkan tindakan dengan akibat||Rusa muda tidak melihat jalan lalu tersandung akar. Sejak itu, rusa berjalan lebih hati-hati di hutan.||Apa akibat rusa tidak memperhatikan jalan?||Ia tersandung akar||Ia menjadi burung||Ia memperoleh sepeda
Menemukan kata perasaan||Setelah berhasil menemukan adiknya, Kila merasa lega. Ia tersenyum dan mengucapkan terima kasih kepada petugas taman.||Kata apa menunjukkan perasaan Kila?||Lega||Taman||Petugas
Memperkirakan perasaan tokoh||Ketika kado buatannya rusak, Danu menunduk dan matanya berkaca-kaca. Kakaknya datang membantu memperbaiki kado.||Bagaimana perasaan Danu saat kado rusak?||Sedih||Bangga karena menang||Mengantuk
Membaca puisi dengan ekspresi||Pagi datang membawa cahaya. Burung bernyanyi di halaman. Aku tersenyum menyambut hari. Puisi ini dibaca dengan suasana ceria.||Suasana puisi paling tepat adalah ...||Gembira||Menakutkan||Marah
Memahami perasaan dalam puisi||Di jendela kulihat hujan. Aku rindu bermain bersama teman. Semoga besok langit cerah. Pembaca puisi menyampaikan rasa rindu.||Apa perasaan yang muncul pada puisi?||Rindu||Kesal karena hadiah||Bangga menang lomba
Menemukan pesan melalui tindakan||Semut membantu temannya membawa makanan yang berat. Berkat kerja sama, makanan sampai di sarang. Keduanya merasa senang.||Apa pesan yang sesuai?||Kerja sama membuat tugas lebih ringan||Teman sebaiknya ditinggalkan||Makanan harus disembunyikan sendiri
Menghubungkan pesan dengan pengalaman||Alya mengembalikan pensil temannya yang tertinggal. Temannya merasa terbantu. Alya tahu bahwa kejujuran penting setiap hari.||Tindakan apa yang sesuai dengan pesan cerita?||Mengembalikan barang temuan||Menyembunyikan barang teman||Menyalahkan orang lain
Memilih tindakan yang patut dicontoh||Burung pipit melihat sarang temannya jatuh. Pipit segera memanggil teman lain untuk membantu memperbaiki sarang.||Tindakan mana yang patut dicontoh?||Mengajak teman membantu||Menertawakan sarang yang jatuh||Meninggalkan teman tanpa alasan
Memberikan alasan berdasarkan cerita||Kancil berjanji akan datang membantu kelinci, tetapi ia lupa. Kelinci menunggu sendirian. Sesudah itu, kancil meminta maaf dan belajar menepati janji.||Mengapa kancil sebaiknya menepati janji?||Agar temannya dapat percaya||Agar kelinci semakin kecewa||Agar tidak perlu saling membantu
''')

add('Membaca untuk Menambah Pengetahuan','C1–C4','Buat Ensiklopedia Foto Mini tentang hewan atau tumbuhan dengan informasi yang ditemukan dalam bacaan.',
['Membaca Teks Pengetahuan','Menghubungkan Teks dan Gambar','Menyusun Pengetahuan dari Bacaan'],
['Mengenal Bacaan Nonfiksi','Memahami Informasi','Memahami Gambar Informasi','Membaca Informasi Visual Sederhana','Mengelompokkan Informasi','Menjelaskan Pengetahuan'],r'''
Membaca pengetahuan tentang hewan||Kupu-kupu memiliki sepasang antena dan dua pasang sayap. Kupu-kupu mengisap nektar dari bunga. Serangga ini membantu penyerbukan.||Apa yang diisap kupu-kupu dari bunga?||Nektar||Batu||Pasir
Membaca tentang kesehatan||Tubuh memerlukan air setiap hari. Minum air putih membantu menjaga kebutuhan cairan tubuh. Kita juga perlu mencuci tangan sebelum makan.||Apa minuman yang disebutkan bermanfaat bagi tubuh?||Air putih||Air sabun||Minyak goreng
Menemukan fakta dalam teks||Pohon mangga memiliki akar, batang, daun, bunga, dan buah. Akarnya menyerap air dari tanah. Buah mangga dapat dimakan ketika matang.||Apa fungsi akar yang disebutkan?||Menyerap air dari tanah||Menghasilkan suara||Menjadi sayap
Menjelaskan informasi dengan bahasa sendiri||Lebah hidup dalam kelompok. Sebagian lebah mengumpulkan nektar dari bunga. Mereka bekerja sama di dalam koloni.||Apa arti hidup dalam kelompok pada bacaan?||Lebah tinggal bersama sesamanya||Lebah hidup sendirian terus||Lebah tinggal di laut
Memahami keterangan foto||Foto menunjukkan anak membuang botol plastik ke tempat sampah khusus plastik. Keterangan foto berbunyi 'Memilah sampah membantu pengelolaan sampah'.||Apa yang sedang dilakukan anak pada foto?||Memilah sampah plastik||Membakar buku||Menanam padi
Menghubungkan gambar dan kalimat||Gambar menunjukkan tanaman kecil yang baru tumbuh. Teks menjelaskan bahwa biji memerlukan air untuk mulai tumbuh.||Apa hubungan gambar dengan teks?||Gambar memperlihatkan tanaman yang mulai tumbuh||Gambar menunjukkan kereta cepat||Teks membahas memasak sup
Membaca tabel kecil||Tabel tinggi tanaman: Senin 3 cm, Rabu 5 cm, Jumat 7 cm. Angka menunjukkan tanaman semakin tinggi.||Pada hari apa tinggi tanaman 7 cm?||Jumat||Senin||Selasa
Menemukan jawaban dari tabel||Daftar hewan: ayam bertelur, kucing melahirkan, bebek bertelur. Anak membaca untuk mengetahui cara berkembang biak.||Hewan mana yang melahirkan?||Kucing||Bebek||Ayam
Mengelompokkan fakta sesuai tema||Teks menyebutkan ikan bernapas dengan insang. Kucing bernapas dengan paru-paru. Kedua fakta berkaitan dengan cara hewan bernapas.||Topik bersama kedua fakta adalah ...||Cara hewan bernapas||Warna sepatu||Nama-nama planet
Membuat kartu informasi||Burung pipit memiliki paruh dan sayap. Ia dapat terbang dan memakan biji-bijian. Faris membuat kartu informasi sederhana.||Informasi apa yang sesuai untuk kartu burung pipit?||Memakan biji-bijian||Hidup di dasar laut||Tidak memiliki sayap
Menyampaikan tiga informasi||Dari bacaan tentang lidah buaya, Risa tahu daunnya tebal, mengandung gel, dan banyak ditanam di pot. Risa menyampaikan ketiga informasi itu.||Manakah informasi dari bacaan?||Daun lidah buaya tebal||Daun lidah buaya terbuat dari kertas||Lidah buaya hidup di bulan
Menghubungkan bacaan dengan lingkungan||Bacaan menjelaskan bahwa tanaman perlu cahaya matahari dan air secukupnya. Di rumah, Ina memindahkan pot ke tempat terang dan menyiramnya.||Apa penerapan yang tepat dari bacaan?||Merawat pot dengan cahaya dan air cukup||Menutup tanaman selamanya||Mengabaikan kebutuhan tanaman
''')

add('Menemukan Hubungan dan Membuat Prediksi','C2–C4','Buat Misteri Akhir Cerita: catat petunjuk, tulis prediksi, lalu cocokkan dengan kelanjutan cerita.',
['Memahami Sebab dan Akibat','Membuat Dugaan Berdasarkan Bacaan','Memeriksa Hasil Prediksi'],
['Mengenali Hubungan Peristiwa','Menjelaskan Hubungan','Mengenali Petunjuk','Membuat Prediksi','Membandingkan Dugaan dan Cerita','Menarik Pemahaman'],r'''
Menemukan penyebab peristiwa||Sejak pagi hujan turun terus. Air mulai menggenang di jalan rendah. Rafi memilih berjalan melalui jalan yang lebih tinggi.||Apa penyebab jalan rendah tergenang?||Hujan turun terus||Matahari bersinar||Jalan baru dicat
Menemukan akibat peristiwa||Sasa lupa menutup botol minumnya di dalam tas. Saat tas miring, air tumpah dan bukunya menjadi basah.||Apa akibat botol tidak ditutup?||Air tumpah dan buku basah||Tas berubah warna emas||Botol berisi pasir
Menjawab mengapa dari teks||Beni membawa jaket ketika pergi ke daerah pegunungan. Ia tahu udara di sana sering lebih dingin. Jaket membantunya tetap hangat.||Mengapa Beni membawa jaket?||Karena udara pegunungan dingin||Karena ingin berenang||Karena jaket dapat dimakan
Menjelaskan sebab-akibat||Adit menaruh sepeda di jalan masuk. Orang yang lewat sulit melintas. Adit lalu memindahkan sepedanya ke tempat yang tepat.||Mengapa Adit memindahkan sepeda?||Agar jalan masuk tidak terhalang||Agar hujan cepat berhenti||Agar sepeda bisa terbang
Menemukan petunjuk dalam teks||Mila melihat tanah pot sangat kering dan daun mulai layu. Ia menduga tanaman memerlukan air. Mila memeriksa tanah sebelum menyiram.||Petunjuk apa yang mendukung dugaan Mila?||Tanah kering dan daun layu||Pot berwarna hijau||Ada meja dekat jendela
Menghubungkan gambar dengan petunjuk||Foto menunjukkan anak memakai mantel tebal. Cerita menyebutkan angin dingin bertiup di pagi hari. Kedua petunjuk menunjukkan udara sedang dingin.||Dugaan apa yang didukung keduanya?||Udara sedang dingin||Udara sangat panas||Sedang berada di dalam oven
Memperkirakan peristiwa berikutnya||Dina menyiapkan bibit, tanah, dan pot. Ia membaca petunjuk menanam dengan saksama. Setelah mengisi pot dengan tanah, Dina mengambil bibit.||Apa yang kemungkinan dilakukan Dina berikutnya?||Menanam bibit dalam pot||Membawa pot ke kolam renang||Membuang semua tanah
Menjelaskan alasan prediksi||Langit terlihat gelap dan angin bertiup semakin kuat. Ibu memindahkan jemuran ke dalam rumah. Bima memperkirakan hujan segera turun.||Apa alasan prediksi Bima?||Langit gelap dan angin kuat||Langit selalu cerah||Ada buku di meja
Memeriksa prediksi dari akhir cerita||Nana menduga burung yang berdiri di depan jendela mencari makanan. Pada akhir cerita, burung mematuk biji-bijian yang disediakan ayah.||Apakah dugaan Nana didukung akhir cerita?||Ya, burung memakan biji-bijian||Tidak, burung membawa payung||Tidak ada cerita akhir
Menjelaskan dugaan yang berbeda||Riko mengira kotak di depan pintu berisi mainan. Setelah dibuka, ternyata kotak itu berisi buku hadiah dari bibi. Riko memperbaiki dugaannya.||Apa isi kotak sebenarnya?||Buku||Mainan mobil||Sepatu roda
Menyimpulkan dengan dua petunjuk||Ruang kelas sudah rapi. Kursi tersusun, papan bersih, dan tidak ada sampah di lantai. Siswa baru selesai kerja bakti.||Kesimpulan mana paling masuk akal?||Kelas telah dibersihkan||Kelas baru terkena banjir||Semua kursi hilang
Belajar dari hasil prediksi||Lina memperkirakan es batu akan tetap padat di bawah matahari. Setelah beberapa waktu, es mencair. Lina belajar memperbaiki dugaan menggunakan hasil pengamatan.||Apa yang dilakukan Lina setelah dugaan salah?||Memperbaiki dugaan dari pengamatan||Menghapus semua pelajaran||Menolak melihat hasil
''')

add('Membandingkan Informasi dari Bacaan','C2–C5','Buat Poster Perbandingan Dua Hewan berdasarkan dua teks dan tunjukkan bukti informasinya.',
['Membaca Dua Teks Bertema Sama','Memahami Perbedaan Informasi','Memeriksa Kesesuaian Informasi'],
['Mengenali Isi Dua Bacaan','Menemukan Persamaan','Membandingkan Isi','Membandingkan Kegunaan','Informasi yang Didukung Teks','Memeriksa Informasi Sederhana'],r'''
Menemukan informasi bacaan pertama||Teks A: Kucing memiliki kumis dan cakar. Kucing biasanya menyusui anaknya. Teks B: Ayam memiliki paruh dan sayap. Ayam berkembang biak dengan bertelur.||Menurut teks A, kucing memiliki ...||Kumis dan cakar||Sirip dan insang||Roda dan mesin
Menemukan informasi bacaan kedua||Teks A: Pohon kelapa dapat tumbuh di daerah pantai. Teks B: Pohon pinus banyak dijumpai di daerah pegunungan yang sejuk.||Menurut teks B, pohon pinus banyak dijumpai di ...||Daerah pegunungan||Dasar laut||Dalam lemari
Menemukan topik yang sama||Teks A menjelaskan cara merawat kucing. Teks B menjelaskan cara merawat kelinci. Kedua teks membahas kebutuhan hewan peliharaan.||Apa kesamaan topik kedua teks?||Perawatan hewan peliharaan||Cara membuat kue||Permainan tradisional
Mencari informasi pada kedua teks||Teks A: Kupu-kupu memerlukan bunga sebagai sumber nektar. Teks B: Lebah mengunjungi bunga untuk mencari nektar.||Apa informasi yang sama?||Keduanya mengunjungi bunga||Keduanya hidup di dalam air||Keduanya tidak memiliki sayap
Mengenali informasi yang berbeda||Teks A: Ikan bernapas dengan insang. Teks B: Kucing bernapas dengan paru-paru. Kedua hewan memiliki cara bernapas berbeda.||Apa perbedaan yang benar?||Ikan memakai insang, kucing memakai paru-paru||Ikan dan kucing memakai roda||Kucing memakai insang, ikan memakai paru-paru
Mengisi tabel persamaan dan perbedaan||Teks A: Sepeda memiliki dua roda dan digerakkan dengan kayuhan. Teks B: Sepeda motor memiliki dua roda dan memakai mesin.||Apa persamaan keduanya?||Sama-sama memiliki dua roda||Sama-sama tidak mempunyai roda||Sama-sama memakai layar
Memilih bacaan berdasarkan kebutuhan||Teks A berjudul 'Merawat Kaktus'. Teks B berjudul 'Merawat Ikan Hias'. Sinta ingin tahu cara memberi makan ikan.||Teks mana yang paling tepat Sinta baca?||Teks B tentang ikan hias||Teks A tentang kaktus||Keduanya tidak ada hubungannya
Memberi alasan memilih bacaan||Lukman perlu mencari petunjuk menjaga gigi. Ia menemukan buku A tentang kebersihan gigi dan buku B tentang cuaca.||Mengapa buku A lebih tepat dipilih?||Karena membahas kebersihan gigi||Karena membahas arah angin||Karena sampulnya paling tebal
Mencocokkan pernyataan dan teks||Teks berbunyi: 'Saat hujan, Dika membawa payung dan memakai sepatu yang tidak licin.' Temannya mengatakan Dika berenang di sungai.||Pernyataan mana didukung teks?||Dika membawa payung saat hujan||Dika berenang di sungai||Dika sedang naik pesawat
Menunjukkan bukti pada kalimat||Teks: 'Bebek memiliki kaki berselaput. Kaki itu membantu bebek bergerak di air.' Tuti berkata bebek memiliki kaki berselaput.||Kalimat mana mendukung pernyataan Tuti?||Bebek memiliki kaki berselaput||Tuti bermain di taman||Bebek terbang ke bulan
Mengenali informasi belum diketahui||Teks menyebutkan Seno memelihara dua ikan mas di akuarium. Teks tidak menyebutkan usia kedua ikan itu.||Informasi mana belum diketahui?||Usia ikan||Jumlah ikan||Tempat ikan dipelihara
Memeriksa informasi dengan bantuan||Pada kartu tertulis: 'Semua jamur aman dimakan.' Guru meminta anak tidak langsung mempercayainya dan bertanya kepada orang dewasa atau sumber tepercaya. Beberapa jamur beracun.||Apa langkah paling aman?||Memeriksa informasi kepada guru atau sumber tepercaya||Memakan semua jamur liar||Menyebarkan pesan tanpa memeriksa
''')

add('Aku Bisa Menilai dan Menanggapi Bacaan','C2–C5','Buat Kartu Rekomendasi Buku yang menjelaskan isi, alasan memilih, dan bukti dari bacaan.',
['Memilih Bacaan Sesuai Tujuan','Memberikan Pendapat tentang Bacaan','Menilai dan Merefleksikan Bacaan'],
['Memahami Tujuan Membaca','Mengenal Pilihan Bacaan','Menyampaikan Tanggapan','Memberikan Alasan','Menilai Tindakan Tokoh','Merefleksikan Pengalaman Membaca'],r'''
Membaca untuk mencari informasi||Ratu ingin mengetahui makanan burung kolibri. Ia memilih buku pengetahuan tentang burung, bukan buku cerita balap mobil.||Apa tujuan Ratu membaca?||Mencari informasi makanan burung||Membeli mobil||Membuat pakaian
Membaca untuk menikmati cerita||Sepulang sekolah, Fina memilih dongeng tentang hutan ajaib. Ia membaca karena ingin menikmati petualangan tokoh cerita.||Mengapa Fina membaca dongeng?||Untuk menikmati cerita||Untuk melihat jadwal kereta||Untuk menghitung berat badan
Mengenali judul dan sampul||Sampul buku bertuliskan 'Petualangan di Kebun'. Ada foto anak dan tanaman. Guru mengajak Beni memperkirakan isi berdasarkan judul dan sampul.||Buku itu kemungkinan membahas ...||Kegiatan di kebun||Perjalanan ke bulan||Perbaikan mesin kapal
Memilih buku sesuai minat||Rika suka hewan laut dan sudah lancar membaca teks pendek. Ia memilih buku bergambar dengan kalimat jelas tentang penyu.||Pilihan Rika sesuai karena ...||Topiknya disukai dan sesuai kemampuan||Semua halamannya kosong||Tidak ada kata yang dapat dibaca
Menjelaskan bagian favorit||Dalam dongeng, Sela membantu nenek menyeberang jalan. Indra menyukai bagian itu karena menunjukkan kepedulian.||Bagian mana yang disukai Indra?||Saat Sela membantu nenek||Saat langit tiba-tiba gelap||Saat tokoh membeli sepeda
Menjelaskan hal yang belum dipahami||Anak membaca kalimat tentang 'migrasi' burung. Ia belum mengerti kata itu lalu menandainya untuk ditanyakan. Guru menjelaskan migrasi sebagai perpindahan musiman.||Apa yang sebaiknya dilakukan saat belum memahami kata?||Menandai dan bertanya||Langsung menyerah membaca||Mengarang arti tanpa memeriksa
Menggunakan alasan dalam tanggapan||Nina berkata, 'Aku suka cerita ini karena tokohnya mau meminta maaf.' Nina menyebutkan bagian cerita yang membuatnya suka.||Apa alasan Nina menyukai cerita?||Tokohnya mau meminta maaf||Gambarnya tidak ada||Bukunya terlalu berat
Menghubungkan pendapat dan teks||Fadil menilai tokoh dalam cerita bertanggung jawab. Alasannya, tokoh membersihkan alat setelah dipakai, seperti tertulis dalam cerita.||Apa bukti tokoh bertanggung jawab?||Membersihkan alat setelah dipakai||Meninggalkan barang berserakan||Datang terlambat setiap hari
Memilih perilaku yang tepat||Ketika melihat teman jatuh, Tono membantunya berdiri. Sementara itu, teman lain hanya menertawakan. Tono menunjukkan sikap peduli.||Tindakan mana paling tepat ditiru?||Membantu teman berdiri||Menertawakan teman||Merekam untuk mengejek
Memberi alasan berdasar kejadian||Mira meminjam buku dari perpustakaan dan mengembalikannya sesuai jadwal. Ia tidak merusak halaman buku.||Mengapa tindakan Mira baik?||Karena menjaga dan mengembalikan buku tepat waktu||Karena menyembunyikan buku||Karena menghilangkan halaman
Menjelaskan pengetahuan baru||Sebelum membaca, Oki belum tahu bahwa penyu bertelur di pantai. Sesudah membaca teks, ia dapat menyebutkan tempat penyu bertelur.||Apa pengetahuan baru Oki?||Penyu bertelur di pantai||Penyu hidup di dalam pohon||Penyu beroda empat
Menentukan target membaca||Sinta sudah berani membaca di depan kelas, tetapi kadang melompati tanda koma. Ia ingin berlatih memberi jeda pada bacaan berikutnya.||Apa target membaca Sinta?||Berlatih jeda pada tanda koma||Berhenti membaca seluruhnya||Mengabaikan tanda baca
''')

add('Pembaca Cilik yang Kreatif','C3–C6','Selenggarakan Festival Literasi: buat buku mini, rekam bacaan, dan ceritakan karya kepada keluarga.',
['Mengembangkan Ide dari Bacaan','Menciptakan Karya Literasi','Merayakan Perkembangan Membaca'],
['Mengumpulkan Inspirasi','Merencanakan Karya','Mengembangkan Cerita','Menyajikan Hasil Membaca','Berbagi Karya','Menilai Perkembangan Diri'],r'''
Memilih bacaan yang menarik||Lana membaca tiga cerita pendek tentang kebun, laut, dan pegunungan. Ia paling menyukai cerita laut karena ingin mengenal penyu. Lana memilihnya untuk proyek akhir tahun.||Cerita apa yang dipilih Lana?||Cerita laut||Cerita kebun||Cerita pegunungan
Menentukan tokoh dan peristiwa favorit||Tomi menyukai cerita tentang anak yang menolong burung. Tokoh favoritnya adalah anak penolong, dan peristiwa favoritnya saat burung kembali terbang.||Peristiwa favorit Tomi adalah ...||Burung kembali terbang||Burung masuk ke lemari||Anak membeli sepeda
Membuat peta ide cerita||Rana membuat peta ide: tokoh Beni, tempat taman, masalah bola hilang, akhir bola ditemukan. Peta itu membantunya menyusun buku mini.||Apa masalah dalam peta ide Rana?||Bola hilang||Sepatu baru||Ayam bertelur
Memilih bentuk karya||Tia memahami cerita tentang hujan. Ia ingin menjelaskan awal, tengah, dan akhir cerita dengan tiga gambar yang diberi kalimat singkat.||Bentuk karya yang paling sesuai adalah ...||Cerita bergambar berurutan||Daftar belanja tanpa gambar||Jadwal kereta antarkota
Membuat akhir cerita baru||Akhir asli: kucing kecil pulang sendiri ke rumah. Rani membuat akhir baru: kucing dibantu anak untuk menemukan jalan pulang. Keduanya sesuai dengan tokoh kucing yang tersesat.||Akhir baru buatan Rani adalah ...||Anak membantu kucing pulang||Kucing berubah menjadi kapal||Rumah kucing terbang ke bulan
Membuat cerita dari inspirasi||Setelah membaca kisah persahabatan, Dimas membuat cerita tentang dua teman yang menanam pohon. Ia mengambil pesan kerja sama, tetapi membuat tokoh dan peristiwa sendiri.||Apa pesan yang digunakan Dimas?||Kerja sama||Saling mengejek||Tidak mau berbagi
Membuat buku mini||Buku mini buatan Nia memiliki sampul, empat halaman cerita, dan halaman penutup. Setiap halaman memuat gambar serta satu atau dua kalimat.||Bagian apa yang ada pada buku mini Nia?||Sampul dan halaman cerita||Hanya satu angka||Hanya daftar harga
Mempresentasikan karya||Tari menunjukkan buku mininya di depan kelompok. Ia menyebutkan judul, tokoh, dan pesan yang didapat dari bacaan. Teman-teman menyimak.||Apa yang disebutkan Tari saat presentasi?||Judul, tokoh, dan pesan||Nomor rumah semua teman||Harga semua makanan
Membacakan karya kepada keluarga||Setelah menyelesaikan bukunya, Iman membacakan cerita kepada adiknya. Iman berhenti di tanda titik dan memberi suara berbeda saat tokoh bertanya.||Apa yang diperhatikan Iman saat membaca nyaring?||Tanda baca dan intonasi||Warna lantai||Bentuk kursi
Memberikan apresiasi kepada teman||Fira mendengarkan Danu membaca cerita. Setelah selesai, Fira berkata, 'Bagian awal ceritamu jelas. Aku suka cara kamu membaca dialog.' Danu merasa dihargai.||Kalimat mana merupakan apresiasi yang baik?||Aku suka cara kamu membaca dialog||Ceritamu tidak perlu didengar||Jangan pernah membaca lagi
Membandingkan perkembangan membaca||Pada awal tahun, Wina sering tersendat ketika membaca paragraf. Kini ia dapat membaca lebih lancar dan menjelaskan isi. Guru membandingkan dua rekaman dengan bimbingan.||Apa perkembangan Wina?||Membaca lebih lancar dan memahami isi||Tidak pernah belajar membaca||Berhenti mencoba
Menyusun target kelas III||Setelah festival literasi, Bagas menulis target: membaca buku lebih beragam dan berani bertanya jika ada kata baru. Ia ingin terus berkembang di kelas III.||Apa target Bagas?||Membaca beragam buku dan bertanya||Menghindari semua buku||Membaca tanpa memahami sama sekali
''')

# Membangun 144 submateri / 576 kegiatan terpetakan ke 72 materi dan 36 subbab
assert len(CHAPTERS)==12,len(CHAPTERS)
sessions=[]
for ci,ch in enumerate(CHAPTERS,1):
    for si,e in enumerate(ch['items'],1):
        sb=(si-1)//4+1
        mt=(si-1)//2+1
        mid=(si-1)%2+1
        id_=f'ML2-{ci:02d}.{sb}.{(mt-1)%2+1}.{mid}'
        seed=ci*100+si
        opts=[e['jawaban'],*e['pengecoh']]
        random.Random(seed).shuffle(opts)
        sessions.append({'id':id_,'bab':ci,'bab_title':ch['title'],'subbab':sb,
          'subbab_title':ch['subbabs'][sb-1],'materi':(mt-1)%2+1,
          'materi_title':ch['materi'][mt-1], 'submateri':mid,
          'submateri_title':e['submateri'],'bloom':ch['bloom'],
          'bacaan':e['bacaan'],'pertanyaan':e['pertanyaan'],
          'opsi':opts,'jawaban':e['jawaban'],
          'proyek_bab':ch['project']})
assert len(sessions)==144
assert len(set(s['id'] for s in sessions))==144
for ch in CHAPTERS:
    assert len(set(x['submateri'] for x in ch['items']))==12
with (ROOT/'data-latihan.json').open('w',encoding='utf-8') as f:
    json.dump({'versi':'1.0','kelas':2,'program':'Membaca Lanjutan','bab':[{'nomor':i+1,'judul':ch['title'],'bloom':ch['bloom'],'proyek':ch['project']} for i,ch in enumerate(CHAPTERS)],'sesi':sessions},f,ensure_ascii=False,indent=2)
with (ROOT/'daftar-144-sesi.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ID','Bab','Judul Bab','Subbab','Judul Subbab','Materi','Judul Materi','Submateri','Judul Submateri','Bloom','Pertanyaan','Jawaban'])
    for s in sessions:w.writerow([s['id'],s['bab'],s['bab_title'],s['subbab'],s['subbab_title'],s['materi'],s['materi_title'],s['submateri'],s['submateri_title'],s['bloom'],s['pertanyaan'],s['jawaban']])
print('GENERATED',len(CHAPTERS),'bab',len(sessions),'sessions',len(sessions)*4,'activities; ids:',sessions[0]['id'],sessions[-1]['id'])
