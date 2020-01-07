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

  constructor ({ username, firstName, lastName, email, inscriptionDate, isAdmin, isMember, hasPassword, records, bestRecord }) {
    this.username = username
    if (records) this.records = records
    if (firstName) this.firstName = firstName
    if (lastName) this.lastName = lastName
    if (email) this.email = email
    if (inscriptionDate) this.inscriptionDate = inscriptionDate
    if (isAdmin) this.isAdmin = isAdmin
    if (isMember) this.isMember = isMember
    if (hasPassword) this.hasPassword = hasPassword
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
