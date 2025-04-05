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
