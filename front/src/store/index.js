import Vue from 'vue'
import Vuex from 'vuex'
import http from '@/modules/http'
import router from '@/router'
import { login, logout, checkToken } from '@/modules/auth'
import jwt from 'jsonwebtoken'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    errors: [],
    username: null,
    logginIn: false,
    loggedIn: false,
    token: null
  },
  getters: {
  },
  mutations: {
    addError (state, error) {
      state.errors.push(error)
    },
    removeError (state, error) {
      state.errors = state.errors.filter(err => err !== error)
    },
    loginRequest (state, username) {
      state.username = username
      state.logginIn = true
    },
    loginSuccess (state, token) {
      state.username = jwt.decode(token).username
      state.loggedIn = true
      state.logginIn = false
      state.token = token
      login(token)
    },
    loginFailure (state) {
      state.logginIn = false
      state.loggedIn = false
      state.username = null
      state.token = null
    },
    logout (state) {
      state.loggedIn = false
      state.username = null
      state.token = null
      logout()
    }
  },
  actions: {
    addError ({ commit }, error) {
      commit('addError', error)
    },
    removeError ({ commit }, error) {
      commit('removeError', error)
    },
    async login ({ dispatch, commit }, { username, password }) {
      commit('loginRequest', username)
      try {
        const res = await http.post('/token', { username, password })
        commit('loginSuccess', res.data.token)
        router.push('/')
      } catch (err) {
        commit('loginFailure')
        dispatch('addError', err)
      }
    },
    saveToken ({ commit }, token) {
      if (checkToken(token)) {
        commit('loginSuccess', token)
      } else {
        commit('loginFailure')
      }
    },
    logout ({ commit }) {
      commit('logout')
    }
  },
  modules: {
  }
})
