const API_BASE = "http://localhost:8000";

document.getElementById("signupForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    role: document.getElementById("role").value
  };

  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    document.getElementById("error").innerText = "Signup failed";
    return;
  }

  window.location.href = "login.html";
});


document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(
    `${API_BASE}/auth/login?email=${email}&password=${password}`,
    { method: "POST" }
  );

  const data = await res.json();

  if (!res.ok) {
    document.getElementById("error").innerText = "Invalid credentials";
    return;
  }

  localStorage.setItem("token", data.access_token);
  localStorage.setItem("role", data.role);

  // TEMP redirect (we’ll replace later)
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("role", data.role);

  if (data.role === "student") {
    window.location.href = "../student/my_projects.html";
  } else {
    window.location.href = "../company/post_internship.html";
  }

});
