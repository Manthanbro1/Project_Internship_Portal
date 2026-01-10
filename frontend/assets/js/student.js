const API_BASE = "http://localhost:8000";

const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

if (!token || role !== "student") {
  alert("Unauthorized");
  window.location.href = "../../index.html";
}

function logout() {
  localStorage.clear();
  window.location.href = "../../index.html";
}

// Load projects if page has #projects
const projectContainer = document.getElementById("projects");

if (projectContainer) {
  fetch(`${API_BASE}/student/projects`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.length === 0) {
      projectContainer.innerHTML = "<p>No projects yet.</p>";
      return;
    }

    data.forEach(p => {
      const div = document.createElement("div");
      div.className = "project-card";
      div.innerHTML = `
        <h3>${p.title}</h3>
        <p>${p.description}</p>
        <small>${p.status} | ${p.difficulty}</small>
      `;
      projectContainer.appendChild(div);
    });
  });
}
const projectForm = document.getElementById("projectForm");

if (projectForm) {
  projectForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      members_count: document.getElementById("members_count").value || null,
      student_role: document.getElementById("student_role").value,
      difficulty: document.getElementById("difficulty").value,
      status: document.getElementById("status").value,
      outcome: document.getElementById("outcome").value || null,
      skills: document.getElementById("skills").value
                .split(",")
                .map(s => s.trim())
                .filter(Boolean)
    };

    const res = await fetch(`${API_BASE}/student/projects`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      document.getElementById("error").innerText = "Failed to add project";
      return;
    }

    window.location.href = "my_projects.html";
  });
}


function renderInternship(container, internship, score = null) {
  const div = document.createElement("div");
  div.className = "internship-card";

  div.innerHTML = `
    <h4>${internship.role_title}</h4>
    ${score !== null ? `<p class="match">Match: ${score}%</p>` : ""}
    <button class="btn secondary">View</button>
  `;

  div.querySelector("button").onclick = () => {
    localStorage.setItem("selectedInternship", JSON.stringify(internship));
    window.location.href = "internship_detail.html";
  };

  container.appendChild(div);
}

const recommendedBox = document.getElementById("recommended");

if (recommendedBox) {
  fetch(`${API_BASE}/company/internships/recommended`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.length === 0) {
      recommendedBox.innerHTML = "<p>No recommendations yet.</p>";
      return;
    }

    data.forEach(r => {
  renderInternship(
    recommendedBox,
    {
      id: r.internship_id,           // ✅ FIX
      role_title: r.role_title,
      role_description: r.role_description || ""
    },
    r.similarity_score
  );
  });
  });
}
const allBox = document.getElementById("allInternships");
const searchInput = document.getElementById("search");

if (allBox) {
  let allInternships = [];

  fetch(`${API_BASE}/company/internships`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => {
    allInternships = data;
    renderAll(allInternships);
  });

  function renderAll(list) {
    allBox.innerHTML = "";
    if (list.length === 0) {
      allBox.innerHTML = "<p>No internships found.</p>";
      return;
    }
    list.forEach(i => renderInternship(allBox, i));
  }

  searchInput.addEventListener("input", () => {
    const q = searchInput.value.toLowerCase();
    const filtered = allInternships.filter(i =>
      i.role_title.toLowerCase().includes(q) ||
      i.role_description.toLowerCase().includes(q)
    );
    renderAll(filtered);
  });
}
const internshipData = localStorage.getItem("selectedInternship");
const titleEl = document.getElementById("roleTitle");
const descEl = document.getElementById("roleDesc");
const projectList = document.getElementById("projectList");
const applyBtn = document.getElementById("applyBtn");

if (internshipData && titleEl) {
  const internship = JSON.parse(internshipData);

  titleEl.innerText = internship.role_title;
  descEl.innerText = internship.role_description || "";

  let selectedProjects = [];

  // Load student's projects
  fetch(`${API_BASE}/student/projects`, {
    headers: { "Authorization": `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(projects => {
    projects.forEach(p => {
      const label = document.createElement("label");
      label.style.display = "block";

      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.value = p.id;

      cb.onchange = () => {
        if (cb.checked) selectedProjects.push(p.id);
        else selectedProjects = selectedProjects.filter(id => id !== p.id);
      };

      label.appendChild(cb);
      label.append(` ${p.title}`);
      projectList.appendChild(label);
    });
  });

  applyBtn.onclick = async () => {
  if (selectedProjects.length < 1 || selectedProjects.length > 3) {
    document.getElementById("error").innerText =
      "Select between 1 and 3 projects";
    return;
  }

  const payload = {
    internship_id: Number(internship.id),
    project_ids: selectedProjects.map(Number)
  };

  console.log("APPLY PAYLOAD", payload);

  const res = await fetch(`${API_BASE}/applications`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const err = await res.json();
    console.error(err);
    document.getElementById("error").innerText =
      err.detail?.msg || JSON.stringify(err.detail);
    return;
  }

  alert("Applied successfully");
  window.location.href = "find_internship.html";
  };

}
const applicationsBox = document.getElementById("applications");

if (applicationsBox) {
  fetch(`${API_BASE}/student/applications`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.length === 0) {
      applicationsBox.innerHTML = "<p>No applications yet.</p>";
      return;
    }

    data.forEach(app => {
      const div = document.createElement("div");
      div.className = "application-card";

      div.innerHTML = `
        <h4>Internship ID: ${app.internship_id}</h4>
        <p class="status ${app.status}">Status: ${app.status}</p>
        ${
          app.status === "Rejected"
            ? `<p><strong>Reason:</strong> ${app.rejection_reason}</p>`
            : ""
        }
      `;

      applicationsBox.appendChild(div);
    });
  });
}
