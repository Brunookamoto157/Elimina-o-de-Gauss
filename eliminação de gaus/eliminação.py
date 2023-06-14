import numpy as np

def gauss_elimination(coefficients, constants):
    augmented_matrix = np.column_stack((coefficients, constants))
    num_equations, num_variables = augmented_matrix.shape

    L = np.eye(num_equations)  # Matriz de permutação
    U = np.zeros((num_equations, num_variables))  # Matriz U
    P = np.eye(num_equations)  # Matriz de permutação

    for i in range(num_equations):
        pivot = augmented_matrix[i, i]

        # Troca de linhas para pivôs não nulos
        if pivot == 0:
            non_zero_row = np.where(augmented_matrix[i+1:, i] != 0)[0]
            if len(non_zero_row) > 0:
                non_zero_row = non_zero_row[0] + i + 1
                augmented_matrix[[i, non_zero_row]] = augmented_matrix[[non_zero_row, i]]
                P[[i, non_zero_row]] = P[[non_zero_row, i]]
            else:
                raise ValueError("O sistema não tem solução única.")

        L[i+1:, i] = augmented_matrix[i+1:, i] / pivot
        U[i, i:] = augmented_matrix[i, i:]
        U[i+1:, i+1:] = augmented_matrix[i+1:, i+1:] - np.outer(L[i+1:, i], U[i, i+1:])

    solution = back_substitution(augmented_matrix)
    return L, U, P, solution

def back_substitution(matrix):
    num_equations, num_variables = matrix.shape
    solution = np.zeros(num_equations)

    for i in range(num_equations - 1, -1, -1):
        solution[i] = matrix[i, -1]
        for j in range(i + 1, num_variables - 1):
            solution[i] -= matrix[i, j] * solution[j]
        solution[i] /= matrix[i, i]

    return solution

def gauss_seidel(coefficients, constants, initial_guess, max_iterations, tolerance):
    num_equations = len(coefficients)
    num_variables = len(coefficients[0])
    x = initial_guess.copy()
    converged = False
    iterations = 0

    while not converged and iterations < max_iterations:
        x_new = x.copy()
        for i in range(num_equations):
            sum_ = 0
            for j in range(num_variables):
                if j != i:
                    sum_ += coefficients[i][j] * x_new[j]
            x_new[i] = (constants[i] - sum_) / coefficients[i][i]

        if np.linalg.norm(x_new - x) < tolerance:
            converged = True

        x = x_new
        iterations += 1

    return x

# Exemplo de uso
num_equations = int(input("Digite o número de equações: "))
num_variables = int(input("Digite o número de variáveis: "))

coefficients = []
constants = []

print("Digite os coeficientes das equações:")
for _ in range(num_equations):
    equation = []
    for _ in range(num_variables):
        coefficient = float(input("Coeficiente: "))
        equation.append(coefficient)
    coefficients.append(equation)

print("Digite os termos independentes:")
for _ in range(num_equations):
    constant = float(input("Termo independente: "))
    constants.append(constant)

method = int(input("Escolha o método (1 - Gauss, 2 - Eliminação de Gauss, 3 - Gauss-Seidel): "))

if method == 1:
    solution = gauss_elimination(coefficients, constants)
    print("Solução usando o método de Gauss:", solution)
elif method == 2:
    L, U, P, solution = gauss_elimination(coefficients, constants)
    print("Matriz L:")
    print(L)
    print("Matriz U:")
    print(U)
    print("Matriz de Permutação:")
    print(P)
    print("Solução usando o método de Eliminação de Gauss:")
    print(solution)
elif method == 3:
    max_iterations = int(input("Digite o número máximo de iterações: "))
    tolerance = float(input("Digite a tolerância: "))
    initial_guess = np.zeros(num_variables)
    solution = gauss_seidel(coefficients, constants, initial_guess, max_iterations, tolerance)
    print("Solução usando o método de Gauss-Seidel:", solution)
else:
    print("Opção inválida. Por favor, escolha um método válido.")
