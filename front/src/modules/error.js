import store from '@/store'

export default function error (err) {
  if (err.message) store.commit('addError', err.message)
  console.log(err)
}
