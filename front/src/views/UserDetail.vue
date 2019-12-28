<template lang="pug">
div
  h1 {{user.username}}
  GChart(type="LineChart" :data="chartData" :options="chartOptions" v-if="user.records.length>0")
  sui-table(single-line)
    sui-table-header
      sui-table-row
        sui-table-header-cell(@click="orderRecords('chrono')") Chrono
        sui-table-header-cell(@click="orderRecords('date')") Date
        sui-table-header-cell Actions
    sui-table-body
      sui-table-row(v-for="record in user.records" :key="record.id")
        sui-table-cell {{(record.chrono / 1000).toFixed(2)}}
        sui-table-cell {{record.date}}
        sui-table-cell
          sui-button(icon="trash" negative @click="deleteRecord(record)")
  sui-segment
    sui-form(@submit.prevent="createRecord(newRecord)")
      sui-button(@click.prevent="startChrono()") Start
      sui-button(@click.prevent="stopChrono()") Stop
      div
        sui-statistic
          sui-statistic-value {{(newRecord.chrono / 1000).toFixed(2)}}
          sui-statistic-label sec
      sui-button(type="submit" basic positive) Record
  sui-divider(horizontal) OR
  sui-segment
    sui-form(@submit.prevent="createRecord(newCustomRecord)")
      sui-form-fields(:fields="2")
        sui-form-field
          label Chrono (ms)
          input(type="number" step="0.001" v-model.number="newCustomRecord.chrono")
        sui-form-field
          label Date
          input(type="date" v-model="newCustomRecord.date")
      sui-button(type="submit" basic positive) Create
</template>

<script>
import { User, Record } from '@/modules/models'

export default {
  data () {
    return {
      user: new User({}),
      newRecord: new Record({}),
      newCustomRecord: new Record({}),
      interval: null,
      chartOptions: {
        title: 'Records',
        legend: { position: 'bottom' },
        curvetype: 'function'
      }
    }
  },
  computed: {
    chartData () {
      return [['Date', 'Chrono']].concat(this.user.records.concat().sort((a, b) => (a.date > b.date)).map(record => [record.date, record.chrono]))
    }
  },
  created () {
    this.$http.get(`users/${this.$route.params.username}`)
      .then(res => (this.user = new User(res.data)))
      .then(() => this.user.loadRecords())
      .catch(err => this.$error(err))
  },
  methods: {
    createRecord (record) {
      this.$http.post(`users/${this.$route.params.username}/records`, record)
        .then(res => this.user.records.push(new Record(res.data)))
        .catch(err => this.$error(err))
      this.newRecord = new Record({})
      this.newCustomRecord = new Record({})
    },
    deleteRecord (record) {
      this.$http.delete(`records/${record.id}`)
        .then(res => (this.user.records = this.user.records.filter(rec => rec.id !== record.id)))
        .catch(err => this.$error(err))
    },
    orderRecords (order) {
      switch (order) {
        case 'chrono':
          this.user.records.sort((a, b) => a.chrono > b.chrono)
          break
        case 'date':
          this.user.records.sort((a, b) => a.date < b.date)
          break
        default:
          this.user.records.sort((a, b) => a.date < b.date)
          break
      }
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

<style scoped>
table {
  margin-left: auto;
  margin-right: auto;
}
</style>
