<template>
  <div>
    <h2>Método de Solução de Equações Lineares</h2>
    <label>Número de equações:</label>
    <input type="number" v-model="numEquations">
    <br>
    <label>Número de variáveis:</label>
    <input type="number" v-model="numVariables">
    <br>
    <h3>Coeficientes das equações:</h3>
    <div v-for="(equation, index) in coefficients" :key="index">
      <div v-for="(coefficient, j) in equation" :key="j">
        <label>Coeficiente:</label>
        <input type="number" v-model="coefficients[index][j]">
      </div>
    </div>
    <h3>Termos independentes:</h3>
    <div v-for="(constant, index) in constants" :key="index">
      <label>Termo independente:</label>
      <input type="number" v-model="constants[index]">
    </div>
    <label>Método:</label>
    <select v-model="selectedMethod">
      <option value="1">Gauss</option>
      <option value="2">Eliminação de Gauss</option>
      <option value="3">Gauss-Seidel</option>
    </select>
    <div v-if="selectedMethod === '3'">
      <label>Número máximo de iterações:</label>
      <input type="number" v-model="maxIterations">
      <br>
      <label>Tolerância:</label>
      <input type="number" step="0.0001" v-model="tolerance">
    </div>
    <button @click="solveEquations">Solução</button>
    <div v-if="solution">
      <h3>Solução:</h3>
      <p>{{ solution }}</p>
    </div>
    <div v-if="errorMessage">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import * as np from 'numpy'; // Import numpy (assumes you have numpy installed in your project)

export default {
  data() {
    return {
      numEquations: 0,
      numVariables: 0,
      coefficients: [],
      constants: [],
      selectedMethod: '1',
      maxIterations: 0,
      tolerance: 0,
      solution: null,
      errorMessage: ''
    };
  },
  methods: {
    solveEquations() {
      this.solution = null;
      this.errorMessage = '';

      const coefficients = this.coefficients.map(equation => [...equation]);
      const constants = [...this.constants];

      try {
        if (this.selectedMethod === '1') {
          this.solution = this.gaussElimination(coefficients, constants);
        } else if (this.selectedMethod === '2') {
          this.solution = this.gaussElimination(coefficients, constants);
        } else if (this.selectedMethod === '3') {
          const initialGuess = np.zeros(this.numVariables);
          this.solution = this.gaussSeidel(coefficients, constants, initialGuess, this.maxIterations, this.tolerance);
        } else {
          throw new Error('Opção inválida. Por favor, escolha um método válido.');
        }
      } catch (error) {
        this.errorMessage = 'Erro ao calcular a solução. Verifique os dados de entrada.';
      }
    },
    gaussElimination(coefficients, constants) {
      const augmentedMatrix = np.column_stack([coefficients, constants]);
      const [numEquations, numVariables] = augmentedMatrix.shape;

      for (let i = 0; i < numEquations; i++) {
        const pivot = augmentedMatrix[i][i];

        for (let j = i + 1; j < numEquations; j++) {
          const factor = augmentedMatrix[j][i] / pivot;
          augmentedMatrix[j] -= factor * augmentedMatrix[i];
        }
      }

      const solution = this.backSubstitution(augmentedMatrix);
      return solution;
    },
    backSubstitution(matrix) {
      const [numEquations, numVariables] = matrix.shape;
      const solution = np.zeros(numEquations);

      for (let i = numEquations - 1; i >= 0; i--) {
        solution[i] = matrix[i][numVariables - 1];
        for (let j = i + 1; j < numVariables - 1; j++) {
          solution[i] -= matrix[i][j] * solution[j];
        }
        solution[i] /= matrix[i][i];
      }

      return solution;
    },
    gaussSeidel(coefficients, constants, initialGuess, maxIterations, tolerance) {
      const numEquations = coefficients.length;
      const numVariables = coefficients[0].length;
      const x = initialGuess.slice();
      let converged = false;
      let iterations = 0;

      while (!converged && iterations < maxIterations) {
        const xNew = x.slice();
        for (let i = 0; i < numEquations; i++) {
          let sum_ = 0;
          for (let j = 0; j < numVariables; j++) {
            if (j !== i) {
              sum_ += coefficients[i][j] * xNew[j];
            }
          }
          xNew[i] = (constants[i] - sum_) / coefficients[i][i];
        }

        if (np.linalg.norm(xNew - x) < tolerance) {
          converged = true;
        }

        x = xNew;
        iterations++;
      }

      return x;
    }
  }
};
</script>
