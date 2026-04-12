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

function getHeaders(includeJson = false) {
  const headers = {
    Authorization: `Bearer ${token}`,
  };

  if (includeJson) {
    headers["Content-Type"] = "application/json";
  }

  return headers;
}

async function safeJson(response) {
  const text = await response.text();
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function loadStudentProfile() {
  const department = document.getElementById("department");
  if (!department) {
    return;
  }

  const response = await fetch(`${API_BASE}/student/profile`, {
    headers: getHeaders(),
  });
  const profile = await safeJson(response);

  if (!response.ok || !profile) {
    alert("Failed to load profile");
    return;
  }

  document.getElementById("department").value = profile.department || "";
  document.getElementById("about").value = profile.about_me || "";
  document.getElementById("github").value = profile.github_link || "";
  document.getElementById("linkedin").value = profile.linkedin_link || "";
}

async function saveProfile() {
  const payload = {
    department: document.getElementById("department").value.trim() || null,
    about_me: document.getElementById("about").value.trim() || null,
    github_link: document.getElementById("github").value.trim() || null,
    linkedin_link: document.getElementById("linkedin").value.trim() || null,
  };

  const response = await fetch(`${API_BASE}/student/profile`, {
    method: "PUT",
    headers: getHeaders(true),
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    alert("Failed to save profile");
    return;
  }

  alert("Profile saved");
}

window.saveProfile = saveProfile;

const projectContainer = document.getElementById("projects");

if (projectContainer) {
  fetch(`${API_BASE}/student/projects`, {
    headers: getHeaders(),
  })
    .then((res) => res.json())
    .then((data) => {
      projectContainer.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        projectContainer.innerHTML = "<p>No projects yet.</p>";
        return;
      }

      data.forEach((project) => {
        const div = document.createElement("div");
        div.className = "project-card";
        div.innerHTML = `
          <h3>${project.title}</h3>
          <p>${project.description}</p>
          <small>${project.status} | ${project.difficulty}</small>
        `;
        projectContainer.appendChild(div);
      });
    });
}

const projectForm = document.getElementById("projectForm");

if (projectForm) {
  projectForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      members_count: document.getElementById("members_count").value || null,
      student_role: document.getElementById("student_role").value,
      difficulty: document.getElementById("difficulty").value,
      status: document.getElementById("status").value,
      outcome: document.getElementById("outcome").value || null,
      skills: document
        .getElementById("skills")
        .value
        .split(",")
        .map((skill) => skill.trim())
        .filter(Boolean),
    };

    const response = await fetch(`${API_BASE}/student/projects`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await safeJson(response);
      document.getElementById("error").innerText =
        error?.detail || "Failed to add project";
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
    <p>${internship.role_description || ""}</p>
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
  fetch(`${API_BASE}/student/internships/recommended`, {
    headers: getHeaders(),
  })
    .then((res) => res.json())
    .then((data) => {
      recommendedBox.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        recommendedBox.innerHTML = "<p>No recommendations yet.</p>";
        return;
      }

      data.forEach((item) => {
        renderInternship(
          recommendedBox,
          {
            id: item.internship_id,
            role_title: item.role_title,
            role_description: item.role_description || "",
          },
          item.similarity_score
        );
      });
    });
}

const allBox = document.getElementById("allInternships");
const searchInput = document.getElementById("search");

if (allBox) {
  let allInternships = [];

  fetch(`${API_BASE}/student/internships`, {
    headers: getHeaders(),
  })
    .then((res) => res.json())
    .then((data) => {
      allInternships = Array.isArray(data) ? data : [];
      renderAll(allInternships);
    });

  function renderAll(list) {
    allBox.innerHTML = "";

    if (list.length === 0) {
      allBox.innerHTML = "<p>No internships found.</p>";
      return;
    }

    list.forEach((internship) => renderInternship(allBox, internship));
  }

  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const query = searchInput.value.toLowerCase();
      const filtered = allInternships.filter(
        (internship) =>
          internship.role_title.toLowerCase().includes(query) ||
          internship.role_description.toLowerCase().includes(query)
      );
      renderAll(filtered);
    });
  }
}

const internshipData = localStorage.getItem("selectedInternship");
const titleEl = document.getElementById("roleTitle");
const descEl = document.getElementById("roleDesc");
const projectList = document.getElementById("projectList");
const applyBtn = document.getElementById("applyBtn");

if (internshipData && titleEl && descEl && projectList && applyBtn) {
  const internship = JSON.parse(internshipData);

  titleEl.innerText = internship.role_title;
  descEl.innerText = internship.role_description || "";

  let selectedProjects = [];

  fetch(`${API_BASE}/student/projects`, {
    headers: getHeaders(),
  })
    .then((res) => res.json())
    .then((projects) => {
      if (!Array.isArray(projects) || projects.length === 0) {
        projectList.innerHTML = "<p>No projects available. Add a project first.</p>";
        return;
      }

      projects.forEach((project) => {
        const label = document.createElement("label");
        label.style.display = "block";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = project.id;

        checkbox.onchange = () => {
          if (checkbox.checked) {
            selectedProjects.push(project.id);
          } else {
            selectedProjects = selectedProjects.filter((id) => id !== project.id);
          }
        };

        label.appendChild(checkbox);
        label.append(` ${project.title}`);
        projectList.appendChild(label);
      });
    });

  applyBtn.onclick = async () => {
    if (selectedProjects.length < 1 || selectedProjects.length > 3) {
      document.getElementById("error").innerText = "Select between 1 and 3 projects";
      return;
    }

    const payload = {
      internship_id: Number(internship.id),
      project_ids: selectedProjects.map(Number),
    };

    const response = await fetch(`${API_BASE}/applications`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await safeJson(response);
      document.getElementById("error").innerText =
        error?.detail || "Failed to apply";
      return;
    }

    alert("Applied successfully");
    window.location.href = "find_internship.html";
  };
}

const applicationsBox = document.getElementById("applications");

if (applicationsBox) {
  fetch(`${API_BASE}/student/applications`, {
    headers: getHeaders(),
  })
    .then((res) => res.json())
    .then((data) => {
      applicationsBox.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        applicationsBox.innerHTML = "<p>No applications yet.</p>";
        return;
      }

      data.forEach((application) => {
        const div = document.createElement("div");
        div.className = "application-card";
        div.innerHTML = `
          <h4>Internship ID: ${application.internship_id}</h4>
          <p class="status ${application.status}">Status: ${application.status}</p>
          ${
            application.status === "Rejected"
              ? `<p><strong>Reason:</strong> ${application.rejection_reason || ""}</p>`
              : ""
          }
        `;
        applicationsBox.appendChild(div);
      });
    });
}

loadStudentProfile();
