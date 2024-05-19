<template>
  <div class="container mt-5">
    <h1>Veículos</h1>
    <div class="row">
      <div class="col-md-6">
        <h2>Cadastrar/Editar Veículo</h2>
        <div class="form-group">
          <label for="plateInput">Placa:</label>
          <input type="text" class="form-control" id="plateInput" v-model="currentVehicle.plate" />
        </div>
        <div class="form-group">
          <label for="modelInput">Modelo:</label>
          <input type="text" class="form-control" id="modelInput" v-model="currentVehicle.model" />
        </div>
        <div class="form-group">
          <label for="descriptionInput">Descrição:</label>
          <input type="text" class="form-control" id="descriptionInput" v-model="currentVehicle.description" />
        </div>
        <div class="form-group">
          <label for="customerIdSelect">Cliente:</label>
          <select class="form-control" id="customerIdSelect" v-model="currentVehicle.customer">
            <option value="">Selecione um cliente</option>
            <option v-for="customer in customers" :key="customer.id" :value="customer.id">
              {{ customer.name }}
            </option>
          </select>
        </div>
        <button class="btn btn-primary" @click="saveVehicle" v-if="!editingVehicle">
          Cadastrar
        </button>
        <button class="btn btn-success" @click="updateVehicle" v-else>
          Salvar Alterações
        </button>
        <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
      </div>
      <div class="col-md-6">
        <h2>Lista de Veículos</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Placa</th>
              <th>Modelo</th>
              <th>Descrição</th>
              <th>Cliente</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vehicle in vehicles" :key="vehicle.id">
              <td>{{ vehicle.plate }}</td>
              <td>{{ vehicle.model }}</td>
              <td>{{ vehicle.description }}</td>
              <td>{{ vehicle.customer ? vehicle.customer.name : '-' }}</td>
              <td>
                <button class="btn btn-warning btn-sm mr-2" @click="editVehicle(vehicle)">
                  Editar
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteVehicle(vehicle.id)">
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
      vehicles: [],
      customers: [],
      currentVehicle: {
        id: null,
        plate: '',
        model: '',
        description: '',
        customer: '',
      },
      editingVehicle: false,
      errorMessage: null,
    };
  },
  mounted() {
    this.fetchVehicles();
    this.fetchCustomers();
  },
  methods: {
    async fetchVehicles() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/vehicles/');
        this.vehicles = response.data;
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao buscar veículos.';
      }
    },
    async fetchCustomers() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/customers/');
        this.customers = response.data;
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao buscar clientes.';
      }
    },
    async saveVehicle() {
      this.errorMessage = null;
      try {
        await axios.post('http://localhost:8000/api/v1/vehicles/', this.currentVehicle);
        this.currentVehicle = {
          id: null,
          plate: '',
          model: '',
          description: '',
          customer: '',
        };
        this.fetchVehicles();
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao cadastrar veículo.';
        }
      }
    },
    editVehicle(vehicle) {
      this.editingVehicle = true;
      this.currentVehicle = { ...vehicle };
    },
    async updateVehicle() {
      this.errorMessage = null;
      try {
        await axios.put(
          `http://localhost:8000/api/v1/vehicles/${this.currentVehicle.id}/`,
          this.currentVehicle,
        );
        this.editingVehicle = false;
        this.currentVehicle = {
          id: null,
          plate: '',
          model: '',
          description: '',
          customer: '',
        };
        this.fetchVehicles();
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao atualizar veículo.';
        }
      }
    },
    async deleteVehicle(vehicleId) {
      this.errorMessage = null;
      try {
        await axios.delete(`http://localhost:8000/api/v1/vehicles/${vehicleId}/`);
        this.fetchVehicles();
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao excluir veículo.';
      }
    },
  },
};
</script>