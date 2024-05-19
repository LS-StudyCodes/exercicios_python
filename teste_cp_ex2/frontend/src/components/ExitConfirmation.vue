<template>
  <div v-if="showExitConfirmation" class="modal-container">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Saída de Veículo</h5>
        <button type="button" class="close" @click="$emit('close')">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="exitPlate">Placa:</label>
          <input type="text" class="form-control" id="exitPlate" :value="popupVehicle.plate" readonly>
        </div>
        <div class="form-group">
          <label for="exitCardId">ID do Cartão:</label>
          <input type="text" class="form-control" id="exitCardId" :value="popupVehicle.card_id || '-' " readonly>
        </div>
        <div class="form-group">
          <label for="exitEntryDate">Data de Entrada:</label>
          <input type="text" class="form-control" id="exitEntryDate" :value="new Date(popupVehicle.entry_date).toLocaleString()" readonly>
        </div>
        <div class="form-group">
          <label for="exitExitDate">Data de Saída:</label>
          <input type="text" class="form-control" id="exitExitDate" :value="new Date(popupVehicle.exit_date).toLocaleString()" readonly>
        </div>
        <div class="form-group">
          <label for="exitValue">Valor a Cobrar:</label>
          <input type="text" class="form-control" id="exitValue" :value="popupVehicle.value || 'Gratuito'" readonly>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="$emit('close')">OK</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showExitConfirmation: {
      type: Boolean,
      required: true
    },
    popupVehicle: {
      type: Object,
      required: true
    }
  },
  methods: {
  }
};
</script>

<style scoped>
.modal-container {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-body {
  margin-bottom: 20px;
}

.modal-footer {
  display: flex;
  justify-content: center;
}

.close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.close:hover {
  color: red;
}
</style>