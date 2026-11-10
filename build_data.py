import json, os, pathlib
base=pathlib.Path(__file__).parent
# Each leaf is an independently addressable lesson (96 leaves). Target is
# an age-adapted practice token, not an official government assessment item.
chapters=[
('Kesiapan Membaca dan Menulis','Kesiapan pramembaca, pramenulis, serta kesadaran bunyi.','Mengenali simbol, urutan bacaan, bunyi bahasa, dan membentuk pola dasar tulisan.','Buku Jejak Garis dan Bunyi',[
 ('Kesiapan Membaca',[
  ('Pengenalan Simbol dan Tulisan', [('Membedakan gambar, simbol, angka, huruf dan kata','a'),('Mengenal fungsi tulisan sehari-hari','nama')]),
  ('Arah dan Urutan Membaca', [('Membaca dari kiri ke kanan','i'),('Mengikuti urutan huruf dan kata dalam satu baris','u')])]),
 ('Kesadaran Bunyi Bahasa',[
  ('Mengenali Bunyi dalam Kata',[('Mengenali rima dalam kata','mama'),('Memecah kata menjadi suku kata','pa')]),
  ('Kesadaran Fonem Dasar',[('Mengenal bunyi awal kata','ba'),('Mengenal bunyi akhir kata','a')])]),
 ('Kesiapan Menulis',[
  ('Koordinasi Motorik Halus',[('Melatih koordinasi mata dan tangan','o'),('Memegang alat tulis dan mengatur kertas','l')]),
  ('Membuat Pola Dasar Tulisan',[('Membuat garis tegak, datar, dan miring','i'),('Membuat pola lengkung dan lingkaran','o')])])
]),
('Pengenalan Huruf dan Bunyi Dasar','Vokal dan konsonan awal melalui pendekatan fonik.','Mengenali bunyi dan bentuk huruf, lalu menggabungkannya menjadi suku kata.','Pohon Huruf dan Suku Kata',[
 ('Pengenalan Huruf Vokal',[
  ('Mengenal Bunyi Huruf Vokal',[('Mengenal bunyi a, i, u, e, o','a'),('Membedakan vokal dalam kata','i')]),
  ('Membaca dan Menulis Huruf Vokal',[('Membaca huruf kapital dan kecil','u'),('Menulis vokal secara terbimbing','e')])]),
 ('Pengenalan Konsonan Awal',[
  ('Konsonan M dan N',[('Mengenal bunyi dan bentuk m serta n','ma'),('Membaca dan menulis ma–mo serta na–no','na')]),
  ('Konsonan B dan P',[('Mengenal dan membedakan b serta p','ba'),('Membaca dan menulis ba–bo serta pa–po','pa')])]),
 ('Penggabungan Bunyi dan Huruf Dasar',[
  ('Menggabungkan Konsonan dan Vokal',[('Menggabungkan bunyi menjadi suku kata','mi'),('Membaca suku kata dengan urutan acak','bu')]),
  ('Menulis Suku Kata dan Kata Awal',[('Menyalin suku kata yang didengar','pipa'),('Membaca dan menulis kata sederhana','bibi')])])
]),
('Membaca dan Menulis Suku Kata','Penguatan suku kata terbuka dan kata dua atau tiga suku kata.','Menggabungkan suku kata menjadi kata baru serta menuliskannya sesuai bunyi.','Kereta Suku Kata',[
 ('Konsonan T, D, L, dan S',[
  ('Mengenali Bunyi dan Huruf',[('Mengenali bentuk t, d, l dan s','ta'),('Membedakan bunyi t, d, l dan s','da')]),
  ('Membaca dan Menulis Suku Kata',[('Membaca ta–to, da–do, la–lo dan sa–so','la'),('Menulis kata tali, susu, dan sapi','susu')])]),
 ('Konsonan K, G, R, dan H',[
  ('Mengenali Bentuk dan Bunyi Huruf',[('Mengenali huruf k, g, r dan h','ka'),('Menghubungkan konsonan dan bunyinya','ga')]),
  ('Membaca dan Menulis Suku Kata',[('Membaca ka–ko, ga–go, ra–ro dan ha–ho','ra'),('Menulis kata dengan bunyi baru','hari')])]),
 ('Pembentukan Kata dari Suku Kata',[
  ('Membaca Kata Berpola KV–KV',[('Merangkai suku kata ka-ki dan su-su','kaki'),('Membaca kata dua suku kata secara utuh','roda')]),
  ('Membaca dan Menulis Kata Tiga Suku Kata',[('Membaca kata tiga suku kata','kelapa'),('Menyusun dan menulis kata tiga suku kata','kepala')])])
]),
('Penguasaan Huruf dan Kata Sederhana','Melengkapi alfabet dan meningkatkan akurasi membaca-menulis kata.','Mengidentifikasi huruf lanjutan, membaca kata, dan menulis berdasarkan bunyinya.','Kamus Kata Pertamaku',[
 ('Konsonan C, J, W, dan Y',[
  ('Pengenalan Huruf Lanjutan',[('Mengenal bunyi c, j, w dan y','ca'),('Membedakan bentuk huruf lanjutan','ja')]),
  ('Membaca dan Menulis Kata',[('Membaca kata cuci, jari, wajah, yoyo','cuci'),('Menulis kata dengan huruf lanjutan','jari')])]),
 ('Pengenalan Huruf F, V, Z, Q, dan X',[
  ('Huruf F, V, dan Z',[('Mengenal huruf f, v dan z','foto'),('Menulis kata dengan f, v, dan z','vas')]),
  ('Huruf Q dan X',[('Mengenali q dan x di alfabet','q'),('Membedakan bentuk q dan x','x')])]),
 ('Penguatan Membaca dan Menulis Kata',[
  ('Ketepatan Pengenalan Huruf',[('Membedakan b–d dan p–q','b'),('Membaca kata dengan urutan bervariasi','buku')]),
  ('Menulis Kata Secara Mandiri',[('Menulis kata berdasarkan dikte','mata'),('Memeriksa urutan huruf pada kata','sapu')])])
]),
('Pola Kata dan Bunyi Lanjutan','Suku kata tertutup, ng, ny, dan variasi vokal.','Membaca dan menulis kata dengan pola KVK dan gabungan huruf.','Laboratorium Kata',[
 ('Suku Kata Tertutup',[
  ('Pola Konsonan–Vokal–Konsonan',[('Membaca suku kata tas, rak, kan, man','tas'),('Membedakan pola KV dan KVK','rak')]),
  ('Membaca dan Menulis Kata Berpola Campuran',[('Membaca makan, minum, pensil, lampu','makan'),('Menulis kata terbuka dan tertutup','minum')])]),
 ('Gabungan Huruf Konsonan',[
  ('Gabungan Huruf NG',[('Mengenali gabungan huruf ng','singa'),('Membaca dan menulis bunga serta pulang','bunga')]),
  ('Gabungan Huruf NY',[('Mengenali gabungan huruf ny','nyamuk'),('Membaca dan menulis kata dengan ny','senyum')])]),
 ('Variasi Pola Huruf dan Bunyi',[
  ('Gabungan Vokal dalam Kata',[('Mengenali ai, au dan oi pada kata','pantai'),('Membedakan diftong dari vokal berurutan','pulau')]),
  ('Penguatan Pola Kata Beragam',[('Membaca berbagai pola suku kata','lampu'),('Menulis kata berpola campuran','pensil')])])
]),
('Membaca dan Menulis Kalimat Sederhana','Frasa, kalimat, ejaan dasar, dan tanda baca.','Memahami kalimat dan menulisnya dengan susunan serta ejaan sederhana.','Dinding Kalimat Pintar',[
 ('Membaca Frasa dan Kalimat',[
  ('Membaca Gabungan Kata',[('Membaca frasa buku baru dan bola biru','buku baru'),('Mengenali frasa yang bermakna','bola biru')]),
  ('Membaca Kalimat Sederhana',[('Membaca kalimat tentang aktivitas','Bima makan.'),('Menemukan pelaku dan tindakan dalam kalimat','Ibu baca buku.')])]),
 ('Menyusun dan Menulis Kalimat',[
  ('Menyusun Kata Menjadi Kalimat',[('Menyusun kartu kata acak','Bima makan nasi.'),('Melengkapi kalimat sederhana','Ibu minum susu.')]),
  ('Menulis Kalimat dengan Ejaan Dasar',[('Menggunakan kapital awal kalimat','Budi belajar.'),('Menggunakan spasi dan titik','Siti membaca.')])]),
 ('Membaca Kalimat dengan Tanda Baca',[
  ('Mengenal Intonasi Kalimat',[('Membaca kalimat pernyataan','Hari ini cerah.'),('Membaca kalimat tanya dan seru','Apa kabar?')]),
  ('Menulis Kalimat Berdasarkan Informasi',[('Menulis kalimat dari gambar','Aku baca buku.'),('Memperbaiki ejaan sederhana','Ibu di rumah.')])])
]),
('Membaca dan Menulis Teks Pendek','Membaca teks, memahami informasi, dan menulis deskripsi pendek.','Memahami bacaan pendek dan menghasilkan beberapa kalimat yang berkaitan.','Buku Cerita Mini Karyaku',[
 ('Membaca Teks Pendek',[
  ('Membaca Teks Dua hingga Empat Kalimat',[('Membaca bacaan pendek secara terbimbing','Aku suka buku.'),('Membaca ulang untuk meningkatkan kelancaran','Budi minum susu.')]),
  ('Memahami Isi Bacaan',[('Menemukan siapa, apa, dan di mana','Ibu pergi ke pasar.'),('Mencocokkan isi bacaan dan gambar','Bola ada di meja.')])]),
 ('Membaca Teks Fungsional Sederhana',[
  ('Membaca Informasi Sehari-hari',[('Membaca label dan daftar nama','Siti membaca.'),('Mengikuti petunjuk tertulis','Bima bermain.')]),
  ('Membaca Pesan Tertulis',[('Membaca catatan pendek','Ini daftar buku.'),('Menemukan informasi penting','Tolong tutup pintu.')])]),
 ('Menulis Teks Pendek',[
  ('Menulis Deskripsi Sederhana',[('Menulis dua atau tiga kalimat tentang benda','Buku itu baru.'),('Menulis kalimat dari pengamatan','Bunga merah.')]),
  ('Menulis Cerita Bergambar',[('Mengurutkan peristiwa dari gambar','Ibu pergi.'),('Menulis cerita dari urutan gambar','Aku belajar.')])])
]),
('Literasi Mandiri dan Penguatan MMP','Kelancaran, pemahaman, ekspresi, dan tulisan mandiri.','Membaca bacaan sesuai tingkat kemampuan dengan memahami isi serta menulis teks sederhana.','Festival Karya Literasi',[
 ('Kelancaran Membaca',[
  ('Ketepatan dan Kelancaran',[('Membaca kata dan kalimat secara lancar','Buku di meja.'),('Membaca ulang dengan tepat','Aku membaca lancar.')]),
  ('Membaca dengan Ekspresi Dasar',[('Mengikuti jeda tanda baca','Ayo, kita belajar!'),('Membaca intonasi sesuai makna','Apa kabarmu?')])]),
 ('Pemahaman Bacaan Mandiri',[
  ('Menemukan Informasi dalam Teks',[('Menemukan jawaban dalam bacaan','Budi pergi sekolah.'),('Menghubungkan bacaan dan pengalaman','Ibu membuat kue.')]),
  ('Menceritakan Kembali Bacaan',[('Mengurutkan kejadian sederhana','Siti pergi ke taman.'),('Menceritakan isi bacaan dengan suara','Bima membawa buku.')])]),
 ('Menulis Mandiri dan Portofolio Literasi',[
  ('Menulis Teks dari Pengalaman',[('Menulis kalimat dari pengalaman','Pagi hari.'),('Menyusun beberapa kalimat berurutan','Kami bermain.')]),
  ('Memeriksa dan Mempublikasikan Tulisan',[('Memeriksa ejaan dan keterbacaan','Aku suka membaca.'),('Menyunting serta membacakan tulisan','Ini bukuku.')])])
])
]
# For the two text-literacy chapters, each reading exercise also has a short,
# original three-sentence passage and an actual comprehension question.
PASSAGES={
7:[
 ('Rani suka buku. Rani membaca buku pagi hari. Ia menjaga bukunya.','Siapa yang suka buku?','Rani',['Rani','Budi','Ibu']),
 ('Budi minum susu. Susu ada di gelas. Budi selesai minum.','Apa yang diminum Budi?','susu',['susu','air','teh']),
 ('Ibu pergi ke pasar. Ibu membeli sayur. Ibu pulang membawa tas.','Ke mana Ibu pergi?','pasar',['pasar','taman','kebun']),
 ('Bola ada di meja. Sita mencari bola. Sita menemukan bola itu.','Di mana bola berada?','meja',['meja','tas','kamar']),
 ('Siti membaca tulisan. Tulisan ada di papan. Siti membaca pelan.','Siapa yang membaca?','Siti',['Siti','Bima','Ayah']),
 ('Bima bermain dengan teman. Mereka bermain di taman. Bima tersenyum.','Di mana mereka bermain?','taman',['taman','kelas','rumah']),
 ('Ini daftar buku. Ada buku cerita. Ada buku gambar.','Apa yang ada di daftar?','buku',['buku','sepatu','gelas']),
 ('Tolong tutup pintu. Angin bertiup kuat. Kakak menutup pintu.','Siapa yang menutup pintu?','Kakak',['Kakak','Adik','Guru']),
 ('Ibu pergi ke rumah nenek. Ibu membawa buah. Nenek senang.','Siapa yang senang?','Nenek',['Nenek','Budi','Siti']),
 ('Aku belajar menulis. Aku memakai pensil. Aku menulis namaku.','Apa alat untuk menulis?','pensil',['pensil','sendok','gelas']),
 ('Buku itu baru. Sampulnya biru. Budi menyimpannya di tas.','Apa warna sampul buku?','biru',['biru','merah','kuning']),
 ('Bunga merah tumbuh di halaman. Siti menyiram bunga. Bunganya segar.','Siapa menyiram bunga?','Siti',['Siti','Budi','Ayah'])],
8:[
 ('Buku ada di meja. Ayah membacanya. Ayah menaruhnya kembali.','Di mana buku berada?','meja',['meja','tas','lantai']),
 ('Aku membaca lancar. Aku berlatih tiap pagi. Ibu memujiku.','Kapan aku berlatih?','pagi',['pagi','malam','siang']),
 ('Ayo, kita belajar! Bu Rani mengajak anak membaca. Semua anak senang.','Siapa yang mengajak belajar?','Bu Rani',['Bu Rani','Bima','Ayah']),
 ('Apa kabarmu? Siti bertanya kepada Budi. Budi menjawab baik.','Bagaimana kabar Budi?','baik',['baik','sedih','lelah']),
 ('Budi pergi sekolah. Ia memakai sepatu. Ia membawa tas.','Ke mana Budi pergi?','sekolah',['sekolah','pasar','taman']),
 ('Ibu membuat kue. Kue itu manis. Kami makan bersama.','Apa yang Ibu buat?','kue',['kue','bubur','roti']),
 ('Siti pergi ke taman. Ia melihat bunga. Ia menyiram bunga.','Ke mana Siti pergi?','taman',['taman','pasar','kelas']),
 ('Bima membawa buku. Buku itu untuk Rani. Rani berterima kasih.','Untuk siapa buku itu?','Rani',['Rani','Ibu','Bima']),
 ('Pagi hari cerah. Ayam berkokok. Aku membuka jendela.','Kapan ayam berkokok?','pagi',['pagi','malam','sore']),
 ('Kami bermain di halaman. Kami bermain bola. Setelah itu kami minum.','Di mana kami bermain?','halaman',['halaman','kelas','pasar']),
 ('Aku suka membaca. Aku punya buku cerita. Aku membaca bersama Ibu.','Bersama siapa aku membaca?','Ibu',['Ibu','Guru','Kakak']),
 ('Ini bukuku. Sampulnya hijau. Aku merawat buku ini.','Apa warna sampul?','hijau',['hijau','biru','merah'])]
}

