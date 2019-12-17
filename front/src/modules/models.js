export class User {
  username = ''

  constructor ({ username }) {
    this.username = username
  }
}

export class Record {
  date = ''
  chrono = 0

  constructor ({ date, chrono, id, user }) {
    if (date) this.date = date
    if (chrono) this.chrono = chrono
    if (id) this.id = id
    if (user) this.user = user
  }
}
