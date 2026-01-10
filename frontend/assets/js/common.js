const API = "http://127.0.0.1:8000";

function getAuthHeaders() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please login again");
    window.location.href = "../auth/login.html";
    return {};
  }

  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };
}
function requireAuth(requiredRole = null) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) {
    window.location.href = "/frontend/pages/auth/login.html";
    return;
  }

  if (requiredRole && role !== requiredRole) {
    alert("Unauthorized access");
    window.location.href = "/frontend/index.html";
  }
}

function logout() {
  localStorage.clear();
  window.location.href = "/frontend/index.html";
}
