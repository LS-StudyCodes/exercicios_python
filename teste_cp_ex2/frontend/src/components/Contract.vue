<template>
  <div class="container mt-5">
    <h1>Contratos</h1>
    <div class="row">
      <div class="col-md-6">
        <h2>Criar/Editar Contrato</h2>
        <div class="form-group">
          <label for="descriptionInput">Descrição:</label>
          <input type="text" class="form-control" id="descriptionInput" v-model="currentContract.description" />
        </div>
        <div class="form-group">
          <label for="maxValueInput">Valor Máximo:</label>
          <input type="number" class="form-control" id="maxValueInput" v-model="currentContract.max_value" />
        </div>
        <h3>Regras</h3>
        <div v-for="(rule, index) in currentContract.rules" :key="index">
          <div class="form-group">
            <label :for="`untilInput${index}`">Até (minutos):</label>
            <input type="number" class="form-control" :id="`untilInput${index}`" v-model.number="rule.until" />
          </div>
          <div class="form-group">
            <label :for="`valueInput${index}`">Valor:</label>
            <input type="number" class="form-control" :id="`valueInput${index}`" v-model.number="rule.value" />
          </div>
          <button class="btn btn-danger btn-sm mb-2" @click="removeRule(index)">
            Remover Regra
          </button>
        </div>
        <button class="btn btn-secondary mb-3" @click="addRule">Adicionar Regra</button>
        <button class="btn btn-primary" @click="saveContract" v-if="!editingContract">
          Criar
        </button>
        <button class="btn btn-success" @click="updateContract" v-else>
          Salvar Alterações
        </button>
        <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
      </div>
      <div class="col-md-6">
        <h2>Lista de Contratos</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Descrição</th>
              <th>Valor Máximo</th>
              <th>Regras</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="contract in contracts" :key="contract.id">
              <td>{{ contract.description }}</td>
              <td>{{ contract.max_value }}</td>
              <td>
                <ul>
                  <li v-for="rule in contract.rules" :key="rule.id">
                    Até {{ rule.until }} minutos: {{ rule.value }}
                  </li>
                </ul>
              </td>
              <td>
                <button class="btn btn-warning btn-sm mr-2" @click="editContract(contract)">
                  Editar
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteContract(contract.id)">
                  Excluir
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';

export default {
  data() {
    return {
      contracts: [],
      currentContract: {
        id: null,
        description: '',
        max_value: 0,
        rules: [],
      },
      editingContract: false,
      errorMessage: null,
    };
  },
  mounted() {
    this.fetchContracts();
  },
  methods: {
    async fetchContracts() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/contracts/');
        this.contracts = response.data.map(contract => ({
          ...contract,
          rules: contract.rules || [] 
        }));
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao buscar contratos.';
      }
    },
    async saveContract() {
      this.errorMessage = null;
      try {
        const response = await axios.post('http://localhost:8000/api/v1/contracts/', this.currentContract);
        this.contracts.push(response.data);
        this.currentContract = {
          id: null,
          description: '',
          max_value: 0,
          rules: [],
        };
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao criar contrato.';
        }
      }
    },
    editContract(contract) {
      this.editingContract = true;

      this.currentContract = JSON.parse(JSON.stringify(contract)); 

      this.currentContract.rules = contract.rules || []; 
    },
    async updateContract() {
      this.errorMessage = null;
      try {
        await axios.put(
          `http://localhost:8000/api/v1/contracts/${this.currentContract.id}/`,
          this.currentContract,
        );
        const index = this.contracts.findIndex(c => c.id === this.currentContract.id);
        if (index !== -1) {
          this.contracts.splice(index, 1, this.currentContract); 
        }
        this.editingContract = false;
        this.currentContract = {
          id: null,
          description: '',
          max_value: 0,
          rules: [],
        };
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao atualizar contrato.';
        }
      }
    },
    async deleteContract(contractId) {
      this.errorMessage = null;
      try {
        await axios.delete(`http://localhost:8000/api/v1/contracts/${contractId}/`);
        this.contracts = this.contracts.filter(c => c.id !== contractId);
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao excluir contrato.';
      }
    },
    addRule() {
      if (!Array.isArray(this.currentContract.rules)) {
        this.currentContract.rules = [];
      }
      this.currentContract.rules.push({ until: 0, value: 0 });
    },
    removeRule(index) {
      Vue.delete(this.currentContract.rules, index);
    },
  },
};
</script>