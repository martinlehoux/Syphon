<template lang="pug">
sui-modal(:open="user")
  sui-modal-header Delete {{user.username}} ?
  sui-modal-actions
    sui-button(positive basic @click="$emit('quit')") Cancel
    sui-button(negative @click="deleteUser()") Delete
</template>

<script>
import { User } from '@/modules/models'
import http from '@/modules/http'

export default {
  name: 'DeleteUser',
  props: {
    user: User
  },
  methods: {
    deleteUser () {
      http.delete(`users/${this.user.username}`)
        .then(() => this.$emit('remove', this.user.username))
        .then(() => this.$emit('quit'))
        .catch(err => this.$error(err))
    }
  }
}
</script>
