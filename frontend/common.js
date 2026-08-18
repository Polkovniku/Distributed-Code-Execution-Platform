function getToken() {
  return localStorage.getItem('token');
}

function getRefreshToken() {
  return localStorage.getItem('refresh_token');
}

function saveTokens(access, refresh) {
  localStorage.setItem('token', access);
  if (refresh) localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
  localStorage.removeItem('token');
  localStorage.removeItem('refresh_token');
}

function showApp() {
  document.getElementById('authBlock').style.display = 'none';
  document.getElementById('appBlock').style.display = 'block';
}

function showLogin() {
  document.getElementById('authBlock').style.display = 'block';
  document.getElementById('appBlock').style.display = 'none';
}

async function refreshAccessToken() {
  const refresh = getRefreshToken();
  if (!refresh) return false;

  try {
    const res = await fetch('/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refresh })
    });

    if (!res.ok) return false;

    const data = await res.json();
    saveTokens(data.access_token, data.refresh_token);
    return true;
  } catch {
    return false;
  }
}

async function authFetch(url, options = {}) {
  const token = getToken();
  options.headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`
  };

  let res = await fetch(url, options);

  if (res.status === 401) {
    const refreshed = await refreshAccessToken();
    if (!refreshed) {
      clearTokens();
      showLogin();
      throw new Error(t('sessionExpired'));
    }

    options.headers['Authorization'] = `Bearer ${getToken()}`;
    res = await fetch(url, options);
  }

  return res;
}

setLanguage(getStoredLanguage());

if (getToken()) showApp();
