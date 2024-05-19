import { createRouter, createWebHistory } from 'vue-router';
import Operation from '../components/Operation.vue';
import Vehicle from '../components/Vehicle.vue';
import Customer from '../components/Customer.vue';
import Plan from '../components/Plan.vue';
import Contract from '../components/Contract.vue';

const routes = [
  {
    path: '/', // Rota principal
    name: 'Operation',
    component: Operation
  },
  {
    path: '/vehicles',
    name: 'Vehicles',
    component: Vehicle
  },
  {
    path: '/customers',
    name: 'Customers',
    component: Customer
  },
  {
    path: '/plans',
    name: 'Plans',
    component: Plan
  },
  {
    path: '/contracts',
    name: 'Contracts',
    component: Contract
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;