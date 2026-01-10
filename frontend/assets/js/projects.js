async function loadProjects() {
  const res = await fetch(`${API}/student/projects`, {
    headers: getAuthHeaders()
  });

  if (!res.ok) {
    alert("Failed to load projects");
    return;
  }

  const projects = await res.json();
  const container = document.getElementById("projects");
  container.innerHTML = "";

  projects.forEach(p => {
    const div = document.createElement("div");
    div.innerHTML = `
      <h4>${p.title}</h4>
      <p>${p.description}</p>
      <small>${p.difficulty} | ${p.status}</small>
      <hr/>
    `;
    container.appendChild(div);
  });
}

function goToAdd() {
  window.location.href = "add_project.html";
}

loadProjects();

async function submitProject() {
  const body = {
    title: document.getElementById("title").value,
    description: document.getElementById("description").value,
    members_count: Number(document.getElementById("members").value),
    student_role: document.getElementById("role").value,
    difficulty: document.getElementById("difficulty").value,
    status: document.getElementById("status").value,
    outcome: document.getElementById("outcome").value,
    skills: document.getElementById("skills").value.split(",").map(s => s.trim())
  };

  const res = await fetch(`${API}/student/projects`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body)
  });

  if (res.ok) {
    alert("Project added");
    window.location.href = "my_projects.html";
  } else {
    alert("Failed to add project");
  }
}
