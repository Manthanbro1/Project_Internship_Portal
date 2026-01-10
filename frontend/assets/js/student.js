async function loadProfile() {
  const res = await fetch(`${API}/student/profile`, {
    headers: getAuthHeaders()
  });

  const p = await res.json();
  document.getElementById("department").value = p.department || "";
  document.getElementById("about").value = p.about_me || "";
  document.getElementById("github").value = p.github_link || "";
  document.getElementById("linkedin").value = p.linkedin_link || "";
}

async function saveProfile() {
  const body = {
    department: document.getElementById("department").value,
    about_me: document.getElementById("about").value,
    github_link: document.getElementById("github").value,
    linkedin_link: document.getElementById("linkedin").value
  };

  const res = await fetch(`${API}/student/profile`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) alert("Profile saved");
  else alert("Failed to save");
}

loadProfile();
