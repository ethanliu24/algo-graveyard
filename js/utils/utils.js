export function getReqHeader() {
  return {
    header: {
      "Content-Type": "application/json",
    },
  }
}

export function capitalizeFirst(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
};

export function formatDate(dateStr) {
  const options = { month: 'short', day: 'numeric', year: 'numeric' };
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', options);
};

export function formatQueries(queries) {
  let queryStr = new URLSearchParams(queries).toString();
  return queryStr;
};
