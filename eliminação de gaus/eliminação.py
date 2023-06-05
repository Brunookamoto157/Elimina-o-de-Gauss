from numpy import column_stack, zeros

def gauss_elimination(coefficients, constants):
    augmented_matrix = column_stack((coefficients, constants))
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
    solution = zeros(num_equations)

    for i in range(num_equations - 1, -1, -1):
        solution[i] = matrix[i, -1]
        for j in range(i + 1, num_variables - 1):
            solution[i] -= matrix[i, j] * solution[j]
        solution[i] /= matrix[i, i]

    return solution

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

solution = gauss_elimination(coefficients, constants)
print("A solução do sistema é:", solution)
