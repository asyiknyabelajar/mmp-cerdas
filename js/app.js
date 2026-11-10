/* MMP Cerdas v1 — aplikasi statis. Tidak merekam atau menyimpan audio/tinta anak. */
(()=>{'use strict';
  const COURSE=window.MMP_COURSE, CFG=window.MMP_CONFIG||{}, TTL=4*24*60*60*1000, STORE_KEY='mmp_cerdas_anak_v1';
  const tasks=['Dengarkan','Baca','Tulis','Bicara'], keys=['listen','read','write','speak'];
  const lessons=COURSE.chapters.flatMap(c=>c.sections.flatMap(s=>s.materials.flatMap(m=>m.lessons)));
  const byId=Object.fromEntries(lessons.map(l=>[l.id,l]));
  const $=id=>document.getElementById(id), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm=s=>String(s??'').toLocaleLowerCase('id-ID').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\s]/g,'').replace(/\s+/g,' ').trim();
  let profile=null, selected=lessons[0], tab=0, lastSpoken='', recognizing=null, listening=false, worker=null, supa=null, syncTimer=0, activeCloud=false, sessionStarted=false;
  let pen={canvas:null,ctx:null,down:false,hasInk:false};
  let recording=null,recordStream=null,recordUrl=null,recordTimeout=null;
  function getStore(){try{return localStorage.getItem(STORE_KEY)}catch{return null}}
  function setStore(v){try{localStorage.setItem(STORE_KEY,JSON.stringify(v));return true}catch{return false}}
  function removeStore(){try{localStorage.removeItem(STORE_KEY)}catch{}}
  function restore(){let v;try{v=JSON.parse(getStore()||'null')}catch{v=null}if(!v)return null;
    if(!v.lastActive||Date.now()-v.lastActive>=TTL){removeStore();return null}
    return {name:String(v.name||'').slice(0,24),progress:v.progress||{},projects:v.projects||{},lastActive:v.lastActive,lastLesson:v.lastLesson||lessons[0].id,cloud:!!v.cloud,consent:!!v.consent};
  }
  function touch(){if(!profile)return;profile.lastActive=Date.now();profile.lastLesson=selected.id;setStore(profile);if(activeCloud)queueCloud()}
  function queueCloud(){clearTimeout(syncTimer);syncTimer=setTimeout(()=>{uploadCloud().catch(err=>syncMsg('Daring tertunda: '+err.message))},2000)}
  function syncMsg(message){$('sync-status').textContent=message}
  async function loadScript(src){if(document.querySelector('script[data-source="'+src+'"]'))return;
    await new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=src;script.dataset.source=src;script.onload=resolve;script.onerror=()=>reject(Error('Gagal memuat pustaka daring. Periksa internet.'));document.head.append(script)});
  }
  async function initCloud(freshIdentity=false){if(!CFG.url||!CFG.publishableKey)throw Error('Proyek '+(CFG.projectName||'Supabase')+': alamat Project URL dan publishable key belum diisi pada js/config.js.');
    if(!/^https:\/\/[a-z0-9-]+\.supabase\.co\/?$/i.test(CFG.url))throw Error('Project URL Supabase tidak sesuai format.');
    if(/^sb_secret_|^eyJ/i.test(CFG.publishableKey)&&!/^sb_publishable_/i.test(CFG.publishableKey))throw Error('Gunakan publishable key, jangan secret key atau legacy JWT.');
    await loadScript('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js');
    supa=window.supabase.createClient(CFG.url,CFG.publishableKey,{auth:{persistSession:true,autoRefreshToken:true}});
    let {data:{session},error:sessionError}=await supa.auth.getSession();
    if(sessionError)throw sessionError;
    // Identitas anak tidak boleh memakai kembali akun anonim anak sebelumnya.
    // Supabase menyimpan sesi autentikasi di browser; pergantian anak harus membuat akun baru.
    if(freshIdentity&&session){const {error}=await supa.auth.signOut();if(error)throw error;session=null;}
    if(!session){const {error}=await supa.auth.signInAnonymously();if(error)throw error;}
    activeCloud=true;
  }
  async function uploadCloud(){if(!supa||!profile||!activeCloud)return;
    const {data:{user},error:userError}=await supa.auth.getUser();if(userError||!user)throw userError||Error('Sesi tidak tersedia');
    const record={id:user.id,nickname:profile.name,progress:profile.progress,projects:profile.projects,last_lesson:profile.lastLesson};
    const {error}=await supa.from('mmp_child_profiles').upsert(record,{onConflict:'id'});
    if(error)throw error;syncMsg('Progres tersinkron · Supabase');
  }
  async function maybeDownloadCloud(){if(!supa||!profile)return;
    const {data:{user}}=await supa.auth.getUser();if(!user)return;
    const {data,error}=await supa.from('mmp_child_profiles').select('nickname,progress,projects,last_lesson,last_active').eq('id',user.id).maybeSingle();
    if(error)throw error;
    if(data){const last=new Date(data.last_active).getTime();
      if(!last||Date.now()-last>=TTL){await supa.from('mmp_child_profiles').delete().eq('id',user.id);syncMsg('Profil daring lama telah kedaluwarsa');return}
      // Use the database for remote continuity, provided the session is still active.
      profile.progress={...(data.progress||{}),...profile.progress};profile.projects={...(data.projects||{}),...profile.projects};
      if(data.last_lesson)profile.lastLesson=data.last_lesson;
      setStore(profile);
    }
  }
  function say(text){lastSpoken=String(text);$('teacher-speech').textContent=text;
    if(!('speechSynthesis' in window)){notify('Suara otomatis tidak tersedia di browser ini.',true);return}
    window.speechSynthesis.cancel();const utter=new SpeechSynthesisUtterance(text);utter.lang='id-ID';utter.rate=Number($('tts-speed').value||'.88');utter.pitch=1.12;utter.volume=1;
    const voices=window.speechSynthesis.getVoices();const voice=voices.find(v=>/^id[-_]ID$/i.test(v.lang)&&/female|indonesia|google|microsoft|natural/i.test(v.name))||voices.find(v=>/^id[-_]ID$/i.test(v.lang));
    if(voice)utter.voice=voice;window.speechSynthesis.speak(utter);
  }
  function stopSound(){if('speechSynthesis' in window)window.speechSynthesis.cancel()}
  function speakLesson(){if(!profile)return;sessionStarted=true;const chapter=COURSE.chapters[selected.chapter-1];
    const hour=new Date().getHours();const greeting=hour<11?'Selamat pagi':hour<15?'Selamat siang':hour<18?'Selamat sore':'Selamat malam';
    const hasProgress=countDone()>0;const empathy=hasProgress?'Senang sekali kamu kembali belajar. Ibu melihat kamu sudah berlatih.':'Ibu senang bertemu denganmu hari ini. Kita mulai dari langkah kecil, ya.';
    const msg=`${greeting}, ${profile.name}! ${empathy} Sekarang kita belajar bab ${selected.chapter}, ${chapter.title}. Materi kita adalah ${selected.focus}. Tujuan pembelajaran: ${chapter.atp} Fokus kita hari ini adalah ${selected.title.toLowerCase()}. Pertama mendengarkan, lalu membaca, menulis, dan berbicara. Tidak harus langsung benar. Ibu siap menemanimu mencoba lagi.`;
    say(msg);touch();}
  function taskState(id,key){return profile?.progress?.[id]?.[key]?.state||''}
  function mark(key,state='latihan',transcript=''){if(!profile)return;
    profile.progress[selected.id]??={};profile.progress[selected.id][key]={state,time:new Date().toISOString(),source:state==='otomatis'?'auto':'latihan'};
    touch();renderTabs();refreshStats();renderNavigation();}
  function countDone(){return Object.values(profile?.progress||{}).reduce((n,p)=>n+keys.filter(k=>p[k]?.state).length,0)}
  function lessonDone(l){return keys.every(k=>taskState(l.id,k))}
  function refreshStats(){const done=countDone();$('sidebar-progress').style.width=(100*done/(lessons.length*4))+'%';$('sidebar-progress-text').textContent=`${done} dari ${lessons.length*4} latihan`;
    const n=keys.filter(k=>taskState(selected.id,k)).length;$('lesson-done').textContent=`${n} dari 4 kegiatan`;
    $('project-toggle').textContent=profile?.projects?.[selected.chapter]?'Proyek selesai ✓':'Tandai proyek sudah dipresentasikan';
  }
  function renderNavigation(){const root=$('outline-list');root.innerHTML=COURSE.chapters.map(c=>`<details data-chapter="${c.number}" ${c.number===selected.chapter?'open':''}><summary>Bab ${c.number} · ${esc(c.title)}</summary><div class="chapter-lessons">${c.sections.map(s=>`<div class="section-label">${c.number}.${s.number} · ${esc(s.title)}</div>${s.materials.map(m=>`<div class="material-label">${c.number}.${s.number}.${m.number} · ${esc(m.title)}</div>${m.lessons.map(l=>`<button type="button" class="lesson-link ${l.id===selected.id?'active':''} ${lessonDone(l)?'complete':''}" data-id="${l.id}" title="${esc(l.title)}"><span class="dot"></span>${esc(l.title)}</button>`).join('')}`).join('')}`).join('')}</div></details>`).join('');
    root.querySelectorAll('button[data-id]').forEach(btn=>btn.addEventListener('click',()=>goLesson(btn.dataset.id,true)));
  }
  function setQueryLesson(id){try{const u=new URL(location.href);u.searchParams.set('lesson',id);history.replaceState({},'',u.toString())}catch{}}
  function goLesson(id,userAction=false){if(!byId[id])return;cleanupRecording();stopSound();if(recognizing)try{recognizing.abort()}catch{};
    selected=byId[id];tab=0;$('task-feedback').textContent='';$('task-feedback').classList.remove('warn');
    const chapter=COURSE.chapters[selected.chapter-1];const idx=lessons.indexOf(selected);
    $('chapter-kicker').textContent=`BAB ${selected.chapter} · ${chapter.title}`;
    $('lesson-title').textContent=selected.title;$('lesson-path').textContent=`${selected.chapter}.${selected.section} ${chapter.sections[selected.section-1].title} / ${selected.focus}`;
    $('lesson-code').textContent=selected.id;$('lesson-position').textContent=`Sesi ${idx+1} dari 96`;
    $('breadcrumb').textContent=`Bab ${selected.chapter} / Subbab ${selected.section} / Materi ${selected.material} / Submateri ${selected.number}`;
    $('goal-title').textContent=selected.focus;$('goal-text').textContent=`${chapter.atp} Fokus hari ini: ${selected.title}.`;
    $('teacher-speech').textContent=`Hai ${profile?.name||'teman kecil'}, kali ini kita belajar: ${selected.title.toLowerCase()}. Klik mulai agar Ibu menjelaskan ATP.`;
    $('project-name').textContent=chapter.project;$('project-info').textContent=`Proyek Bab ${chapter.number}: buat ${chapter.project.toLowerCase()} bersama pendamping. Gunakan hasil latihan membaca dan menulis, kemudian tunjukkan atau bacakan kepada orang lain.`;
    $('prev-lesson').disabled=idx===0;$('next-lesson').disabled=idx===lessons.length-1;
    renderNavigation();renderTabs();renderTask();refreshStats();setQueryLesson(id);
    if(userAction){touch();if(window.innerWidth<=900)$('outline').classList.remove('show');speakLesson()}
  }
  function renderTabs(){const root=$('task-tabs');root.innerHTML=tasks.map((name,i)=>`<button class="task-tab ${tab===i?'active':''} ${taskState(selected.id,keys[i])?'done':''}" role="tab" aria-selected="${i===tab}" data-tab="${i}"><span class="num">${String(i+1).padStart(2,'0')} · ${taskState(selected.id,keys[i])?'SELESAI':'LATIHAN'}</span>${name}</button>`).join('');
    root.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{tab=Number(b.dataset.tab);$('task-feedback').textContent='';touch();renderTabs();renderTask()}));
  }
  function notify(s,warn=false){$('task-feedback').textContent=s;$('task-feedback').classList.toggle('warn',!!warn)}
  function renderTask(){cleanupRecording();const t=selected.practice;const root=$('task-area');
    if(tab===0){root.innerHTML=`<h3>Latihan 1 · Mendengarkan</h3><p class="hint">Dengarkan Bu Rani menyebutkan contoh. Pilih kartu yang sama dengan bunyi yang Ibu ucapkan. Ketuk "Dengar pilihan" bila belum bisa membaca.</p><div class="action-row"><button id="listen-instruction" class="btn gold">Dengarkan soal</button></div><div class="choices">${t.listen.options.map((choice,i)=>`<div><button class="choice" data-choice="${i}" style="width:100%">${esc(choice)}</button><button class="choice-opt" data-hear="${i}">Dengar pilihan ${i+1}</button></div>`).join('')}</div>`;
      $('listen-instruction').onclick=()=>{say(t.listen.speech);touch()};
      root.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{const choice=t.listen.options[Number(b.dataset.choice)];if(norm(choice)===norm(t.listen.answer)){mark('listen','otomatis');notify('Hebat! Kamu memilih bunyi yang tepat.');say(`Bagus ${profile.name}! Itu benar, ${choice}.`)}else{notify('Belum cocok. Dengarkan suara Bu Rani sekali lagi, ya.',true);say('Belum tepat, tidak apa-apa. Kita dengarkan ulang, ya.')}});
      root.querySelectorAll('[data-hear]').forEach(b=>b.onclick=()=>{say(t.listen.options[Number(b.dataset.hear)]);touch()});
    }else if(tab===1){root.innerHTML=`<h3>Latihan 2 · Berlatih membaca</h3><p class="hint">${esc(t.read.instruction)}</p><div class="large-read ${t.read.question?'passage-read':''}">${esc(t.read.display)}</div>${t.read.question?`<div class="comprehension"><strong>Pahami bacaan: ${esc(t.read.question)}</strong><div class="choices">${t.read.options.map((option,i)=>`<button class="choice" data-read-choice="${i}">${esc(option)}</button>`).join('')}</div></div><p class="hint">Untuk pemeriksaan mikrofon, bacalah bagian berikut: <strong>${esc(t.read.checkTarget)}</strong></p>`:''}<div class="action-row"><button id="read-example" class="btn gold">Dengar contoh</button><button id="read-mic" class="btn primary">Baca dengan mikrofon</button><button id="read-manual" class="btn light">Sudah berlatih bersama pendamping</button></div><div class="record-panel"><button id="record-start" class="btn outline small">Rekam suaraku</button><button id="record-stop" class="btn light small" hidden>Hentikan rekaman</button><audio id="record-playback" controls hidden aria-label="Putar rekaman suara sendiri"></audio><small>Rekaman hanya berada sementara di memori browser; tidak disimpan dalam database.</small></div><div class="speech-transcript" id="mic-status">Hasil pengenal suara akan muncul di sini. Gunakan mikrofon dengan izin orang tua/wali.</div>`;
      $('read-example').onclick=()=>{say(t.read.display);touch()};$('read-mic').onclick=()=>checkSpeech(t.read.checkTarget||t.read.display,'read');
      root.querySelectorAll('[data-read-choice]').forEach(b=>b.onclick=()=>{const choice=t.read.options[Number(b.dataset.readChoice)];if(norm(choice)===norm(t.read.answer)){mark('read','otomatis');notify('Jawaban pemahaman bacaan tepat. Bagus!');say(`Betul ${profile.name}, ${choice}.`)}else{notify('Ayo baca lagi bagian ceritanya dan pilih jawaban yang sesuai.',true);say('Tidak apa-apa, mari baca ceritanya sekali lagi.') }});
      $('read-manual').onclick=()=>{mark('read','latihan');notify('Latihan tercatat. Minta pendamping memastikan kata telah dibaca dengan benar.');say(`Bagus sudah mencoba, ${profile.name}. Kita akan semakin lancar dengan latihan.`)};setupRecording();
    }else if(tab===2){root.innerHTML=`<h3>Latihan 3 · Berlatih menulis</h3><p class="hint">${esc(t.write.instruction)} Kamu dapat mengetik atau menggambar tulisan di papan putih.</p><div class="large-read">${esc(t.write.answer)}</div><label for="typing" class="eyebrow">Ketik jawaban di sini</label><input id="typing" class="text-answer" autocomplete="off" autocapitalize="off" placeholder="Tulis jawabanmu..." aria-label="Jawaban tertulis"><div class="action-row"><button id="check-typing" class="btn primary">Periksa ketikan</button><button id="write-example" class="btn light">Dengar kata</button></div><p class="hint" style="margin-top:20px">Atau tulis dengan jari / pena digital pada papan berikut:</p><canvas id="draw-board" class="writing-board" aria-label="Papan untuk menulis tangan" width="640" height="220"></canvas><div class="action-row"><button id="ocr-check" class="btn gold">Kenali tulisan tangan (OCR)</button><button id="draw-clear" class="btn light">Bersihkan papan</button><button id="draw-practice" class="btn outline">Tandai sudah berlatih menulis</button></div><p class="secondary-note">OCR dapat keliru membaca tulisan tangan anak. Tulisan tidak diunggah oleh aplikasi; mesin OCR dimuat di browser dari pustaka daring saat diperlukan.</p><div id="ocr-result" class="drawing-preview hide"></div>`;
      $('write-example').onclick=()=>{say(t.write.answer);touch()};$('check-typing').onclick=()=>checkWriting($('typing').value,'ketikan');
      $('typing').onkeydown=e=>{if(e.key==='Enter')checkWriting($('typing').value,'ketikan')};
      $('draw-clear').onclick=()=>{clearCanvas();touch()};$('ocr-check').onclick=recognizeInk;
      $('draw-practice').onclick=()=>{if(!pen.hasInk){notify('Silakan menulis di papan terlebih dahulu.',true);return}mark('write','latihan');notify('Usaha menulis tercatat. Pendamping dapat membantu mengecek bentuk huruf dan urutannya.');say('Terima kasih sudah berusaha menulis. Ibu bangga kamu mencoba.')};
      initCanvas();
    }else{root.innerHTML=`<h3>Latihan 4 · Berlatih berbicara</h3><p class="hint">${esc(t.speak.instruction)}</p><div class="large-read">${esc(t.speak.target)}</div><div class="action-row"><button id="speak-example" class="btn gold">Dengar contoh</button><button id="speak-mic" class="btn primary">Bicara dengan mikrofon</button><button id="speak-manual" class="btn light">Sudah berbicara bersama pendamping</button></div><div class="record-panel"><button id="record-start" class="btn outline small">Rekam suaraku</button><button id="record-stop" class="btn light small" hidden>Hentikan rekaman</button><audio id="record-playback" controls hidden aria-label="Putar rekaman suara sendiri"></audio><small>Rekaman hanya berada sementara di memori browser; tidak disimpan dalam database.</small></div><div class="speech-transcript" id="mic-status">Bicaralah dekat mikrofon, pelan, dan jelas. Coba beberapa kali bila pengenal suara belum tepat.</div>`;
      $('speak-example').onclick=()=>{say(t.speak.target);touch()};$('speak-mic').onclick=()=>checkSpeech(t.speak.target,'speak');
      $('speak-manual').onclick=()=>{mark('speak','latihan');notify('Latihan bicara tercatat tanpa penilaian otomatis. Pendamping dapat memberi umpan balik.');say(`Bagus ${profile.name}, terima kasih sudah mau berbicara.`)};setupRecording();
    }
  }
  function cleanupRecording(){clearTimeout(recordTimeout);
    if(recording&&recording.state==='recording'){recording.onstop=null;try{recording.stop()}catch{}}
    recordStream?.getTracks().forEach(t=>t.stop());recordStream=null;recording=null;
    if(recordUrl){URL.revokeObjectURL(recordUrl);recordUrl=null}
  }
  function setupRecording(){const start=$('record-start'),stop=$('record-stop');if(!start||!stop)return;
    start.onclick=async()=>{if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){notify('Perekam suara belum tersedia. Gunakan latihan mikrofon atau pendamping.',true);return}
      stopSound();cleanupRecording();
      try{recordStream=await navigator.mediaDevices.getUserMedia({audio:{noiseSuppression:true,echoCancellation:true,autoGainControl:true}});
        const chunks=[],rec=new MediaRecorder(recordStream);recording=rec;
        rec.ondataavailable=e=>{if(e.data?.size)chunks.push(e.data)};
        rec.onstop=()=>{recordStream?.getTracks().forEach(t=>t.stop());recordStream=null;
          if(!chunks.length)return;recordUrl=URL.createObjectURL(new Blob(chunks,{type:rec.mimeType||'audio/webm'}));
          const audio=$('record-playback');if(audio){audio.src=recordUrl;audio.hidden=false}
          if($('record-stop'))$('record-stop').hidden=true;if($('record-start'))$('record-start').disabled=false;
          notify('Rekaman sementara siap diputar. Dengarkan bersama pendamping, lalu ulangi jika perlu.');
        };
        rec.start();start.disabled=true;stop.hidden=false;
        notify('Sedang merekam suara. Setelah selesai, pilih Hentikan rekaman.');touch();
        recordTimeout=setTimeout(()=>{if(recording?.state==='recording')recording.stop()},12000);
      }catch(error){notify('Perekam suara gagal: '+error.message,true);cleanupRecording()}
    };
    stop.onclick=()=>{clearTimeout(recordTimeout);if(recording?.state==='recording')recording.stop()};
  }
  function checkWriting(value,mode){if(!value.trim()){notify('Coba ketik atau tulis jawabannya dahulu, ya.',true);return}
    const expected=norm(selected.practice.write.answer),actual=norm(value);if(expected===actual){mark('write','otomatis');notify(`Bagus, ${profile.name}! ${mode==='ketikan'?'Ketikan':'Tulisan yang terdeteksi'} cocok dengan contoh.`);say(`Luar biasa ${profile.name}, tulisanmu cocok!`)}
    else{notify(`Bu Rani membaca: “${value}”. Coba bandingkan dengan contoh: “${selected.practice.write.answer}”.`,true);say('Kamu sudah berusaha. Mari kita periksa huruf demi huruf, ya.')}
  }
  function matchSpeech(actual,expected){const a=norm(actual),e=norm(expected);if(!a||!e)return false;
    if(a===e||a.includes(e))return true; // Consider substring when recognizer adds words around target.
    const ed=(x,y)=>{const dp=Array.from({length:y.length+1},(_,j)=>j);for(let i=1;i<=x.length;i++){let prev=dp[0];dp[0]=i;for(let j=1;j<=y.length;j++){const old=dp[j];dp[j]=Math.min(dp[j]+1,dp[j-1]+1,prev+(x[i-1]===y[j-1]?0:1));prev=old}}return dp[y.length]};
    return e.length>=5 && Math.abs(a.length-e.length)<=1 && ed(a,e)<=1;
  }
  function checkSpeech(expected,key){const Speech=window.SpeechRecognition||window.webkitSpeechRecognition;
    if(!Speech){notify('Browser belum menyediakan pengenal suara. Gunakan Chrome/Edge terkini atau tombol latihan bersama pendamping.',true);return}
    if(listening){notify('Mikrofon masih digunakan. Silakan selesaikan dulu.',true);return}
    stopSound();const status=$('mic-status');if(status)status.textContent='Mendengarkan suara... silakan berbicara.';
    try{const rec=new Speech();recognizing=rec;listening=true;rec.lang='id-ID';rec.continuous=false;rec.interimResults=true;rec.maxAlternatives=5;
      let finalResults=[],received=false;
      rec.onresult=event=>{let interim='';for(let i=event.resultIndex;i<event.results.length;i++){
        const r=event.results[i],choices=Array.from(r).map(a=>String(a.transcript||''));
        if(r.isFinal){finalResults.push(...choices);received=true}else interim=choices[0]||'';
      }
      if(status)status.textContent=`Terdengar: ${finalResults[0]||interim||'...'}${interim?' (sedang diproses)':''}`;
      if(received){received=false;const candidates=[...new Set(finalResults)];if(candidates.some(t=>matchSpeech(t,expected))){mark(key,'otomatis',candidates[0]||'');notify('Bacaan dikenali sesuai target. Hebat! Hasil ini tetap perlu dikonfirmasi pendamping bila pelafalannya belum jelas.');say(`Bagus sekali ${profile.name}! Terus semangat, ya.`)}else{notify(`Terdeteksi “${candidates[0]||'-'}”. Targetnya “${expected}”. Mesin bisa keliru mengenali suara anak. Coba sekali lagi atau gunakan pendamping.`,true);}
      }};
      rec.onerror=ev=>{if(status)status.textContent='Mikrofon: '+ev.error;notify('Pengenalan suara tidak berhasil ('+ev.error+'). Coba ulangi atau minta pendamping mengecek.',true)};
      rec.onend=()=>{listening=false;recognizing=null};rec.start();touch();
    }catch(error){listening=false;recognizing=null;notify('Mikrofon tidak dapat dimulai: '+error.message,true)}
  }
  function initCanvas(){const canvas=$('draw-board'),ctx=canvas.getContext('2d',{willReadFrequently:true});pen={canvas,ctx,down:false,hasInk:false};
    clearCanvas();canvas.addEventListener('pointerdown',ev=>{ev.preventDefault();canvas.setPointerCapture(ev.pointerId);pen.down=true;pen.hasInk=true;const p=point(ev);ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x+.1,p.y+.1);ctx.stroke();touch()});
    canvas.addEventListener('pointermove',ev=>{if(!pen.down)return;ev.preventDefault();const p=point(ev);ctx.lineTo(p.x,p.y);ctx.stroke()});
    for(const name of ['pointerup','pointercancel','pointerleave'])canvas.addEventListener(name,()=>pen.down=false);
  }
  function point(ev){const r=pen.canvas.getBoundingClientRect();return{x:(ev.clientX-r.left)*pen.canvas.width/r.width,y:(ev.clientY-r.top)*pen.canvas.height/r.height}}
  function clearCanvas(){if(!pen.ctx)return;pen.ctx.fillStyle='#ffffff';pen.ctx.fillRect(0,0,pen.canvas.width,pen.canvas.height);pen.ctx.strokeStyle='#143f32';pen.ctx.lineWidth=12;pen.ctx.lineCap='round';pen.ctx.lineJoin='round';pen.hasInk=false;const info=$('ocr-result');if(info)info.classList.add('hide')}
  async function recognizeInk(){if(!pen.hasInk){notify('Tulislah dahulu di papan putih, ya.',true);return}const btn=$('ocr-check');btn.disabled=true;btn.textContent='Sedang mengenali tulisan...';
    try{if(!window.Tesseract)await loadScript('https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js');
      if(!worker){worker=await window.Tesseract.createWorker('eng',1);}
      const psm=selected.practice.write.answer.trim().length===1?window.Tesseract.PSM.SINGLE_CHAR:window.Tesseract.PSM.SINGLE_LINE;
      await worker.setParameters({tessedit_pageseg_mode:psm,tessedit_char_whitelist:'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,!?' });
      const {data}=await worker.recognize(pen.canvas);const result=(data.text||'').trim();const info=$('ocr-result');info.classList.remove('hide');
      info.textContent=`Hasil baca mesin: “${result||'(belum dikenali)'}”. Ini hanya perkiraan OCR. Kamu bisa memperbaiki hasilnya pada kotak ketikan sebelum dinilai.`;
      $('typing').value=result;if(result)checkWriting(result,'OCR');else notify('Mesin belum mengenali bentuk tulisan. Coba tulis lebih besar, atau minta bantuan pendamping.',true);
    }catch(error){notify('OCR tidak tersedia: '+error.message+'. Kamu tetap dapat mengetik atau meminta pendamping memeriksa tulisan.',true)}
    finally{btn.disabled=false;btn.textContent='Kenali tulisan tangan (OCR)'}
  }
  function startWorkspace(){document.body.classList.toggle('embed',new URLSearchParams(location.search).get('embed')==='1');$('welcome').hidden=true;$('workspace').hidden=false;
    $('teacher-hello').textContent=`Hai, ${profile.name}!`;const params=new URLSearchParams(location.search);
    const raw=params.get('lesson'), bab=Number(params.get('bab'))||0;
    const start=byId[raw]?raw:(bab>=1&&bab<=8?lessons.find(x=>x.chapter===bab)?.id:(byId[profile.lastLesson]?profile.lastLesson:lessons[0].id));
    goLesson(start,false);syncMsg(profile.cloud?'Menghubungkan database...':'Tersimpan di perangkat');}
  async function register(e){e.preventDefault();const name=$('child-name').value.trim();if(name.length<2){alert('Tuliskan nama panggilan minimal 2 huruf.');return}
    if(!$('guardian-agree').checked){alert('Izin orang tua/wali diperlukan untuk mulai.');return}
    const previous=restore(),sameChild=!!previous&&norm(previous.name)===norm(name);
    const cloud=$('cloud-optin').checked;
    // Hanya melanjutkan progres anak yang sama; nama berbeda berarti profil lokal baru.
    profile={name,progress:sameChild?previous.progress:{},projects:sameChild?previous.projects:{},lastActive:Date.now(),lastLesson:sameChild?previous.lastLesson:lessons[0].id,cloud,consent:true};setStore(profile);
    const btn=$('start-form').querySelector('button[type=submit]');btn.disabled=true;
    if(cloud){try{await initCloud(!sameChild||!previous.cloud);if(sameChild&&previous.cloud)await maybeDownloadCloud();await uploadCloud()}catch(err){activeCloud=false;alert('Penyimpanan daring belum bisa digunakan: '+err.message+'\nKemajuan tetap disimpan di perangkat.');profile.cloud=false;setStore(profile)}}
    startWorkspace();speakLesson();btn.disabled=false;
  }
  async function deleteAll(){const accepted=confirm('Hapus seluruh nama dan kemajuan anak? Data yang dihapus tidak dapat dipulihkan.');if(!accepted)return;
    stopSound();clearTimeout(syncTimer);
    // Delete remote first; on network failure, keep a warning and let the server's 4-day purge run.
    let errorMessage='';
    if(activeCloud&&supa){try{const {data:{user}}=await supa.auth.getUser();if(user){const {error}=await supa.from('mmp_child_profiles').delete().eq('id',user.id);if(error)throw error}}catch(e){errorMessage=e.message}}
    removeStore();profile=null;activeCloud=false;
    if(errorMessage)alert('Data perangkat sudah dihapus, tetapi data server belum terkonfirmasi terhapus: '+errorMessage+'\nCoba lagi saat online atau tunggu pembersihan berkala di server.');
    location.href=location.pathname+(new URLSearchParams(location.search).get('embed')==='1'?'?embed=1':'');
  }
  async function micTest(){const el=$('mic-test-status');if(!navigator.mediaDevices?.getUserMedia){el.textContent='Browser tidak memiliki izin akses mikrofon.';return}
    el.textContent='Memeriksa volume mikrofon tanpa menyimpan suara...';let stream,ctx;
    try{stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
      ctx=new (window.AudioContext||window.webkitAudioContext)();const source=ctx.createMediaStreamSource(stream),analyser=ctx.createAnalyser();analyser.fftSize=1024;source.connect(analyser);
      const values=new Uint8Array(analyser.fftSize);let best=0;
      for(let i=0;i<7;i++){await new Promise(r=>setTimeout(r,260));analyser.getByteTimeDomainData(values);let squares=0;for(const x of values){const f=(x-128)/128;squares+=f*f}best=Math.max(best,Math.sqrt(squares/values.length))}
      const pct=Math.min(100,Math.round(best*450));el.textContent=pct<4?'Suara sangat pelan atau belum terdengar. Dekatkan mikrofon dan ulangi.':pct>75?'Volume kuat. Jauhkan mikrofon sedikit untuk menghindari pecah suara.':`Mikrofon terdeteksi (indikator volume ${pct}/100). Berlatih di tempat tenang.`;
      touch();
    }catch(error){el.textContent='Uji mikrofon gagal: '+error.message}
    finally{stream?.getTracks().forEach(t=>t.stop());if(ctx)await ctx.close()}
  }
  function signOutUI(){stopSound();$('workspace').hidden=true;$('welcome').hidden=false;$('child-name').value=profile?.name||'';profile=null;activeCloud=false;clearTimeout(syncTimer);}
  function initEvents(){
    $('start-form').addEventListener('submit',register);
    $('play-lesson').onclick=speakLesson;$('teacher-repeat').onclick=()=>{if(lastSpoken)say(lastSpoken);else speakLesson();touch()};$('teacher-stop').onclick=stopSound;
    $('next-lesson').onclick=()=>goLesson(lessons[Math.min(lessons.length-1,lessons.indexOf(selected)+1)].id,true);
    $('prev-lesson').onclick=()=>goLesson(lessons[Math.max(0,lessons.indexOf(selected)-1)].id,true);
    $('outline-toggle').onclick=()=>$('outline').classList.toggle('show');$('change-user').onclick=signOutUI;
    $('erase-data').onclick=deleteAll;$('mic-test').onclick=micTest;
    $('project-toggle').onclick=()=>{profile.projects[selected.chapter]=!profile.projects[selected.chapter];touch();refreshStats();notify(profile.projects[selected.chapter]?'Proyek tercatat sebagai selesai. Ceritakan karyamu kepada Bu Rani!':'Tanda proyek selesai dibatalkan.')};
    window.addEventListener('message',ev=>{if(ev.data?.type==='MMP:navigate'&&typeof ev.data.id==='string'&&byId[ev.data.id]&&profile)goLesson(ev.data.id,true)});
    window.addEventListener('beforeunload',()=>{stopSound();cleanupRecording()});
  }
  function init(){initEvents();const existing=restore();if(existing?.name&&existing.consent){profile=existing;startWorkspace();if(profile.cloud){initCloud().then(async()=>{await maybeDownloadCloud();await uploadCloud();goLesson(profile.lastLesson,false)}).catch(e=>syncMsg('Lokal saja: '+e.message))}}}
  init();
})();
