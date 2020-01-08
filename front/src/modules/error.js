import store from '@/store'

export default function error (err) {
  if (err.response) {
    store.dispatch('addError', err.response.data.error)
  } else if (err.message) {
    store.dispatch('addError', err.message)
  }
}
