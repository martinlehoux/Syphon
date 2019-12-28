import http from '@/modules/http'

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

export class User {
  username = ''
  records = []
  bestRecord = new Record({})

  constructor ({ username, records, bestRecord }) {
    this.username = username
    if (records) this.records = records
    if (bestRecord) this.bestRecord = new Record(bestRecord)
  }

  loadRecords () {
    http.get(`users/${this.username}/records`)
      .then(res => (this.records = res.data.map(record => new Record(record))))
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
