const authStatus = document.getElementById('authStatus');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const usernameInput = document.getElementById('username');

document.getElementById('loginBtn').addEventListener('click', async () => {
  authStatus.textContent = t('authStatusLogin');
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
      authStatus.textContent = t('authStatusInvalidCredentials');
      return;
    }

    const data = await res.json();
    saveTokens(data.access_token, data.refresh_token);
    showApp();
  } catch (err) {
    authStatus.textContent = t('authStatusError', { message: err.message });
  }
});

document.getElementById('registerBtn').addEventListener('click', async () => {
  authStatus.textContent = t('authStatusRegister');
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
      authStatus.textContent = t('authStatusRegisterFailed');
      return;
    }

    authStatus.textContent = t('authStatusRegisterSuccess');
  } catch (err) {
    authStatus.textContent = t('authStatusError', { message: err.message });
  }
});
