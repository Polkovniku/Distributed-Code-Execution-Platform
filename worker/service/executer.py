import docker
import base64


class CodeExecuter:
    LANGUAGE_IMAGE = {
        "python": "python:3.12-slim"
    }
    
    def __init__(self, timeout_second: int = 10, mem_limit: str = "128m", cpu_quota: int = 50000):
        self.client = docker.from_env()
        self.timeout_second = timeout_second
        self.mem_limit = mem_limit
        self.cpu_quota = cpu_quota


    def run(self, language: str, code: str) -> dict:
        image = self.LANGUAGE_IMAGE.get(language)
        if image is None:
            return {"stdout": "", "stderr": f"Unsupported language: {language}", "exit_code": None, "status": "FAILED"}

        encoded_code = base64.b64encode(code.encode()).decode()
        command = ["sh", "-c", f"echo {encoded_code} | base64 -d > /tmp/main.py && python /tmp/main.py"]

        container = self.client.containers.run(
            image=image,
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