<template lang="pug">
div
  ol
    li(v-for="user in users" :key="user.username")
      router-link(:to="`/users/${user.username}`") {{user.username}}
  form(@submit.prevent="createUser")
    input(type="text" v-model="newUser.username" id="")
    input(type="submit" value="New user")
</template>

<script>
import { User } from '@/modules/models'

export default {
  data () {
    return {
      users: [],
      newUser: new User({})
    }
  },
  created () {
    this.$http.get('users')
      .then(res => (this.users = res.data.map(user => new User(user))))
      .catch(err => this.$store.commit('addError', err.response.data.error))
  },
  methods: {
    createUser () {
      this.$http.post('users', this.newUser)
        .then(res => this.users.push(new User(res.data)))
        .catch(err => this.$store.commit('addError', err.response.data.error))
      this.newUser = new User({})
    }
  }
}
</script>
