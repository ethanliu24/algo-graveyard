export function getReqBody(method, payload) {
  return {
    method: method.toUpperCase(),
    headers: {
      "Content-Type": "application/json",
    },
    body: payload,
  }
}
