<template lang="pug">
div
  sui-item-group(divided)
    sui-item(v-for="record in records" :key="record.id")
      sui-item-image
      sui-item-content
        sui-item-header {{(record.chrono / 1000).toFixed(2)}} sec by {{record.user}}
        sui-item-meta
          span {{record.date}}
</template>

<script>
import { Record } from '@/modules/models'

export default {
  data () {
    return {
      baseUrl: process.env.BASE_URL,
      records: []
    }
  },
  created () {
    this.$http.get('records')
      .then(res => (this.records = res.data.map(record => new Record(record))))
      .catch(err => this.$store.commit('addError', err.response.data.error))
  },
  methods: {
    orderRecords (order) {
      switch (order) {
        case 'chrono':
          this.records.sort((a, b) => a.chrono > b.chrono)
          break
        case 'date':
          this.records.sort((a, b) => a.date < b.date)
          break
        default:
          this.records.sort((a, b) => a.date < b.date)
          break
      }
    }
  }
}
</script>
