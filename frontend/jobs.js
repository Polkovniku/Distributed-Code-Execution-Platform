const codeInput = document.getElementById('code');
const languageInput = document.getElementById('language');
const output = document.getElementById('output');

document.getElementById('runBtn').addEventListener('click', async () => {
  const token = getToken();
  if (!token) {
    output.textContent = 'Нужна авторизация';
    return;
  }

  output.textContent = 'Отправка...';

  try {
    const res = await fetch('/jobs/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        code: codeInput.value,
        language: languageInput.value
      })
    });

    if (res.status === 401) {
      output.textContent = 'Токен истёк, авторизуйтесь заново';
      return;
    }

    const job = await res.json();
    pollJob(job.job_id, token);
  } catch (err) {
    output.textContent = 'Ошибка: ' + err.message;
  }
});

async function pollJob(jobId, token) {
  output.textContent = 'Выполняется...';
  const interval = setInterval(async () => {
    const res = await fetch(`/jobs/${jobId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const job = await res.json();

    if (job.status === 'PENDING' || job.status === 'RUNNING') {
      output.textContent = `Статус: ${job.status}...`;
      return;
    }

    clearInterval(interval);

    if (job.status === 'TIMEOUT') {
      output.textContent = 'Превышено время выполнения';
      return;
    }

    output.textContent =
      `stdout: ${job.stdout ?? ''}\n` +
      `stderr: ${job.stderr ?? ''}\n` +
      `exit_code: ${job.exit_code ?? '-'}`;
  }, 1000);
}