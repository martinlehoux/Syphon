import http from '@/modules/http'

export class User {
  username = ''
  records = []

  constructor ({ username, records }) {
    this.username = username
    if (records) this.records = records
  }

  loadRecords () {
    http.get(`users/${this.username}/records`)
      .then(res => (this.records = res.data.map(record => new Record(record))))
  }

  get bestRecord () {
    return this.records.concat().sort((a, b) => a.chrono > b.chrono).shift() || {}
  }

  get distinction () {
    const bestChrono = this.bestRecord.chrono
    return [
      'impossible',
      'Unphon',
      'Deuxphon',
      'Triphon',
      'Quadriphon',
      'Cinqphon',
      'Syphon',
      'Septphon',
      'Huitphon'
    ][Math.ceil(bestChrono / 1000)] || 'No distinction'
  }
}

export class Record {
  date = new Date().toISOString().slice(0, 10)
  chrono = 0

  constructor ({ date, chrono, id, user }) {
    if (date) this.date = date
    if (chrono) this.chrono = chrono
    if (id) this.id = id
    if (user) this.user = user
  }
}
