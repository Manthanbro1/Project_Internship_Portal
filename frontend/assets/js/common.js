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
