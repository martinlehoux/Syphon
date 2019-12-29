import jwt from 'jsonwebtoken'

export function checkToken (token) {
  return token && jwt.decode(token) && jwt.decode(token).exp > Date.now() / 1000
}

export function login (token) {
  if (checkToken(token)) {
    localStorage.setItem('authorizationToken', token)
    return true
  }
  return false
}

export function logout () {
  localStorage.removeItem('authorizationToken')
  return true
}
