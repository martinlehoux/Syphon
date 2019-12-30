import http from '@/modules/http'

export class Record {
  date = new Date(0).toISOString().slice(0, 10)
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
  firstName = ''
  lastName = ''
  email = ''
  inscriptionDate = new Date(0).toISOString().slice(0, 10)
  isAdmin = false
  isMember = false
  records = []
  bestRecord = new Record({})

  constructor ({ username, firstName, lastName, email, inscriptionDate, isAdmin, isMember, records, bestRecord }) {
    this.username = username
    if (records) this.records = records
    if (records) this.firstName = firstName
    if (records) this.lastName = lastName
    if (records) this.email = email
    if (records) this.inscriptionDate = inscriptionDate
    if (records) this.isAdmin = isAdmin
    if (records) this.isMember = isMember
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
