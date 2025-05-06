import { createStore } from "vuex"
import api from '../src/axios'

export default createStore({
  state: {
    access_token: localStorage.getItem("access_token") || "",
    refresh_token: localStorage.getItem("refresh_token") || "",
    user: JSON.parse(localStorage.getItem("user")) || null,
    loading: false,
    error: null,
    equipmentTypes: [],
    recentEquipment: [],
  },

  getters: {
    isAuthenticated: (state) => !!state.access_token,
    authStatus: (state) => (state.loading ? "loading" : state.access_token ? "success" : "failed"),
    currentUser: (state) => state.user,
    hasError: (state) => !!state.error,
    errorMessage: (state) => state.error,
    getEquipmentTypes: (state) => state.equipmentTypes,
    getRecentEquipment: (state) => state.recentEquipment,
  },

  mutations: {
    AUTH_REQUEST(state) {
      state.loading = true
      state.error = null
    },
    AUTH_SUCCESS(state, { access_token, user }) {
      state.access_token = access_token
      state.user = user
      state.loading = false
      state.error = null
    },
    AUTH_ERROR(state, error) {
      state.loading = false
      state.error = error
    },
    LOGOUT(state) {
      state.access_token = ""
      state.user = null
    },
    CLEAR_ERROR(state) {
      state.error = null
    },
    SET_EQUIPMENT_TYPES(state, types) {
      state.equipmentTypes = types
    },
    SET_RECENT_EQUIPMENT(state, equipment) {
      state.recentEquipment = equipment
    },
    SET_AUTHENTICATED(state, value) {
      state.isAuthenticated = value
    },
  },

  actions: {
    login({ commit }, credentials) {
      return new Promise((resolve, reject) => {
        commit("AUTH_REQUEST")

        api
          .post("/user/login", credentials)
          .then((response) => {
            const access_token = response.data.access_token
            const refresh_token = response.data.refresh_token
            const user = {
              id: response.data.user_id,
              username: credentials.username,
              email: response.data.email,
            }

            // Store access_token in localStorage
            localStorage.setItem("access_token", access_token)
            localStorage.setItem("refresh_token", refresh_token)
            localStorage.setItem("user", JSON.stringify(user))

            // Set access_token in axios headers
            api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`

            commit("AUTH_SUCCESS", { access_token, user })
            resolve(response)
          })
          .catch((error) => {
            commit("AUTH_ERROR", error.response?.data?.non_field_errors?.[0] || "Login failed. Please check your credentials.")
            localStorage.removeItem("access_token")
            localStorage.removeItem("refresh_token")
            localStorage.removeItem("user")
            reject(error)
          })
      })
    },

    register({ commit }, userData) {
      return new Promise((resolve, reject) => {
        commit("AUTH_REQUEST")

        api
          .post("user/register", userData)
          .then((response) => {
            resolve(response)
          })
          .catch((error) => {
            commit("AUTH_ERROR", error.response?.data?.error || "Registration failed")
            reject(error)
          })
      })
    },

    logout({ commit }) {
      return new Promise((resolve) => {
        commit("LOGOUT")
        localStorage.removeItem("access_token")
        localStorage.removeItem("refresh_token")
        localStorage.removeItem("user")
        delete api.defaults.headers.common["Authorization"]
        resolve()
      })
    },

    clearError({ commit }) {
      commit("CLEAR_ERROR")
    },

    fetchEquipmentTypes({ commit }) {
      return api.get("equipment-type").then((response) => {
        commit("SET_EQUIPMENT_TYPES", response.data.results)
        return response.data.results
      })
    },

    fetchRecentEquipment({ commit }, limit = 5) {
      return api.get(`equipment?page_size=${limit}`).then((response) => {
        commit("SET_RECENT_EQUIPMENT", response.data.results)
        return response.data.results
      })
    },
  },
})
