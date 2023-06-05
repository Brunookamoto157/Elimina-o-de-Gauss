<template>
    <div>
      <h2>Sistema de Equações Lineares</h2>
      <div>
        <label>Número de Equações:</label>
        <input type="number" v-model="numEquations">
      </div>
      <div>
        <label>Número de Variáveis:</label>
        <input type="number" v-model="numVariables">
      </div>
      <div v-for="(equation, index) in equations" :key="index">
        <h4>Equação {{ index + 1 }}</h4>
        <div v-for="(coefficient, variableIndex) in equation" :key="variableIndex">
          <label>Coeficiente {{ variableIndex + 1 }}:</label>
          <input type="number" v-model="equation[variableIndex]">
        </div>
        <label>Termo Independente:</label>
        <input type="number" v-model="constants[index]">
      </div>
      <div>
        <label>Método:</label>
        <select v-model="selectedMethod">
          <option value="1">Gauss</option>
          <option value="2">Eliminação de Gauss</option>
          <option value="3">Gauss-Seidel</option>
        </select>
      </div>
      <button @click="solve">Resolver</button>
      <div v-if="solution">
        <h4>Solução:</h4>
        <p>{{ solution }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { column_stack, zeros } from 'numpy'; // Supondo que você está usando a biblioteca numpy
  
  export default {
    data() {
      return {
        numEquations: 0,
        numVariables: 0,
        equations: [],
        constants: [],
        selectedMethod: '',
        solution: '',
      };
    },
    methods: {
      solve() {
        const coefficients = this.equations.map((equation) => [...equation]);
        const constants = [...this.constants];
  
        if (this.selectedMethod === '1') {
          // Gauss
          const augmentedMatrix = column_stack([coefficients, constants]);
          const numEquations = augmentedMatrix.shape[0];
          const numVariables = augmentedMatrix.shape[1] - 1;
  
          for (let i = 0; i < numEquations; i++) {
            const pivot = augmentedMatrix[i][i];
  
            for (let j = i + 1; j < numEquations; j++) {
              const factor = augmentedMatrix[j][i] / pivot;
              for (let k = i; k < numVariables + 1; k++) {
                augmentedMatrix[j][k] -= factor * augmentedMatrix[i][k];
              }
            }
          }
  
          const solution = this.backSubstitution(augmentedMatrix);
          this.solution = `Solução usando o método de Gauss: ${solution}`;
        } else if (this.selectedMethod === '2') {
          // Eliminação de Gauss
          const augmentedMatrix = column_stack([coefficients, constants]);
          const numEquations = augmentedMatrix.shape[0];
          const numVariables = augmentedMatrix.shape[1] - 1;
  
          for (let i = 0; i < numEquations; i++) {
            const pivot = augmentedMatrix[i][i];
  
            for (let j = i + 1; j < numEquations; j++) {
              const factor = augmentedMatrix[j][i] / pivot;
              for (let k = i; k < numVariables + 1; k++) {
                augmentedMatrix[j][k] -= factor * augmentedMatrix[i][k];
              }
            }
          }
  
          const solution = this.backSubstitution(augmentedMatrix);
          this.solution = `Solução usando o método de Eliminação de Gauss: ${solution}`;
        } else if (this.selectedMethod === '3') {
          // Gauss-Seidel
          // Implemente o código para o método Gauss-Seidel
        }
      },
      backSubstitution(matrix) {
        const numEquations = matrix.shape[0];
        const numVariables = matrix.shape[1] - 1;
        const solution = zeros(numEquations);
  
        for (let i = numEquations - 1; i >= 0; i--) {
          solution[i] = matrix[i][numVariables];
          for (let j = i + 1; j < numVariables; j++) {
            solution[i] -= matrix[i][j] * solution[j];
          }
          solution[i] /= matrix[i][i];
        }
  
        return solution;
      },
    },
  };
  </script>
  
  <style>
  /* Estilize a tela conforme necessário */
  </style>
  