/* MMP Cerdas v1.4 — laporan diagnostik lokal tanpa data pribadi. */
(()=>{'use strict';
  const $=id=>document.getElementById(id);
  const items=[
    {id:'tts',title:'Suara guru virtual',note:'Apakah Bu Rani menyapa, menjelaskan ATP, dan suaranya jelas?'},
    {id:'asr',title:'Pengenalan suara / membaca',note:'Apakah kata yang terdeteksi sesuai dengan ucapan sebenarnya?'},
    {id:'ocr',title:'Pengenalan tulisan tangan',note:'Apakah hasil OCR mendekati tulisan anak?'},
    {id:'cloud',title:'Sinkronisasi Supabase',note:'Apakah progres muncul kembali setelah browser ditutup dan dibuka?'}
  ];
  let answers={tts:'belum',asr:'belum',ocr:'belum',cloud:'belum'};
  function getProgress(){
    let data;try{data=JSON.parse(localStorage.getItem('mmp_cerdas_anak_v1')||'null')}catch{return null}
    if(!data||!data.progress)return null;
    const counters={listen:0,read:0,write:0,speak:0};let withData=0;
    for(const session of Object.values(data.progress)){
      if(!session||typeof session!=='object')continue;
      withData++;
      for(const type of Object.keys(counters))if(session[type]?.state)counters[type]++;
    }
    return {sessions:withData,counters};
  }
  function deviceStatus(){
    const voices=('speechSynthesis' in window)?window.speechSynthesis.getVoices():[];
    const idVoices=voices.filter(v=>/^id(?:-|_)?id$/i.test(v.lang));
    const lines=[
      'Suara sintetis: '+('speechSynthesis' in window?'tersedia':'tidak tersedia'),
      'Suara bahasa Indonesia terdeteksi: '+(idVoices.length?'ada ('+idVoices.length+')':'belum diketahui / tidak ditemukan'),
      'Pengenal ucapan browser: '+(window.SpeechRecognition||window.webkitSpeechRecognition?'tersedia':'tidak tersedia'),
      'Akses mikrofon API: '+(navigator.mediaDevices?.getUserMedia?'tersedia (izin belum diuji)':'tidak tersedia'),
      'OCR tulisan: '+(window.Tesseract?'pustaka pernah dimuat':'akan dimuat saat latihan'),
      'Konfigurasi database: '+(window.MMP_CONFIG?.url?.includes('supabase.co')?'terisi':'belum terisi'),
      'Status sinkronisasi aplikasi: '+($('sync-status')?.textContent?.trim()||'belum tersedia')
    ];
    $('eval-device').textContent=lines.join('\n');
    const p=getProgress();$('eval-progress').textContent=p?`Progres perangkat: ${p.sessions} sesi tersimpan; Dengar ${p.counters.listen}, Baca ${p.counters.read}, Tulis ${p.counters.write}, Bicara ${p.counters.speak}.`:'Belum ada data progres perangkat untuk ditampilkan.';
  }
  function report(){const p=getProgress();const lines=[
    'EVALUASI MMP CERDAS v1.4 — TANPA NAMA SISWA',
    'Tanggal: '+new Date().toLocaleDateString('id-ID'),
    'Progres perangkat: '+(p?`${p.sessions} sesi; dengar ${p.counters.listen}, baca ${p.counters.read}, tulis ${p.counters.write}, bicara ${p.counters.speak}`:'tidak tersedia'),
    ...items.map(item=>`${item.title}: ${answers[item.id]==='baik'?'Berfungsi menurut pengamatan':answers[item.id]==='kurang'?'Perlu perbaikan':'Belum dinilai'}`),
    'Catatan: '+($('eval-note')?.value||'(tidak ada)'),
    'Catatan evaluasi ini bukan pengukuran akurasi ASR/OCR secara ilmiah. Tidak menyertakan rekaman suara maupun tulisan anak.'
  ];return lines.join('\n')}
  function init(){
    if(!$('eval-toggle'))return;
    const opts=[['belum','Belum dinilai'],['baik','Berfungsi menurut pengamatan'],['kurang','Perlu perbaikan']];
    $('eval-rows').innerHTML=items.map(item=>`<div class="eval-row"><label for="eval-${item.id}">${item.title}</label><select id="eval-${item.id}" aria-label="Pengamatan ${item.title}">${opts.map(o=>`<option value="${o[0]}">${o[1]}</option>`).join('')}</select><small class="secondary-note">${item.note}</small></div>`).join('');
    for(const item of items)$('eval-'+item.id).addEventListener('change',e=>{answers[item.id]=e.target.value});
    $('eval-toggle').addEventListener('click',()=>{
      const body=$('eval-body');body.hidden=!body.hidden;$('eval-toggle').setAttribute('aria-expanded',String(!body.hidden));
      if(!body.hidden)deviceStatus();
    });
    $('eval-check').addEventListener('click',deviceStatus);
    $('eval-copy').addEventListener('click',async()=>{
      const val=report();
      try{if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(val);$('eval-result').textContent='Laporan anonim berhasil disalin.';return}}catch{}
      const ta=document.createElement('textarea');ta.value=val;ta.style.width='100%';ta.rows=8;ta.setAttribute('aria-label','Laporan yang dapat disalin manual');
      $('eval-result').textContent='Salin laporan di kotak berikut secara manual:';$('eval-result').after(ta);ta.select();
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
