import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    errors: []
  },
  mutations: {
    addError (state, error) {
      state.errors.push(error)
    },
    removeError (state, error) {
      state.errors = state.errors.filter(err => err !== error)
    }
  },
  actions: {
  },
  modules: {
  }
})
