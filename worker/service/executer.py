import docker
import base64


class CodeExecuter:
    LANGUAGE_CONFIG = {
        "python": {
            "image": "python:3.12-slim",
            "filename": "main.py",
            "run_cmd": "python /tmp/{filename}"
        },
        "javascript": {
            "image": "node:20-alpine",
            "filename": "main.js",
            "run_cmd": "node /tmp/{filename}"
        },
        "c++": {
            "image": "gcc:13",
            "filename": "main.cpp",
            "run_cmd": "g++ /tmp/{filename} -o /tmp/main && /tmp/main"
        },
        "go": {
            "image": "golang:1.22-alpine",
            "filename": "main.go",
            "run_cmd": "go run /tmp/{filename}"
        },
        "java": {
            "image": "eclipse-temurin:21-jdk",
            "filename": "Main.java",
            "run_cmd": "cd /tmp && javac {filename} && java Main"
        },
        "rust": {
            "image": "rust:1.77-slim",
            "filename": "main.rs",
            "run_cmd": "rustc /tmp/{filename} -o /tmp/main && /tmp/main"
        }
    }
    
    def __init__(self, timeout_second: int = 60, mem_limit: str = "128m", cpu_quota: int = 50000):
        self.client = docker.from_env()
        self.timeout_second = timeout_second
        self.mem_limit = mem_limit
        self.cpu_quota = cpu_quota


    def run(self, language: str, code: str) -> dict:
        config = self.LANGUAGE_CONFIG.get(language)
        if config is None:
            return {"stdout": "", "stderr": f"Unsupported language: {language}", "exit_code": None, "status": "FAILED"}

        encoded_code = base64.b64encode(code.encode()).decode()
        run_cmd = config["run_cmd"].format(filename=config["filename"])
        command = ["sh", "-c", f"echo {encoded_code} | base64 -d > /tmp/{config['filename']} && {run_cmd}"]

        container = self.client.containers.run(
            image=config["image"],
            command=command,
            mem_limit=self.mem_limit,
            cpu_quota=self.cpu_quota,
            network_disabled=True,
            detach=True,
        )

        try:
            result = container.wait(timeout=self.timeout_second)
            exit_code = result["StatusCode"]
            stdout = container.logs(stdout=True, stderr=False).decode()
            stderr = container.logs(stdout=False, stderr=True).decode()
            status = "FINISHED" if exit_code == 0 else "FAILED"
        except Exception:
            container.kill()
            stdout, stderr, exit_code = "", "", None
            status = "TIMEOUT"
        finally:
            container.remove(force=True)

        return {"stdout": stdout, "stderr": stderr, "exit_code": exit_code, "status": status}