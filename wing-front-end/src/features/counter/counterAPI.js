/**
 * A mock function to mimic making an async request for data
 * @param {Number} amount
 * @return {Promise}
 */
export function fetchCount(amount = 1) {
  return new Promise((resolve) =>
    setTimeout(() => resolve({ data: amount }), 500)
  );
}