assert len(chapters)==8
out=[]
for ci,(title,focus,atp,project,sections) in enumerate(chapters,1):
 assert len(sections)==3,(ci,'sections')
 c=dict(number=ci,title=title,focus=focus,atp=atp,project=project,sections=[])
 for si,(st,mats) in enumerate(sections,1):
  assert len(mats)==2,(ci,si,'mats')
  s=dict(number=si,title=st,materials=[])
  for mi,(mt,topics) in enumerate(mats,1):
   assert len(topics)==2,(ci,si,mi,'topics')
   m=dict(number=mi,title=mt,lessons=[])
   for ti,(tt,target) in enumerate(topics):
    suffix='A' if ti==0 else 'B'; lessonid=f'MMP-{ci}.{si}.{mi}-{suffix}'
    alternatives=[x[1] for sc in sections for mat in sc[1] for x in mat[1] if x[1]!=target]
    # Hard-code three alternate cards per lesson, rotate to vary choice placement.
    alt=[]
    for v in alternatives:
     if v not in alt: alt.append(v)
    opts=[target]+alt[:3]
    pos=((ci*5+si*3+mi+ti)%4)
    opts.insert(pos,opts.pop(0))
    objective=f'Anak dapat mempraktikkan: {tt.lower()}.'
    material_note=f'Kita belajar {mt.lower()}. Coba perhatikan, ucapkan, lalu tuliskan contoh yang Ibu berikan.'
    practice=dict(
      listen={'speech':f'Dengarkan dengan baik. Ibu menyebutkan: {target}. Sekarang pilih kartu yang cocok dengan bunyi yang kamu dengar.',
              'question':'Kartu mana yang sesuai dengan bunyi dari Bu Guru?', 'options':opts, 'answer':target},
      read={'display':target,'instruction':'Lihat tulisan ini. Dengarkan contohnya, kemudian bacalah dengan suara jelas.'},
      write={'answer':target,'instruction':f'Tulislah {target} di kotak jawaban, atau gambarlah tulisanmu pada papan tulis.'},
      speak={'target': target if ci<=4 else (f'Saya bisa membaca {target.rstrip(".!?")}' if ci<=6 else target),
             'instruction':'Ucapkan kalimat berikut kepada Bu Guru dengan suara tenang dan jelas.'}
    )
    if ci in PASSAGES:
      pi=(si-1)*4+(mi-1)*2+ti
      passage,question,correct,choices=PASSAGES[ci][pi]
      practice['read']['display']=passage
      practice['read']['checkTarget']=target
      practice['read']['instruction']='Bacalah cerita pendek tiga kalimat ini. Setelah itu jawab pertanyaannya dan coba mikrofon pada kalimat contoh.'
      practice['read']['question']=question
      practice['read']['answer']=correct
      practice['read']['options']=choices
    m['lessons'].append(dict(id=lessonid,number=ti+1,title=tt,target=target,focus=mt,objective=objective,
                    notes=material_note,atp=atp,chapter=ci,section=si,material=mi,practice=practice))
   s['materials'].append(m)
  c['sections'].append(s)
 out.append(c)
count=sum(len(m['lessons']) for c in out for s in c['sections'] for m in s['materials'])
assert count==96,count
(base/'js'/'course-data.js').write_text('/* 96 aktivitas MMP — data konten disusun untuk pengembangan pembelajaran, bukan soal resmi. */\nwindow.MMP_COURSE='+json.dumps({'version':'1.0.0','chapters':out},ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
(base/'docs'/'daftar-96-sesi.csv').write_text('id,bab,subbab,materi,submateri,target\n'+''.join(f'"{l["id"]}","{c["title"]}","{s["title"]}","{m["title"]}","{l["title"]}","{l["target"]}"\n' for c in out for s in c['sections'] for m in s['materials'] for l in m['lessons']),encoding='utf-8')
print(f'Wrote {count} unique content lessons, {count*4} activity definitions')
