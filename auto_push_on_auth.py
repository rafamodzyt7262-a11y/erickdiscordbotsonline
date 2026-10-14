import subprocess
import time
import sys

print("Monitoreando autorización de GitHub para ejecutar git push automáticamente...")
while True:
    res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    output = res.stdout + res.stderr
    if "Logged in to github.com" in output:
        print("✅ ¡Autorizado con éxito! Subiendo proyecto con git push...")
        push_res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
        print("Resultado git push:\n", push_res.stdout, push_res.stderr)
        break
    time.sleep(2)
