let activeTask = 'tokenize';

function selectTask(btn) {
  document.querySelectorAll('.task-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  activeTask = btn.dataset.task;
  document.getElementById('resultTaskName').textContent = btn.querySelector('.task-name').textContent;
}

function showLoader() {
  document.getElementById('resultBox').innerHTML = `
    <div class="loader-dots">
      <div class="ld"></div>
      <div class="ld"></div>
      <div class="ld"></div>
    </div>`;
}

function showError(msg) {
  document.getElementById('resultBox').innerHTML = `<div class="error-block">${msg}</div>`;
}

function renderTokenize(data) {
  let html = `<div class="fade-in">`;

  html += `<p class="section-title">Word Tokens (${data.word_count})</p>`;
  html += `<div class="token-wrap">`;
  data.words.forEach(w => {
    html += `<span class="token">${w}</span>`;
  });
  html += `</div>`;

  html += `<p class="section-title" style="margin-top:1.25rem">Sentences (${data.sentence_count})</p>`;
  data.sentences.forEach(s => {
    html += `<span class="token sentence">${s}</span>`;
  });

  html += `<div class="stat-pills" style="margin-top:1rem">
    <span class="stat-pill">Words: <strong>${data.word_count}</strong></span>
    <span class="stat-pill">Sentences: <strong>${data.sentence_count}</strong></span>
  </div>`;

  html += `</div>`;
  document.getElementById('resultBox').innerHTML = html;
}

function renderStopwords(data) {
  let html = `<div class="fade-in">`;

  html += `<p class="section-title">Kept Words (${data.filtered.length})</p>`;
  html += `<div class="token-wrap">`;
  data.filtered.forEach(w => {
    html += `<span class="token kept">${w}</span>`;
  });
  html += `</div>`;

  html += `<p class="section-title" style="margin-top:1.25rem">Removed Stopwords (${data.removed.length})</p>`;
  html += `<div class="token-wrap">`;
  data.removed.forEach(w => {
    html += `<span class="token removed">${w}</span>`;
  });
  html += `</div>`;

  html += `</div>`;
  document.getElementById('resultBox').innerHTML = html;
}

function renderPairs(data, label1, label2) {
  let html = `<div class="fade-in"><table class="pair-table">
    <thead><tr><th>${label1}</th><th>${label2}</th></tr></thead><tbody>`;
  data.pairs.forEach(([orig, changed]) => {
    html += `<tr><td>${orig}</td><td>${changed}</td></tr>`;
  });
  html += `</tbody></table></div>`;
  document.getElementById('resultBox').innerHTML = html;
}

function renderSentiment(data) {
  const emojis = { Positive: '😊', Negative: '😞', Neutral: '😐' };
  const polPct = Math.round(((data.polarity + 1) / 2) * 100);
  const subPct = Math.round(data.subjectivity * 100);

  let html = `<div class="fade-in">
    <div class="sentiment-block">
      <div class="sentiment-emoji">${emojis[data.label]}</div>
      <div class="sentiment-label ${data.label}">${data.label}</div>
      <div class="meter-row">
        <div>
          <div class="meter-label"><span>Polarity</span><span>${data.polarity}</span></div>
          <div class="meter-track"><div class="meter-fill polarity" style="width:${polPct}%"></div></div>
        </div>
        <div>
          <div class="meter-label"><span>Subjectivity</span><span>${data.subjectivity}</span></div>
          <div class="meter-track"><div class="meter-fill subjectivity" style="width:${subPct}%"></div></div>
        </div>
      </div>
    </div>
  </div>`;
  document.getElementById('resultBox').innerHTML = html;
}

async function runTask() {
  const text = document.getElementById('textInput').value.trim();
  if (!text) {
    showError('Please enter some text first.');
    return;
  }

  const btn = document.querySelector('.run-btn');
  btn.disabled = true;
  btn.textContent = 'Analyzing...';
  showLoader();

  try {
    const res = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, task: activeTask })
    });

    const data = await res.json();

    if (data.error) {
      showError(data.error);
    } else if (activeTask === 'tokenize') {
      renderTokenize(data);
    } else if (activeTask === 'stopwords') {
      renderStopwords(data);
    } else if (activeTask === 'stemming') {
      renderPairs(data, 'Original', 'Stemmed');
    } else if (activeTask === 'lemmatization') {
      renderPairs(data, 'Original', 'Lemmatized');
    } else if (activeTask === 'sentiment') {
      renderSentiment(data);
    }
  } catch (e) {
    showError('Something went wrong. Make sure the server is running.');
  }

  btn.disabled = false;
  btn.textContent = 'Run Analysis →';
}
