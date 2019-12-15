export class User {
  username = ''

  constructor ({ username }) {
    this.username = username
  }
}

export class Record {
  timestamp = new Date()
  chrono = 0

  constructor ({ timestamp, chrono, id, user }) {
    if (timestamp) this.timestamp = new Date(timestamp)
    if (chrono) this.chrono = chrono
    if (id) this.id = id
    if (user) this.user = user
  }
}
