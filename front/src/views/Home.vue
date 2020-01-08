<template lang="pug">
div
  GChart(type="ColumnChart" :data="columnChartData" :options="columnChartOptions")
  GChart(type="Histogram" :data="histogramChartData" :options="histogramChartOptions")
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      baseUrl: process.env.BASE_URL,
      columnChartOptions: {
        chart: {
          title: 'Records',
          legend: 'bottom'
        }
      },
      columnChartData: [],
      histogramChartOptions: {
        chart: {
          title: 'Best record',
          legend: 'bottom'
        }
      },
      histogramChartData: []
    }
  },
  async mounted () {
    this.$http.get('charts')
      .then(res => {
        this.columnChartData = res.data.columnChart
        this.histogramChartData = res.data.histogramChart
      })
      .catch(err => this.$error(err))
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
