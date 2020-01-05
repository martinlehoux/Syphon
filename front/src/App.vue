<template lang="pug">
div(id="app")
  Navbar
  error-list
  sui-container
    router-view
</template>

<script>
import ErrorList from '@/components/ErrorList.vue'
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'App',
  components: {
    ErrorList,
    Navbar
  },
  mounted () {
    const token = localStorage.getItem('authorizationToken')
    this.$store.dispatch('saveToken', token)
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
