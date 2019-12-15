<template lang="pug">
  div
    h1 {{user.username}}
    table
      thead
        tr
          th Chrono
          th Date
      tbody
        tr(v-for="record in records")
          td {{(record.chrono / 1000).toFixed(3)}}
          td {{record.timestamp.toLocaleString()}}
    form(@submit.prevent="createRecord")
      //- input(type="date-time" v-model="newRecord.timestamp")
      button(@click.prevent="startChrono()") Start
      button(@click.prevent="stopChrono()") Stop
      //- input(type="number" step="0.001" v-model.number="newRecord.chrono")
      p {{(newRecord.chrono / 1000).toFixed(3)}}
      input(type="submit" value="Ajouter")
</template>

<script>
import { User, Record } from '@/modules/models'

export default {
  data () {
    return {
      user: new User({}),
      records: [],
      newRecord: new Record({}),
      interval: null
    }
  },
  created () {
    this.$http.get(`users/${this.$route.params.username}`)
      .then(res => (this.user = new User(res.data)))
      .catch(err => alert(err))
    this.$http.get(`users/${this.$route.params.username}/records`)
      .then(res => (this.records = res.data.map(record => new Record(record))))
      .catch(err => alert(err))
  },
  methods: {
    createRecord () {
      this.$http.post(`users/${this.$route.params.username}/records`, this.newRecord)
        .then(res => this.records.push(new Record(res.data)))
        .catch(err => alert(err))
      this.newRecord = new Record({})
    },
    startChrono () {
      const start = new Date()
      this.interval = setInterval(() => {
        const now = new Date()
        this.newRecord.chrono = now - start
      }, 10)
    },
    stopChrono () {
      clearInterval(this.interval)
    }
  }
}
</script>

<style>

</style>
