<template lang="pug">
div
  sui-form(@submit.prevent="signup()")
    sui-form-field
      input(placeholder="Username" v-model="user.username")
    sui-form-field
      input(placeholder="First name" v-model="user.firstName")
    sui-form-field
      input(placeholder="Last name" v-model="user.lastName")
    sui-form-field
      input(placeholder="Password" type="password" v-model="user.password")
    sui-form-field
      input(placeholder="Password" type="password" v-model="user.password_bis")
    sui-form-field
      input(placeholder="Email" type="email" v-model="user.email")
    sui-form-field
      sui-button(type="submit") Sign up
</template>

<script>
export default {
  name: 'Signup',
  data () {
    return {
      user: { }
    }
  },
  methods: {
    signup () {
      this.$http.post('/users', {
        username: this.user.username,
        first_name: this.user.firstName,
        last_name: this.user.lastName,
        email: this.user.email,
        password: this.user.password
      })
        .then(res => this.$router.push('/login'))
        .catch(err => this.$error(err))
    }
  }
}
</script>
