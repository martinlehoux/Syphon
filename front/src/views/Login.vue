<template lang="pug">
div
  sui-form(@submit.prevent="login()")
    sui-form-fields(:fields="3")
      sui-form-field
        input(placeholder="Username" v-model="username")
      sui-form-field
        input(type="password" placeholder="Password" v-model="password")
      sui-form-field
        sui-button(type="submit") Login
</template>

<script>

export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login () {
      this.$store.dispatch('login', { username: this.username, password: this.password })
    }
  }
}
</script>
