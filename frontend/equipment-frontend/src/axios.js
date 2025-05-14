import axios from 'axios'

const api = axios.create({
  baseURL: '/api/',
})

api.interceptors.request.use((request) => {
  const access_token = localStorage.getItem('access_token')
  if (access_token) {
    request.headers.Authorization = `Bearer ${access_token}`
  }
  return request
})

api.interceptors.response.use(
  response => response,
  async (error) => {
    if (error.response?.status === 404) {
      return Promise.reject(error)
    }

    if (error.config.url.includes('/user/login')) {
      return Promise.reject(error)
    }

    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')

      if (refreshToken) {
        try {
          const response = await api.post(`/token/refresh/`, {
            refresh: refreshToken,
          })

          const newAccessToken = response.data.access
          localStorage.setItem('access_token', newAccessToken)
          error.config.headers['Authorization'] = `Bearer ${newAccessToken}`

          return api(error.config)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/user/login'
        }
      } else {
        window.location.href = '/user/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api
