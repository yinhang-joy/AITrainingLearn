(() => {
  'use strict';
  const API = location.port === '8765' && location.protocol === 'http:' ? location.origin : 'http://localhost:8765';
  const $ = id => document.getElementById(id);
  const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const dateLabel = value => new Intl.DateTimeFormat('zh-CN', {timeZone:'Asia/Shanghai', month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(value));
  let paper = null, latestId = null, history = [], busy = false, resetUnit = null;
  const url = path => API + path;

  function status(message = '', error = false) {
    $('status').textContent = message;
    $('status').classList.toggle('error', error);
  }
  function setBusy(value) {
    busy = value;
    document.querySelectorAll('button:not(#retry):not(#cancel-reset), #history').forEach(el => { el.disabled = value || !paper; });
    $('questions').setAttribute('aria-busy', String(value));
  }
  async function api(path, body) {
    const response = await fetch(url(path), {
      method:body === undefined ? 'GET' : 'POST',
      ...(body === undefined ? {} : {headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}),
      cache:'no-store'
    });
    let result;
    try { result = await response.json(); }
    catch { throw new Error('服务响应异常，请重新启动本项目的考试服务。'); }
    if (!response.ok) throw new Error(result.error || '操作失败，请刷新后重试。');
    return result;
  }
  function fileLink(file, label) {
    return `<a href="${esc(url(file.url))}" target="_blank" rel="noopener">${esc(label || file.name)}</a>`;
  }
  function render() {
    $('total-count').textContent = paper.questions.length;
    $('total-minutes').textContent = paper.minutes;
    $('total-points').textContent = paper.points;
    const index = history.findIndex(item => item.id === paper.id);
    const ordinal = index < 0 ? history.length : history.length - index;
    $('paper-heading').textContent = `第 ${ordinal} 套试题${paper.id === latestId ? ' · 当前试卷' : ' · 历史试卷'}`;
    $('paper-date').textContent = `${dateLabel(paper.created_at)} 生成 · 作答版本 ${paper.version}`;
    $('history').innerHTML = history.map((item, i) => `<option value="${esc(item.id)}" ${item.id === paper.id ? 'selected' : ''}>第 ${history.length-i} 套 · ${esc(dateLabel(item.created_at))}${item.id === latestId ? '（当前）' : ''}</option>`).join('');
    $('questions').innerHTML = paper.questions.map((q, i) => {
      const task = q.files.find(f => f.name === `${q.unit}.html`);
      const docs = q.files.filter(f => f.suffix === '.docx');
      const data = q.files.filter(f => !['.html','.ipynb','.docx'].includes(f.suffix));
      const links = (task ? fileLink(task, '任务要求') : '') + docs.map(f => fileLink(f,'答题卷')).join('');
      return `<article class="question ${q.has_code ? '' : 'essay'}" data-unit="${esc(q.unit)}">
        <div class="question-top"><span class="unit">${esc(q.unit)}</span><span class="type">${q.has_code ? '代码练习' : '分析 / 文档题'}</span></div>
        <div class="category">第 ${i+1} 题 · ${esc(q.group_name)}</div>
        <h3>${esc(q.title)}</h3>
        <div class="timing"><span><strong>${q.minutes}</strong> 分钟</span><span><strong>${q.points}</strong> 分</span></div>
        <div class="links">${links}</div>
        <div class="question-actions"><a class="button primary" href="${esc(url(q.jupyter_url))}" target="_blank" rel="noopener">${q.has_code ? '在 Jupyter 作答 ↗' : '在 Jupyter 查看 ↗'}</a><button type="button" class="reset-one" data-reset="${esc(q.unit)}">重置本题</button></div>
        <details class="assets"><summary>素材与作答文件</summary><div class="asset-links">${data.map(f => fileLink(f)).join('')}<a href="${esc(url(q.folder_url))}" target="_blank" rel="noopener">打开本题目录 ↗</a></div></details>
      </article>`;
    }).join('');
    $('paper-folder').href = url(paper.folder_url);
    $('paper-folder').hidden = false;
    $('backups').hidden = !paper.resets.length;
    $('backup-list').innerHTML = paper.resets.slice().reverse().map(event => `<div class="backup-entry">${esc(dateLabel(event.at))}${event.previous.map(q => `<a href="${esc(url('/'+q.folder.split('/').map(encodeURIComponent).join('/')+'/'))}" target="_blank" rel="noopener">${esc(q.unit)} 旧作答 ↗</a>`).join('')}</div>`).join('');
  }
  async function load(id) {
    setBusy(true);
    $('retry').hidden = true;
    try {
      const current = await api('/api/exam/current');
      latestId = current.id;
      history = await api('/api/exam/history');
      paper = id && id !== current.id ? await api('/api/exam/paper?id='+encodeURIComponent(id)) : current;
      render();
      status();
    } catch (error) {
      status(error instanceof TypeError ? '无法连接考试服务，请启动服务后点击“重新连接”。' : error.message, true);
      $('retry').hidden = false;
    } finally { setBusy(false); }
  }
  $('draw').addEventListener('click', async () => {
    if (busy) return;
    setBusy(true); status('正在抽题并准备独立作答文件…');
    try {
      paper = await api('/api/exam/draw', {current_id:latestId});
      latestId = paper.id;
      history = await api('/api/exam/history');
      render(); status('新试卷已生成，上一套作答已保留在历史试卷中。');
      window.history.replaceState(null,'',location.pathname);
    } catch (error) { status(error.message, true); }
    finally { setBusy(false); }
  });
  function askReset(unit = null) {
    if (busy || !paper) return;
    resetUnit = unit;
    $('reset-title').textContent = unit ? `重置 ${unit}？` : '重置本套 6 道试题？';
    $('reset-dialog').showModal();
  }
  $('reset-all').addEventListener('click', () => askReset());
  $('questions').addEventListener('click', event => {
    const button = event.target.closest('button[data-reset]');
    if (button) askReset(button.dataset.reset);
  });
  $('cancel-reset').addEventListener('click', () => $('reset-dialog').close());
  $('confirm-reset').addEventListener('click', async () => {
    $('reset-dialog').close();
    setBusy(true); status('正在保留旧作答并生成空白副本…');
    try {
      paper = await api('/api/exam/reset', {id:paper.id,version:paper.version,unit:resetUnit});
      render(); status('重置完成。请使用本页的新入口打开题目；旧作答已保留在页面下方。');
    } catch (error) { status(error.message, true); }
    finally { setBusy(false); }
  });
  $('history').addEventListener('change', async event => {
    const id = event.target.value;
    await load(id);
    if (paper && paper.id === id) window.history.replaceState(null,'',location.pathname+'?paper='+encodeURIComponent(id));
  });
  $('retry').addEventListener('click', () => load(new URLSearchParams(location.search).get('paper')));
  $('practice-link').href = url('/'+encodeURIComponent('练习导航.html'));
  load(new URLSearchParams(location.search).get('paper'));
})();
