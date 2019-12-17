<template lang="pug">
div
  h1 {{user.username}}
  GChart(type="ScatterChart" :data="chartData" :options="chartOptions" v-if="records.length>0")
  sui-table(single-line)
    sui-table-header
      sui-table-row
        sui-table-header-cell(@click="orderRecords('chrono')") Chrono
        sui-table-header-cell(@click="orderRecords('date')") Date
    sui-table-body
      sui-table-row(v-for="record in records" :key="record.id")
        sui-table-cell {{(record.chrono / 1000).toFixed(2)}}
        sui-table-cell {{record.date}}
  form(@submit.prevent="createRecord(newRecord)")
    button(@click.prevent="startChrono()") Start
    button(@click.prevent="stopChrono()") Stop
    p {{(newRecord.chrono / 1000).toFixed(2)}}
    input(type="submit" value="Ajouter")
  p OR
  form(@submit.prevent="createRecord(newCustomRecord)")
    input(type="number" step="0.001" v-model.number="newCustomRecord.chrono" placeholder="Chrono")
    input(type="date" v-model="newCustomRecord.date")
    input(type="submit" value="Create")
</template>

<script>
import { User, Record } from '@/modules/models'

export default {
  data () {
    return {
      user: new User({}),
      records: [],
      newRecord: new Record({}),
      newCustomRecord: new Record({}),
      interval: null,
      chartOptions: {
        chart: {
          title: 'Records',
          legend: { position: 'bottom' }
        }
      }
    }
  },
  computed: {
    chartData () {
      return [['Date', 'Chrono']].concat(this.records.map(record => [record.date, record.chrono]))
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
    createRecord (record) {
      this.$http.post(`users/${this.$route.params.username}/records`, record)
        .then(res => this.records.push(new Record(res.data)))
        .catch(err => alert(err))
      this.newRecord = new Record({})
      this.newCustomRecord = new Record({})
    },
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
