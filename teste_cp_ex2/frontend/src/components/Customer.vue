<template>
  <div class="container mt-5">
    <h1>Clientes</h1>
    <div class="row">
      <div class="col-md-6">
        <h2>Cadastrar/Editar Cliente</h2>
        <div class="form-group">
          <label for="nameInput">Nome:</label>
          <input type="text" class="form-control" id="nameInput" v-model="currentCustomer.name" />
        </div>
        <div class="form-group">
          <label for="cardIdInput">ID do Cartão:</label>
          <input type="text" class="form-control" id="cardIdInput" v-model="currentCustomer.card_id" />
        </div>
        <button class="btn btn-primary" @click="saveCustomer" v-if="!editingCustomer">
          Cadastrar
        </button>
        <button class="btn btn-success" @click="updateCustomer" v-else>
          Salvar Alterações
        </button>
        <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
      </div>
      <div class="col-md-6">
        <h2>Lista de Clientes</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>ID do Cartão</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="customer in customers" :key="customer.id">
              <td>{{ customer.name }}</td>
              <td>{{ customer.card_id }}</td>
              <td>
                <button class="btn btn-warning btn-sm mr-2" @click="editCustomer(customer)">
                  Editar
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteCustomer(customer.id)">
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

export default {
  data() {
    return {
      customers: [],
      currentCustomer: {
        id: null,
        name: '',
        card_id: '',
      },
      editingCustomer: false,
      errorMessage: null,
    };
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    async fetchCustomers() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/customers/');
        this.customers = response.data;
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao buscar clientes.';
      }
    },
    async saveCustomer() {
      this.errorMessage = null;
      try {
        await axios.post('http://localhost:8000/api/v1/customers/', this.currentCustomer);
        this.currentCustomer = {
          id: null,
          name: '',
          card_id: '',
        };
        this.fetchCustomers();
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao cadastrar cliente.';
        }
      }
    },
    editCustomer(customer) {
      this.editingCustomer = true;
      this.currentCustomer = { ...customer };
    },
    async updateCustomer() {
      this.errorMessage = null;
      try {
        await axios.put(
          `http://localhost:8000/api/v1/customers/${this.currentCustomer.id}/`,
          this.currentCustomer,
        );
        this.editingCustomer = false;
        this.currentCustomer = {
          id: null,
          name: '',
          card_id: '',
        };
        this.fetchCustomers();
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao atualizar cliente.';
        }
      }
    },
    async deleteCustomer(customerId) {
      this.errorMessage = null;
      try {
        await axios.delete(`http://localhost:8000/api/v1/customers/${customerId}/`);
        this.fetchCustomers();
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao excluir cliente.';
      }
    },
  },
};
</script>