function getToken() {
  return localStorage.getItem('token');
}

function showApp() {
  document.getElementById('authBlock').style.display = 'none';
  document.getElementById('appBlock').style.display = 'block';
}

if (getToken()) showApp();