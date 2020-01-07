<template lang="pug">
div
  sui-table
    sui-table-header
      sui-table-row
        sui-table-header-cell(@click="orderUsers('username')") Name
        sui-table-header-cell(@click="orderUsers('inscriptionDate')") Inscription date
        sui-table-header-cell Member
        sui-table-header-cell Admin
        sui-table-header-cell Password set
        sui-table-header-cell Actions
    sui-table-body
      sui-table-row(v-for="user in users" :key="user.username")
        sui-table-cell
          router-link(:to="`/users/${user.username}`") {{user.username}} ({{user.firstName}} {{user.lastName}})
        sui-table-cell {{user.inscriptionDate}}
        sui-table-cell
          sui-icon(v-if="user.isMember" name="toggle on" color="green")
          sui-icon(v-else name="toggle off" color="red")
        sui-table-cell
          sui-icon(v-if="user.isAdmin" name="toggle on" color="green")
          sui-icon(v-else name="toggle off" color="red")
        sui-table-cell
          sui-icon(v-if="user.hasPassword" name="toggle on" color="green")
          sui-icon(v-else name="toggle off" color="red")
        sui-table-cell
          sui-button(v-if="user.email" size="mini" icon="key" basic color="purple") New password
          sui-button(v-else size="mini" icon="key" basic color="purple" disabled) No email
          sui-button(size="mini" icon="trash" basic color="red" @click="deletingUser = user")
    sui-table-footer
      sui-table-row
        sui-table-header-cell(colspan="6")
          sui-button(:disabled="page <= 0" @click="fetchPage(page-1)" icon)
            sui-icon(name="left chevron")
          sui-button(@click="fetchPage(page+1)" icon)
            sui-icon(name="right chevron")
  sui-segment
    sui-form(@submit.prevent="createUser")
      sui-form-field
        label Username
        input(type="text" v-model="newUser.username" id="")
      sui-button(type="submit" basic positive) Create user

  DeleteUser(:user="deletingUser" v-if="deletingUser" @quit="deletingUser = null" @remove="username => removeUser(username)")
</template>

<script>
import { User } from '@/modules/models'
import DeleteUser from '@/components/DeleteUser'

export default {
  name: 'Admin',
  components: {
    DeleteUser
  },
  data () {
    return {
      users: [],
      newUser: {} || new User({}),
      page: Number(this.$route.query.page) || 0,
      deletingUser: null
    }
  },
  mounted () {
    this.getUsers()
  },
  methods: {
    getUsers () {
      this.$http.get(`users?page=${this.page}`)
        .then(res => (this.users = res.data.map(user => new User(user))))
        .catch(err => this.$error(err))
    },
    fetchPage (page) {
      this.page = page
      this.$router.push(`/admin?page=${page}`)
      this.getUsers()
    },
    createUser () {
      if (this.users.map(user => user.username).includes(this.newUser.username)) {
        this.$router.push(`/users/${this.newUser.username}`)
      } else {
        this.$http.post('users', this.newUser)
          .then(res => this.users.push(new User(res.data)))
          .then(() => this.$router.push(`/users/${this.newUser.username}`))
          .catch(err => this.$error(err))
          .then(() => (this.newUser = new User({})))
      }
    },
    removeUser (username) {
      this.users = this.users.filter(user => user.username !== username)
    },
    orderUsers (order) {
      switch (order) {
        case 'inscriptionDate':
          this.users.sort((a, b) => a.inscriptionDate < b.inscriptionDate)
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
