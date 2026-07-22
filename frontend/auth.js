const authStatus = document.getElementById('authStatus');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const usernameInput = document.getElementById('username');

document.getElementById('loginBtn').addEventListener('click', async () => {
  authStatus.textContent = 'Вход...';
  try {
    const res = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: emailInput.value,
        password: passwordInput.value
      })
    });

    if (!res.ok) {
      authStatus.textContent = 'Неверный email/пароль';
      return;
    }

    const data = await res.json();
    saveTokens(data.access_token, data.refresh_token);
    showApp();
  } catch (err) {
    authStatus.textContent = 'Ошибка: ' + err.message;
  }
});

document.getElementById('registerBtn').addEventListener('click', async () => {
  authStatus.textContent = 'Регистрация...';
  try {
    const res = await fetch('/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: emailInput.value,
        password: passwordInput.value,
        username: usernameInput.value
      })
    });

    if (!res.ok) {
      authStatus.textContent = 'Ошибка регистрации';
      return;
    }

    authStatus.textContent = 'Успешно! Теперь войдите.';
  } catch (err) {
    authStatus.textContent = 'Ошибка: ' + err.message;
  }
});