import subprocess


def run_scripts():
    try:
        # Ejecutar metrics.py
        subprocess.run(["python", "metrics.py"], check=True)
        # Ejecutar results.py
        subprocess.run(["python", "results.py"], check=True)
        # Ejecutar plots.py
        subprocess.run(["python", "plots.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar un script: {e}")

if __name__ == "__main__":
    run_scripts()