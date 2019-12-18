<template lang="pug">
div
  sui-table
    sui-table-header
      sui-table-row
        sui-table-header-cell(@click="orderUsers('username')") Username
        sui-table-header-cell(@click="orderUsers('chrono')") Best record
        sui-table-header-cell Distinction
    sui-table-body
      sui-table-row(v-for="user in users" :key="user.username")
        sui-table-cell
          router-link(:to="`/users/${user.username}`") {{user.username}}
        sui-table-cell {{(user.bestRecord.chrono / 1000).toFixed(2)}} sec
        sui-table-cell {{user.distinction}}
  sui-segment
    sui-form(@submit.prevent="createUser")
      sui-form-field
        label Username
        input(type="text" v-model="newUser.username" id="")
      sui-button(type="submit" basic positive) Create user
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
      .then(() => this.users.forEach(user => user.loadRecords()))
      .catch(err => this.$error(err))
  },
  methods: {
    createUser () {
      this.$http.post('users', this.newUser)
        .then(res => this.users.push(new User(res.data)))
        .then(() => this.$router.push(`/users/${this.newUser.username}`))
        .catch(err => this.$error(err))
        .then(() => (this.newUser = new User({})))
    },
    orderUsers (order) {
      switch (order) {
        case 'chrono':
          this.users.sort((a, b) => a.bestRecord.chrono > b.bestRecord.chrono)
          break
        case 'username':
          this.users.sort((a, b) => a.username > b.username)
          break
        default:
          break
      }
    }
  }
}
</script>
