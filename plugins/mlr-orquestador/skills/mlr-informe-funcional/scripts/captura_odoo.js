// In-page capture of Odoo screens for MLR functional guides.
//
// Why: the desktop Browser pane has no "save screenshot to disk", and while it is
// hidden the page has a 0x0 viewport. Emulating a 1440x900 viewport
// (Claude_Browser__resize_window) makes Odoo lay out; this helper rasterises the
// DOM with html-to-image and stores the JPEG as an ir.attachment on the TEST base,
// from where descarga_capturas.py pulls it by API and deletes it.
//
// Use ONLY on a test/duplicate base confirmed by Marcos: it writes attachments.
//
// 1) Once per tab, store the helper so it survives full page loads:
//      sessionStorage.setItem('__inj', <contents of this file>)
//    then, after each navigation:
//      await (new Function('return (async()=>{'+sessionStorage.getItem('__inj')+'})()'))()
// 2) Move inside Odoo without reloading, so the helpers stay loaded:
//      await __act({type:'ir.actions.act_window', res_model:'sale.order', res_id:8139, views:[[false,'form']]})
//    OWL paints on requestAnimationFrame: with the pane hidden, take one small
//    screenshot (scale 0.2) after navigating so the frame is actually drawn.
// 3) Capture:  await __cap('01')                      whole page
//              await __cap('01', '.o_form_sheet')     the sheet at its natural height
//              await __cap('06', '.modal-content')    a wizard, without the dimmed page
//    For one2many lists that scroll inside the sheet, first run __full() so the
//    table is drawn complete.
if (!window.htmlToImage) {
  await new Promise((ok, ko) => {
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js';
    s.onload = ok; s.onerror = ko; document.head.appendChild(s);
  });
}
window.__rpc = async (model, method, args, kwargs = {}) => {
  const r = await fetch('/web/dataset/call_kw', {method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({jsonrpc: '2.0', method: 'call', params: {model, method, args, kwargs}})}).then(r => r.json());
  if (r.error) throw new Error(r.error.data ? r.error.data.message : r.error.message);
  return r.result;
};
window.__act = (a) => odoo.__WOWL_DEBUG__.root.env.services.action.doAction(a);
window.__full = () => {
  if (document.getElementById('__mlrst')) return;
  const st = document.createElement('style'); st.id = '__mlrst';
  st.textContent = '.o_form_sheet .o_list_renderer{max-height:none!important;overflow:visible!important}';
  document.head.appendChild(st);
};
window.__cap = async (key, sel) => {
  // the red "neutralized database" banner of test copies does not go in a client deliverable
  [...document.querySelectorAll('.o_web_client > div')]
    .filter(d => /neutralizada|neutralized/i.test(d.innerText || '') && d.innerText.length < 140).forEach(d => d.remove());
  await new Promise(r => setTimeout(r, 600));
  const node = sel ? document.querySelector(sel) : document.body;
  if (!node) throw new Error('No existe ' + sel);
  const url = await htmlToImage.toJpeg(node, {quality: 0.92, pixelRatio: 1.5, backgroundColor: '#ffffff'});
  const b64 = url.split(',')[1];
  const name = 'mlr_cap_' + key + '.jpg';
  const old = await __rpc('ir.attachment', 'search', [[['name', '=', name]]]);
  if (old.length) await __rpc('ir.attachment', 'unlink', [old]);
  // Odoo 19.3+ dropped "datas"; "raw" takes the base64 over JSON-RPC. On older
  // versions use datas: b64 instead.
  const id = await __rpc('ir.attachment', 'create', [{name, raw: b64, mimetype: 'image/jpeg'}]);
  return {key, id, kb: Math.round(b64.length * 0.75 / 1024)};
};
'ok';
