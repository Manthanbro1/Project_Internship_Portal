function requireAuth(requiredRole) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token || !role) {
    window.location.href = "/index.html";
    return;
  }

  if (requiredRole && role !== requiredRole) {
    alert("Unauthorized access");
    window.location.href = "/index.html";
  }
}

function authHeader() {
  return {
    "Authorization": "Bearer " + localStorage.getItem("token"),
    "Content-Type": "application/json"
  };
}
