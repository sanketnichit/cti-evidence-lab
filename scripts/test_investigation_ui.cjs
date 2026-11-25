/* Optional DOM integration checks. This does not replace browser visual QA.
 * node scripts/test_investigation_ui.cjs /path/to/jsdom [source-a.html source-b.html]
 * Build outputs/investigation/index.html first. jsdom is pinned to 26.1.0.
 */
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {webcrypto} = require('node:crypto');
const {JSDOM, VirtualConsole} = require(process.argv[2] ? path.resolve(process.argv[2]) : 'jsdom');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'outputs/investigation/index.html'), 'utf8');
const errors = [], blobs = [];
const consoleCapture = new VirtualConsole();
consoleCapture.on('jsdomError', e => errors.push(e.message));
const dom = new JSDOM(html, {runScripts:'dangerously', url:'http://localhost/', virtualConsole:consoleCapture, beforeParse(w) {
    w.TextDecoder = TextDecoder; w.TextEncoder = TextEncoder; w.Blob = Blob;
    Object.defineProperty(w, 'crypto', {value:webcrypto});
    w.URL.createObjectURL = blob => {blobs.push(blob); return 'blob:test';};
    w.URL.revokeObjectURL = () => {};
    w.HTMLAnchorElement.prototype.click = function() {};
}});
const w = dom.window, d = w.document;
const data = JSON.parse(d.getElementById('data').textContent);
function select(id, value) {d.getElementById(id).value=value; d.getElementById(id).dispatchEvent(new w.Event('change'));}
function click(id) {d.getElementById(id).click();}
function query(values) {values.forEach((v,i)=>select('q'+i,v));}
async function waitFor(predicate) {for(let i=0;i<200;i++){if(predicate())return; await new Promise(r=>setTimeout(r,10));}throw Error('Timed out waiting for local source check');}
async function sourceFile(raw) {
    Object.defineProperty(d.getElementById('sourcefile'), 'files', {configurable:true,value:[{arrayBuffer:async()=>Uint8Array.from(raw).buffer}]});
    d.getElementById('sourcefile').dispatchEvent(new w.Event('change'));
}
(async()=>{
    assert.match(d.getElementById('verdict').textContent,/No supporting sequence/);
    assert.match(d.getElementById('projection').textContent,/run_nslookup_batch/);
    assert.match(d.getElementById('projection').textContent,/run_adfind_batch/);
    let queryStates=0;
    for(const c of data.cases.filter(c=>['rdp','domain-controller'].includes(c.key))){select('case',c.key); for(const p of c.profiles){select('profile',p.name); for(const item of Object.values(p.answers)){
        query(item.answer.query);
        const heading=d.getElementById('verdict').querySelector('h2').textContent;
        const expected={SUPPORTED:'Supported in this interpretation',UNRESOLVED_MAPPING:'Unresolved mapping could change the answer',NOT_SUPPORTED:'No supporting sequence in the retained graph'}[item.answer.status];
        assert.equal(heading,expected);
        assert.equal(d.querySelectorAll('#sensitivity tbody tr').length,c.profiles.filter(x=>x.level===p.level).length);
        queryStates++;
    }}}
    assert.equal(queryStates,532);
    assert.equal(data.cases.length,6);
    select('case','dfir-hive');
    query(['T1048','T1098','T1486']);
    assert.match(d.getElementById('verdict').textContent,/Supported in this interpretation/);
    assert.match(d.getElementById('witnesses').textContent,/paragraph \d+/);
    select('case','dfir-netsupport');
    query(['T1105','T1059','T1560']);
    assert.match(d.getElementById('verdict').textContent,/No supporting sequence/);
    assert.match(d.getElementById('projection').textContent,/middle occurrences/);
    click('core'); assert.match(d.getElementById('verdict').textContent,/Supported in this interpretation/);
    assert.match(d.getElementById('witnesses').textContent,/rdp_dc/);
    assert.equal(d.getElementById('profile').value,'archive_mapping_withheld');
    query(['T1218','T1059','T1560']);
    assert.match(d.getElementById('verdict').textContent,/Unresolved mapping/);
    assert.match(d.getElementById('witnesses').textContent,/archive_results → T1560/);
    click('example'); click('download');
    const exported = await blobs.at(-1).text();
    const certificate=JSON.parse(exported);
    assert.deepEqual(certificate.answer.query,['T1560','T1059','T1560']);
    assert.equal(certificate.answer.status,'NOT_SUPPORTED');
    fs.writeFileSync(path.join(root,'outputs/investigation/ui-export.json'),exported);
    let sourceChecks=0;
    if(process.argv[3] && process.argv[4]) {
        for(const [key,filename] of [['rdp',process.argv[3]],['domain-controller',process.argv[4]]]) {
            select('case',key);
            if(key==='domain-controller'){select('profile','core_transfer_execution');query(['T1021','T1570','T1218']);}
            else {select('profile','proposed_cleanup_full_edges');query(['T1021','T1070','T1021']);}
            await sourceFile(fs.readFileSync(filename));
            await waitFor(()=>d.getElementById('sourceState').textContent.includes('Matching source loaded')||d.getElementById('sourceState').textContent.includes('does not match'));
            assert.match(d.getElementById('sourceState').textContent,/Matching source loaded/);
            assert.ok(d.querySelectorAll('blockquote').length>0);
            await sourceFile(Buffer.from('<p>Different source.</p>'));
            await waitFor(()=>d.getElementById('sourceState').textContent.includes('does not match'));
            sourceChecks++;
        }
    }
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({status:'PASS_DOM_INTEGRATION_NOT_VISUAL_BROWSER_QA',query_states:queryStates,matching_and_rejected_source_pairs:sourceChecks,export_verified:true,jsdom_version:require(path.join(path.dirname(require.resolve(process.argv[2]?path.resolve(process.argv[2]):'jsdom')),'../package.json')).version}));
    w.close();
})().catch(e=>{console.error(e);w.close();process.exitCode=1;});
