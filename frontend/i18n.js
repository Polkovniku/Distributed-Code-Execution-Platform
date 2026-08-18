const I18N_STORAGE_KEY = 'ui_language';
const DEFAULT_UI_LANGUAGE = 'en';

const TRANSLATIONS = {
  en: {
    pageTitle: 'Code Runner',
    appHeading: 'Code Runner',
    authHeading: 'Sign in',
    interfaceLanguage: 'Interface language',
    languageLabel: 'Programming language',
    emailPlaceholder: 'Email',
    passwordPlaceholder: 'Password',
    usernamePlaceholder: 'Username (for registration)',
    loginButton: 'Sign in',
    registerButton: 'Register',
    runButton: 'Run',
    resultHeading: 'Result',
    outputLabel: 'OUTPUT',
    codePlaceholderPython: "print('Hello, world')",
    authStatusLogin: 'Signing in...',
    authStatusRegister: 'Registering...',
    authStatusInvalidCredentials: 'Invalid email or password',
    authStatusRegisterFailed: 'Registration failed',
    authStatusRegisterSuccess: 'Success! Now sign in.',
    authStatusError: 'Error: {message}',
    sessionExpired: 'Session expired, please sign in again',
    authRequired: 'Authorization required',
    submitting: 'Submitting...',
    running: 'Running...',
    jobStatus: 'Status: {status}...',
    jobTimedOut: 'Execution timed out',
    outputError: 'Error: {message}',
    uiLanguageEnglish: 'English',
    uiLanguageUkrainian: 'Ukrainian'
  },
  uk: {
    pageTitle: 'Запуск коду',
    appHeading: 'Запуск коду',
    authHeading: 'Вхід',
    interfaceLanguage: 'Мова інтерфейсу',
    languageLabel: 'Мова програмування',
    emailPlaceholder: 'Email',
    passwordPlaceholder: 'Пароль',
    usernamePlaceholder: 'Логін (для реєстрації)',
    loginButton: 'Увійти',
    registerButton: 'Реєстрація',
    runButton: 'Запустити',
    resultHeading: 'Результат',
    outputLabel: 'ВИВІД',
    codePlaceholderPython: "print('Hello, world')",
    authStatusLogin: 'Вхід...',
    authStatusRegister: 'Реєстрація...',
    authStatusInvalidCredentials: 'Невірний email або пароль',
    authStatusRegisterFailed: 'Помилка реєстрації',
    authStatusRegisterSuccess: 'Успішно! Тепер увійдіть.',
    authStatusError: 'Помилка: {message}',
    sessionExpired: 'Сесія закінчилася, авторизуйтесь заново',
    authRequired: 'Потрібна авторизація',
    submitting: 'Надсилання...',
    running: 'Виконується...',
    jobStatus: 'Статус: {status}...',
    jobTimedOut: 'Перевищено час виконання',
    outputError: 'Помилка: {message}',
    uiLanguageEnglish: 'Англійська',
    uiLanguageUkrainian: 'Українська'
  }
};

let currentLanguage = DEFAULT_UI_LANGUAGE;

function getStoredLanguage() {
  const stored = localStorage.getItem(I18N_STORAGE_KEY);
  return TRANSLATIONS[stored] ? stored : DEFAULT_UI_LANGUAGE;
}

function setLanguage(language) {
  currentLanguage = TRANSLATIONS[language] ? language : DEFAULT_UI_LANGUAGE;
  localStorage.setItem(I18N_STORAGE_KEY, currentLanguage);
  document.documentElement.lang = currentLanguage;
  applyTranslations();
}

function getLanguage() {
  return currentLanguage;
}

function t(key, values = {}) {
  const bundle = TRANSLATIONS[currentLanguage] || TRANSLATIONS[DEFAULT_UI_LANGUAGE];
  const fallback = TRANSLATIONS[DEFAULT_UI_LANGUAGE];
  const template = bundle[key] ?? fallback[key] ?? key;

  return template.replace(/\{(\w+)\}/g, (_, name) => {
    return values[name] ?? '';
  });
}

function applyTranslations() {
  const languageSelect = document.getElementById('uiLanguage');

  document.title = t('pageTitle');
  document.getElementById('appHeading').textContent = t('appHeading');
  document.getElementById('authHeading').textContent = t('authHeading');
  document.getElementById('interfaceLanguageLabel').textContent = t('interfaceLanguage');
  document.getElementById('languageLabel').textContent = t('languageLabel');
  document.getElementById('email').placeholder = t('emailPlaceholder');
  document.getElementById('password').placeholder = t('passwordPlaceholder');
  document.getElementById('username').placeholder = t('usernamePlaceholder');
  document.getElementById('code').placeholder = t('codePlaceholderPython');
  document.getElementById('loginBtn').textContent = t('loginButton');
  document.getElementById('registerBtn').textContent = t('registerButton');
  document.getElementById('runBtn').textContent = t('runButton');
  document.getElementById('resultHeading').textContent = t('resultHeading');
  document.getElementById('output').dataset.label = t('outputLabel');

  if (languageSelect) {
    const englishOption = languageSelect.querySelector('option[value="en"]');
    const ukrainianOption = languageSelect.querySelector('option[value="uk"]');

    if (englishOption) englishOption.textContent = t('uiLanguageEnglish');
    if (ukrainianOption) ukrainianOption.textContent = t('uiLanguageUkrainian');
    languageSelect.value = currentLanguage;
  }
}

currentLanguage = getStoredLanguage();

const languageSelect = document.getElementById('uiLanguage');
if (languageSelect) {
  languageSelect.addEventListener('change', (event) => {
    setLanguage(event.target.value);
  });
}
