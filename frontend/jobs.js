function combinedHint(cm) {
  const cursor = cm.getCursor();
  const line = cm.getLine(cursor.line);

  let start = cursor.ch;
  let end = cursor.ch;
  while (start && /[\w]/.test(line.charAt(start - 1))) start--;
  while (end < line.length && /[\w]/.test(line.charAt(end))) end++;

  const word = line.slice(start, end).toLowerCase();
  if (!word) return null;

  const lang = languageInput.value;
  const dictWords = KEYWORDS[lang] || [];
  const dictMatches = dictWords.filter(w => w.toLowerCase().startsWith(word));

  const anywordResult = CodeMirror.hint.anyword(cm, { word: /[\w$]+/ });
  const anywordMatches = anywordResult ? anywordResult.list : [];

  const merged = [...new Set([...dictMatches, ...anywordMatches])];
  if (!merged.length) return null;

  return {
    list: merged,
    from: CodeMirror.Pos(cursor.line, start),
    to: CodeMirror.Pos(cursor.line, end)
  };
}

const editor = CodeMirror.fromTextArea(document.getElementById('code'), {
  mode: 'python',
  theme: 'dracula',
  lineNumbers: true,
  indentUnit: 4,
  matchBrackets: true,
  autoCloseBrackets: true,
  tabSize: 4,
  extraKeys: { "Ctrl-Space": "autocomplete" }
});


const languageInput = document.getElementById('language');
const output = document.getElementById('output');

const DEFAULT_SNIPPETS = {
  python: "print('Hello, world')",
  javascript: "console.log('Hello, world')",
  'c++': '#include <iostream>\n\nint main() {\n    std::cout << "Hello, world" << std::endl;\n    return 0;\n}',
  go: 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, world")\n}',
  java: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, world");\n    }\n}',
  rust: 'fn main() {\n    println!("Hello, world");\n}'
};

editor.setValue(DEFAULT_SNIPPETS.python); 


const MODES = {
  python: 'python',
  javascript: 'javascript',
  'c++': 'text/x-c++src',
  go: 'go',
  java: 'text/x-java',
  rust: 'rust'
};

languageInput.addEventListener('change', () => {
  const lang = languageInput.value;
  const currentValue = editor.getValue();
  const isDefaultOrEmpty = !currentValue.trim() || 
    Object.values(DEFAULT_SNIPPETS).includes(currentValue);

  editor.setOption('mode', MODES[lang] || 'python');
  if (isDefaultOrEmpty) {
    editor.setValue(DEFAULT_SNIPPETS[lang] || '');
  }
});


editor.on("inputRead", function (cm, change) {
  if (change.text[0] && /[a-zA-Z_]/.test(change.text[0])) {
    cm.showHint({ hint: combinedHint, completeSingle: false });
  }
});

document.getElementById('runBtn').addEventListener('click', async () => {
  if (!getToken()) {
    output.textContent = 'Потрібна авторизація';
    return;
  }

  output.textContent = 'Надсилання...';

  try {
    const res = await authFetch('/jobs/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: editor.getValue(),
        language: languageInput.value
      })
    });

    const job = await res.json();
    pollJob(job.job_id);
  } catch (err) {
    output.textContent = 'Помилка: ' + err.message;
  }
});

async function pollJob(jobId) {
  output.textContent = 'Виконується...';
  const interval = setInterval(async () => {
    try {
      const res = await authFetch(`/jobs/${jobId}`);
      const job = await res.json();

      if (job.status === 'PENDING' || job.status === 'RUNNING') {
        output.textContent = `Статус: ${job.status}...`;
        return;
      }

      clearInterval(interval);

      if (job.status === 'TIMEOUT') {
        output.textContent = 'Перевищено час виконання';
        return;
      }

      output.textContent =
        `stdout: ${job.stdout ?? ''}\n` +
        `stderr: ${job.stderr ?? ''}\n` +
        `exit_code: ${job.exit_code ?? '-'}`;
    } catch (err) {
      clearInterval(interval);
      output.textContent = err.message;
    }
  }, 1000);
}