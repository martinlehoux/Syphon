<template lang="pug">
sui-container
  sui-message(
    v-for="error in errors"
    :key="error"
    header="An error has occured"
    :content="error"
    dismissable
    error
    @dismiss="handleDismiss(error)"
  )
</template>

<script>
export default {
  data () {
    return {
    }
  },
  computed: {
    errors () {
      return this.$store.state.errors
    }
  },
  methods: {
    handleDismiss (error) {
      this.$store.commit('removeError', error)
    }
  }
}
</script>
