import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import Login from "../views/Login.vue"
import Logout from "../views/Logout.vue"
import store from "../store"
import Register from "../views/Register.vue"
import EquipmentList from "../views/EquipmentList.vue"
import AddEquipment from "../views/AddEquipment.vue"
import EquipmentTypeList from "../views/EquipmentTypeList.vue"
import EquipmentDetail from "../views/EquipmentDetail.vue"
import NotFound from "../views/NotFound.vue"

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/user/login",
    name: "Login",
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: "/logout",
    name: "Logout",
    component: Logout,
    meta: { requiresAuth: true },
  },
  {
    path: "/user/register",
    name: "Register",
    component: Register,
    meta: { requiresAuth: false },
  },
  {
    path: "/equipment",
    name: "EquipmentList",
    component: EquipmentList,
    meta: { requiresAuth: true },
  },
  {
  path: "/equipment/:id",
  name: "EquipmentDetail",
  component: EquipmentDetail,
  meta: { requiresAuth: true },
  props: true
  },
  {
    path: "/equipment/add",
    name: "AddEquipment",
    component: AddEquipment,
    meta: { requiresAuth: true },
  },
  {
    path: "/equipment-types",
    name: "EquipmentTypeList",
    component: EquipmentTypeList,
    meta: { requiresAuth: true },
  },
  {
    path: "/about",
    name: "about",
    component: () => import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
    meta: { requiresAuth: false },
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL || '/'),
  routes,
})

router.beforeEach((to, from, next) => {
  // Determine if the route requires Authentication
  const requiresAuth = to.matched.some((x) => x.meta.requiresAuth)
  const isAuthenticated = store.getters.isAuthenticated

  // If it does and they are not logged in, send the user to "/login"
  if (requiresAuth && !isAuthenticated) {
    next("/user/login")
  } else {
    // Else let them go to their next destination
    next()
  }
})

export default router
