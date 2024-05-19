<template>
  <div class="container mt-5">
    <h1>Planos</h1>
    <div class="row">
      <div class="col-md-6">
        <h2>Criar/Editar Plano</h2>
        <div class="form-group">
          <label for="descriptionInput">Descrição:</label>
          <input type="text" class="form-control" id="descriptionInput" v-model="currentPlan.description" />
        </div>
        <div class="form-group">
          <label for="valueInput">Valor:</label>
          <input type="number" class="form-control" id="valueInput" v-model="currentPlan.value" />
        </div>
        <button class="btn btn-primary" @click="savePlan" v-if="!editingPlan">
          Criar
        </button>
        <button class="btn btn-success" @click="updatePlan" v-else>
          Salvar Alterações
        </button>
        <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
      </div>
      <div class="col-md-6">
        <h2>Lista de Planos</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Descrição</th>
              <th>Valor</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="plan in plans" :key="plan.id">
              <td>{{ plan.description }}</td>
              <td>{{ plan.value }}</td>
              <td>
                <button class="btn btn-warning btn-sm mr-2" @click="editPlan(plan)">
                  Editar
                </button>
                <button class="btn btn-danger btn-sm" @click="deletePlan(plan.id)">
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
      plans: [],
      currentPlan: {
        id: null,
        description: '',
        value: 0,
      },
      editingPlan: false,
      errorMessage: null,
    };
  },
  mounted() {
    this.fetchPlans();
  },
  methods: {
    async fetchPlans() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/plans/');
        this.plans = response.data;
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao buscar planos.';
      }
    },
    async savePlan() {
      this.errorMessage = null;
      try {
        await axios.post('http://localhost:8000/api/v1/plans/', this.currentPlan);
        this.currentPlan = {
          id: null,
          description: '',
          value: 0,
        };
        this.fetchPlans();
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao criar plano.';
        }
      }
    },
    editPlan(plan) {
      this.editingPlan = true;
      this.currentPlan = { ...plan };
    },
    async updatePlan() {
      this.errorMessage = null;
      try {
        await axios.put(
          `http://localhost:8000/api/v1/plans/${this.currentPlan.id}/`,
          this.currentPlan,
        );
        this.editingPlan = false;
        this.currentPlan = {
          id: null,
          description: '',
          value: 0,
        };
        this.fetchPlans();
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Erro ao atualizar plano.';
        }
      }
    },
    async deletePlan(planId) {
      this.errorMessage = null;
      try {
        await axios.delete(`http://localhost:8000/api/v1/plans/${planId}/`);
        this.fetchPlans();
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Erro ao excluir plano.';
      }
    },
  },
};
</script>