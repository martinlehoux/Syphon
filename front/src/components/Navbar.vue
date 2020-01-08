<template lang="pug">
sui-menu(id="nav" :widths="4")
  sui-menu-item(header v-if="loggedIn") Welcome {{username}}
  sui-menu-item(header v-else) Please log in
  router-link(to="/" is="sui-menu-item" :active="$route.path == '/'") Home
  router-link(to="/admin" is="sui-menu-item" :active="$route.path == '/admin'" :disabled="!isAdmin") Admin
  router-link(v-if="!isAdmin" to="/signup" is="sui-menu-item" :active="$route.path == '/signup'") Sign up
  sui-menu-item(v-else @click="$store.dispatch('logout')") Logout
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Navbar',
  computed: mapState(['loggedIn', 'username', 'isAdmin'])
}
</script>

<style scoped>
button::-moz-focus-inner {
  border: 0;
}
</style>
