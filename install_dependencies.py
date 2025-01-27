import sys
import subprocess

# Verificar la versión de Python
required_version = (3, 8, 10)
current_version = sys.version_info

if current_version < required_version:
    print(f"Se requiere Python {required_version[0]}.{required_version[1]}.{required_version[2]} o superior.")
    print(f"La versión actual es {current_version[0]}.{current_version[1]}.{current_version[2]}.")
    sys.exit("La versión de Python no es la correcta. Por favor, actualiza Python a la versión requerida.")

print("Versión de Python correcta. Procediendo con la instalación de las dependencias...")

# Lista de paquetes necesarios
required_packages = [
    'qiskit',
    'matplotlib',
    'qiskit-aer',
    'qiskit-ibm-runtime',
    'pylatexenc'
]

# Instalar los paquetes necesarios
for package in required_packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("Instalación de paquetes completada.")
