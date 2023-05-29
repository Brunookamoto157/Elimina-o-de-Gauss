import numpy as np
import tkinter as tk
from tkinter import messagebox

def gauss_elimination(coefficients, constants):
    augmented_matrix = np.column_stack((coefficients, constants))
    num_equations, num_variables = augmented_matrix.shape

    for i in range(num_equations):
        pivot = augmented_matrix[i, i]

        for j in range(i + 1, num_equations):
            factor = augmented_matrix[j, i] / pivot
            augmented_matrix[j, :] -= factor * augmented_matrix[i, :]

    solution = back_substitution(augmented_matrix)
    return solution

def back_substitution(matrix):
    num_equations, num_variables = matrix.shape
    solution = np.zeros(num_equations)

    for i in range(num_equations - 1, -1, -1):
        solution[i] = matrix[i, -1]
        for j in range(i + 1, num_variables - 1):
            solution[i] -= matrix[i, j] * solution[j]
        solution[i] /= matrix[i, i]

    return solution

def solve_equations():
    coefficients = []
    constants = []

    try:
        num_equations = int(num_equations_entry.get())
        num_variables = int(num_variables_entry.get())

        for i in range(num_equations):
            equation = []
            for j in range(num_variables):
                coefficient = float(coefficients_entries[i][j].get())
                equation.append(coefficient)
            coefficients.append(equation)

        for i in range(num_equations):
            constant = float(constants_entries[i].get())
            constants.append(constant)

        solution = gauss_elimination(coefficients, constants)

        messagebox.showinfo("Resultado", f"A solução do sistema é: {solution}")
    except ValueError:
        messagebox.showerror("Erro", "Certifique-se de inserir apenas números válidos.")

root = tk.Tk()
root.title("Eliminação de Gauss")

# Número de equações
num_equations_label = tk.Label(root, text="Número de Equações:")
num_equations_label.grid(row=0, column=0, sticky="E")
num_equations_entry = tk.Entry(root)
num_equations_entry.grid(row=0, column=1)

# Número de variáveis
num_variables_label = tk.Label(root, text="Número de Variáveis:")
num_variables_label.grid(row=1, column=0, sticky="E")
num_variables_entry = tk.Entry(root)
num_variables_entry.grid(row=1, column=1)

coefficients_entries = []
constants_entries = []

# Entradas para os coeficientes
coefficients_label = tk.Label(root, text="Coeficientes:")
coefficients_label.grid(row=2, column=0, sticky="E")

for i in range(10):  # Definindo um limite máximo de 10 equações
    if i == 0:
        label_text = "Equação 1:"
    else:
        label_text = ""
    label = tk.Label(root, text=label_text)
    label.grid(row=i+3, column=0, sticky="E")

    entries = []
    for j in range(10):  # Definindo um limite máximo de 10 variáveis
        entry = tk.Entry(root)
        entry.grid(row=i+3, column=j+1)
        entries.append(entry)
    coefficients_entries.append(entries)

# Entradas para os termos independentes
constants_label = tk.Label(root, text="Termos Independ")
