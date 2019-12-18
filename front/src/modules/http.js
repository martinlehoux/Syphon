import axios from 'axios'

export default axios.create({
  baseURL: `http://${window.location.hostname}:5000`,
  timeout: 5000,
  responseType: 'json'
})
