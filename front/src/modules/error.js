import store from '@/store'

export default function error (err) {
  // TODO: Handle 401 to fetch new token
  if (err.response) {
    store.commit('addError', err.response.data.error)
  } else if (err.message) {
    store.commit('addError', err.message)
  }
  console.log(err)
}
