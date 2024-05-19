<template>
  <div class="container mt-5">
    <h1>Operação</h1>
    <div class="row">
      <div class="col-md-6">
        <h2>Entrada de Veículo</h2>
        <div class="form-group">
          <label for="plateInput">Placa:</label>
          <input type="text" class="form-control" id="plateInput" v-model="plate" />
        </div>
        <div class="form-group">
          <label for="cardIdInput">ID do Cartão:</label>
          <input type="text" class="form-control" id="cardIdInput" v-model="cardId" />
        </div>
        <button class="btn btn-primary" @click="registerEntry">Registrar Entrada</button>
        <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
      </div>
      <div class="col-md-6">
        <h2>Veículos no Pátio</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Placa</th>
              <th>ID do Cartão</th>
              <th>Entrada</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="movement in sortedParkMovements" :key="movement.id">
              <td>{{ movement.plate }}</td>
              <td>{{ movement.card_id || '' }}</td>
              <td>{{ new Date(movement.entry_date).toLocaleString() }}</td>
              <td>
                <button 
                  class="btn btn-danger btn-sm" 
                  @click="registerExit(movement.id)" 
                  :disabled="movement.exit_date" 
                >Registrar Saída</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <ExitConfirmation 
      :showExitConfirmation="showExitConfirmation" 
      :popupVehicle="popupVehicle" 
      @close="showExitConfirmation = false" 
    />
  </div>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';
import ExitConfirmation from './ExitConfirmation.vue';

export default {
  components: {
    ExitConfirmation
  },
  data() {
    return {
      plate: '',
      cardId: '',
      parkMovements: [],
      errorMessage: null,
      showExitConfirmation: false,
      popupVehicle: {},
    };
  },
  mounted() {
    this.fetchParkMovements();
  },
  computed: {
    sortedParkMovements() {
      return this.parkMovements.sort((a, b) => new Date(b.entry_date) - new Date(a.entry_date));
    }
  },
  methods: {
    async fetchParkMovements() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/park-movements/');
        this.parkMovements = response.data;
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao buscar veículos no pátio.';
      }
    },
    async registerEntry() {
      this.errorMessage = null;
      try {
        const response = await axios.post('http://localhost:8000/api/v1/park-movements/', {
          plate: this.plate,
          card_id: this.cardId,
        });

        this.fetchParkMovements(); 

        this.plate = '';
        this.cardId = '';
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao registrar entrada.';
        }
      }
    },
    async registerExit(movementId) {
      this.errorMessage = null;
      try {
        const response = await axios.patch(`http://localhost:8000/api/v1/park-movements/${movementId}/`, {
          exit_date: new Date().toISOString(),
        });

        this.fetchParkMovements();

        this.amount = response.data.value;

        this.showExitConfirmation = true; 
        this.popupVehicle = response.data; 
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao registrar saída.';
        }
      }
    },
    showExitPopup(movementId) {
    },
  },
};
</script>