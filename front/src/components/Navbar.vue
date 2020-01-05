<template lang="pug">
sui-menu(id="nav" :widths="4")
  sui-menu-item(header v-if="loggedIn") Welcome {{username}}
  sui-menu-item(header v-else) Please log in
  router-link(to="/users" is="sui-menu-item" :active="$route.path == '/users'") User List &nbsp;
  router-link(to="/records" is="sui-menu-item" :active="$route.path == '/records'") Records &nbsp;
  router-link(to="/signup" is="sui-menu-item" :active="$route.path == '/signup'") Sign up &nbsp;
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Navbar',
  computed: mapState(['loggedIn', 'username'])
}
</script>

<style scoped>
button::-moz-focus-inner {
  border: 0;
}
</style>
