const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const src=fs.readFileSync(__dirname+'/js/app.js','utf8');
const block=src.slice(src.indexOf('  function matchSpeech(actual,expected){'),src.indexOf('  function checkSpeech(expected,key){'));
assert.ok(block.includes('function matchSpeech'));
const context={};
vm.runInNewContext(`const norm=s=>String(s??'').toLocaleLowerCase('id-ID').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9\\s]/g,'').replace(/\\s+/g,' ').trim();\n${block}\nthis.matchSpeech=matchSpeech;`, context);
const c=context.matchSpeech;
for(const [spoken,target,expect] of [
  ['makan','a',false],['salah','a',false],['a','a',true],['baba','ba',false],
  ['mama','mama',true],['ini mama','mama',true],['papa','mama',false],
  ['sekolah','sekolah',true],['sekulah','sekolah',true],
  ['menggambar','mama',false],['kaki','kaki',true],['kaki','kaki kaki',false],
  ['kata','a',false]
]){assert.equal(c(spoken,target),expect,`${spoken} versus ${target}`)}
assert.ok(src.includes("if(target.length<=2)"),'short speech protected');
assert.ok(src.includes("mark(key,'terdeteksi')"),'machine-only result distinguished');
assert.ok(src.includes("markComprehension()"),'reading comprehension stored separately');
assert.ok(!src.includes("mark('read','otomatis');notify('Jawaban pemahaman"),'comprehension must not auto-grade oral reading');
assert.ok(src.includes('if(ocrPending)'),'OCR output blocked from auto-grading');
assert.ok(!src.includes("checkWriting(result,'OCR')"),'OCR must not grade automatically');
console.log('PASS 13 speech match cases + 6 safety assertions');
