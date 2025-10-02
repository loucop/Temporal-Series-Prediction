import subprocess

# Lista de scripts na ordem do pipeline
scripts = [
    "etl.py",
    "features.py",
    "train.py",
    "plot_results.py"
]

for script in scripts:
    print(f"\n🚀 Rodando {script} ...")
    subprocess.run(["python", script], check=True)
