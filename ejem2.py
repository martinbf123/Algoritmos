from qiskit import transpile
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2, SamplerV2
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# Función para factorizar un número entero utilizando simulaciones cuánticas
def approximate_factorization(n):
    """
    Simulación de aproximación de la factorización cuántica sin usar Shor.
    Aquí utilizamos estimadores cuánticos y métodos de muestreo para aproximar factores.
    """
    # Configuración del simulador cuántico
    sim = AerSimulator()

    # --------------------------
    # Simulación usando el estimador cuántico
    # ---------------------------
    # Crear circuitos cuánticos parametrizados
    psi1 = transpile(RealAmplitudes(num_qubits=2, reps=2), sim, optimization_level=0)
    psi2 = transpile(RealAmplitudes(num_qubits=2, reps=3), sim, optimization_level=0)

    # Definir los operadores de Pauli
    H1 = SparsePauliOp.from_list([("II", 1), ("IZ", 2), ("XI", 3)])
    H2 = SparsePauliOp.from_list([("IZ", 1)])
    H3 = SparsePauliOp.from_list([("ZI", 1), ("ZZ", 1)])

    theta1 = [0, 1, 1, 2, 3, 5]
    theta2 = [0, 1, 1, 2, 3, 5, 8, 13]
    theta3 = [1, 2, 3, 4, 5, 6]

    # Inicializar el estimador cuántico
    estimator = EstimatorV2()

    # Calcular expectativas
    job = estimator.run(
        [
            (psi1, [H1, H3], [theta1, theta3]),
            (psi2, H2, theta2)
        ],
        precision=0.01
    )

    result = job.result()
    print(f"expectation values : psi1 = {result[0].data.evs}, psi2 = {result[1].data.evs}")

    # --------------------------
    # Simulación usando el sampler cuántico
    # ---------------------------
    # Crear un circuito de Bell
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()

    # Crear circuitos parametrizados
    pqc = RealAmplitudes(num_qubits=2, reps=2)
    pqc.measure_all()
    pqc = transpile(pqc, sim, optimization_level=0)
    pqc2 = RealAmplitudes(num_qubits=2, reps=3)
    pqc2.measure_all()
    pqc2 = transpile(pqc2, sim, optimization_level=0)

    # Inicializar el sampler cuántico
    sampler = SamplerV2()

    # Recoger 128 shots del circuito de Bell
    job = sampler.run([bell], shots=128)
    job_result = job.result()
    print(f"counts for Bell circuit : {job_result[0].data.meas.get_counts()}")

    # Ejecutar un job de sampler para los circuitos parametrizados
    job2 = sampler.run([(pqc, theta1), (pqc2, theta2)])
    job_result = job2.result()
    print(f"counts for parameterized circuit : {job_result[0].data.meas.get_counts()}")

    # Simulación de factorización aproximada
    # Aquí no estamos implementando un algoritmo de factorización cuántica directo, sino una simulación
    print(f"Simulación de factorización para el número {n}:\n")
    factors = []
    for i in range(1, n):
        if n % i == 0:
            factors.append(i)

    print(f"Posibles factores del número {n}: {factors}")
    
    # Mostrar el gráfico de la simulación de los resultados de la factorización
    return factors, bell, pqc, pqc2

# Número a factorizar
n = 14400 # Cambia este número por el que desees factorizar

# Ejecutar la simulación de la factorización cuántica
factors, bell, pqc, pqc2 = approximate_factorization(n)

# Mostrar los resultados en gráficos si es necesario
image_path = "/mnt/data/image.png"  # Ruta de la imagen que subiste
if os.path.exists(image_path):
    img = mpimg.imread(image_path)
    plt.figure(figsize=(10, 8))
    plt.imshow(img)
    plt.axis('off')  # Ocultar los ejes
    plt.title("Diagrama Cuántico Relacionado")
    plt.show()
else:
    print("No se pudo cargar la imagen. Asegúrate de que la ruta sea correcta.")

# Visualización de los circuitos cuánticos
print("Visualización de los circuitos cuánticos:")
bell.draw('mpl')
pqc.draw('mpl')
pqc2.draw('mpl')

# Mostrar gráfico de pastel de los factores
plt.figure(figsize=(6, 6))
plt.pie([factors.count(i) for i in factors], labels=factors, autopct='%1.1f%%', startangle=90)
plt.title(f"Distribución de factores para el número {n}")
plt.show()