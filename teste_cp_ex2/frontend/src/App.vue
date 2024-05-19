<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <a class="navbar-brand" href="#">Parking System</a>
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Operação</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/vehicles">Veículos</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/customers">Clientes</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/plans">Planos</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/contracts">Contratos</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
}
</script>