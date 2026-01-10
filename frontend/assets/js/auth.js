const API = "http://127.0.0.1:8000";

async function signup() {
  const body = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    role: document.getElementById("role").value
  };

  const res = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  if (res.ok) {
    alert("Signup successful");
    window.location.href = "login.html";
  } else {
    alert("Signup failed");
  }
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(
    `${API}/auth/login?email=${email}&password=${password}`,
    { method: "POST" }
  );

  const data = await res.json();

  if (res.ok) {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.role);

    if (data.role === "student") {
      window.location.href = "../student/my_projects.html";
    } else {
      window.location.href = "../company/post_internship.html";
    }
  } else {
    alert("Login failed");
  }
}
