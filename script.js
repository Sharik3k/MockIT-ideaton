const observer = typeof IntersectionObserver === "function"
  ? new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.18,
      }
    )
  : null;

document.querySelectorAll(".reveal").forEach((element) => {
  if (observer) {
    observer.observe(element);
  } else {
    element.classList.add("visible");
  }
});

document.querySelectorAll(".faq-item").forEach((item) => {
  item.addEventListener("toggle", () => {
    if (!item.open) {
      return;
    }

    document.querySelectorAll(".faq-item").forEach((other) => {
      if (other !== item) {
        other.open = false;
      }
    });
  });
});

const DEMO_STORAGE_KEY = "mockit-demo-state";

function readDemoState() {
  try {
    return JSON.parse(localStorage.getItem(DEMO_STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function writeDemoState(patch) {
  const nextState = { ...readDemoState(), ...patch };
  localStorage.setItem(DEMO_STORAGE_KEY, JSON.stringify(nextState));
  return nextState;
}

function showDemoToast(message) {
  const toast = document.createElement("div");
  toast.className = "demo-toast";
  toast.textContent = message;
  document.body.append(toast);

  requestAnimationFrame(() => {
    toast.classList.add("visible");
  });

  window.setTimeout(() => {
    toast.classList.remove("visible");
    window.setTimeout(() => toast.remove(), 220);
  }, 1800);
}

function setupLoginDemo() {
  const form = document.querySelector(".auth-form");
  const emailInput = document.querySelector("#email");
  const passwordInput = document.querySelector("#password");
  const eyeButton = document.querySelector(".eye-button");
  const oauthButtons = document.querySelectorAll(".oauth-button");

  if (!form || !emailInput || !passwordInput) {
    return;
  }

  const savedState = readDemoState();

  if (savedState.userEmail) {
    emailInput.value = savedState.userEmail;
  }

  eyeButton?.addEventListener("click", () => {
    passwordInput.type = passwordInput.type === "password" ? "text" : "password";
  });

  oauthButtons.forEach((button) => {
    button.addEventListener("click", () => {
      writeDemoState({
        authProvider: button.textContent.trim(),
        userEmail: emailInput.value.trim() || "demo@mockit.ai",
      });
      window.location.href = "./welcome.html";
    });
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    writeDemoState({
      authProvider: "Email",
      userEmail: emailInput.value.trim() || "demo@mockit.ai",
    });
    window.location.href = "./welcome.html";
  });
}

function setupCompanyDemo() {
  const nameInput = document.querySelector("#company-name");
  const industrySelect = document.querySelector("#company-industry");
  const regionSelect = document.querySelector("#company-region");
  const sizeButtons = document.querySelectorAll(".company-size-switch button");
  const nextLink = document.querySelector('.company-button.primary[href="./hiring.html"]');

  if (!nameInput || !industrySelect || !regionSelect || sizeButtons.length === 0) {
    return;
  }

  const industryOptions = [
    "Technology",
    "Fintech",
    "Healthcare",
    "E-commerce",
    "Agency",
    "Education",
  ];
  const regionOptions = [
    "North America",
    "Europe",
    "United Kingdom",
    "Middle East",
    "Remote Global",
  ];

  if (industrySelect.options.length < 2) {
    industryOptions.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      industrySelect.append(option);
    });
  }

  if (regionSelect.options.length < 2) {
    regionOptions.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      regionSelect.append(option);
    });
  }

  const savedState = readDemoState();

  if (savedState.companyName) {
    nameInput.value = savedState.companyName;
  }
  if (savedState.industry) {
    industrySelect.value = savedState.industry;
  }
  if (savedState.region) {
    regionSelect.value = savedState.region;
  }

  const applySize = (value) => {
    sizeButtons.forEach((button) => {
      button.classList.toggle("active", button.textContent.trim() === value);
    });
    writeDemoState({ companySize: value });
  };

  if (savedState.companySize) {
    applySize(savedState.companySize);
  }

  nameInput.addEventListener("input", () => {
    writeDemoState({ companyName: nameInput.value.trim() });
  });

  industrySelect.addEventListener("change", () => {
    writeDemoState({ industry: industrySelect.value });
  });

  regionSelect.addEventListener("change", () => {
    writeDemoState({ region: regionSelect.value });
  });

  sizeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      applySize(button.textContent.trim());
    });
  });

  nextLink?.addEventListener("click", () => {
    writeDemoState({
      companyName: nameInput.value.trim() || "Silk Recruitment Systems",
      industry: industrySelect.value,
      region: regionSelect.value,
    });
  });
}

function setupHiringDemo() {
  const goalCards = document.querySelectorAll(".hiring-goal-card");
  const roleButtons = document.querySelectorAll(".hiring-tags button");
  const volumeCards = document.querySelectorAll(".hiring-volume-card");
  const nextLink = document.querySelector('.company-button.primary[href="./invite.html"]');

  if (goalCards.length === 0) {
    return;
  }

  const savedState = readDemoState();

  const setGoal = (label) => {
    goalCards.forEach((card) => {
      const active = card.querySelector("h3")?.textContent.trim() === label;
      card.classList.toggle("active", active);
    });
    writeDemoState({ hiringGoal: label });
  };

  const setVolume = (label) => {
    volumeCards.forEach((card) => {
      card.classList.toggle("active", card.textContent.includes(label));
    });
    writeDemoState({ hiringVolume: label });
  };

  if (savedState.hiringGoal) {
    setGoal(savedState.hiringGoal);
  }

  if (Array.isArray(savedState.hiringRoles)) {
    roleButtons.forEach((button) => {
      button.classList.toggle("active", savedState.hiringRoles.includes(button.textContent.trim()));
    });
  }

  if (savedState.hiringVolume) {
    setVolume(savedState.hiringVolume);
  }

  goalCards.forEach((card) => {
    card.addEventListener("click", () => {
      const title = card.querySelector("h3")?.textContent.trim();
      if (title) {
        setGoal(title);
      }
    });
  });

  roleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      button.classList.toggle("active");
      const activeRoles = [...roleButtons]
        .filter((item) => item.classList.contains("active"))
        .map((item) => item.textContent.trim());
      writeDemoState({ hiringRoles: activeRoles });
    });
  });

  volumeCards.forEach((card) => {
    card.addEventListener("click", () => {
      const label = card.querySelector("strong")?.textContent.trim();
      if (label) {
        setVolume(label);
      }
    });
  });

  nextLink?.addEventListener("click", () => {
    const activeRoles = [...roleButtons]
      .filter((item) => item.classList.contains("active"))
      .map((item) => item.textContent.trim());
    writeDemoState({ hiringRoles: activeRoles });
  });
}

function setupInviteDemo() {
  const grid = document.querySelector("#invite-form-grid");
  const addButton = document.querySelector(".invite-add-person");
  const submitButton = document.querySelector(".invite-submit");

  if (!grid || !addButton || !submitButton) {
    return;
  }

  const createField = (type, placeholder, role) => {
    const field = document.createElement("div");
    field.className = "invite-field";

    if (type === "email") {
      field.innerHTML = `<input type="email" placeholder="${placeholder}" />`;
      return field;
    }

    field.innerHTML = `
      <div class="invite-select-shell">
        <select>
          <option>${role}</option>
          <option>Hiring Manager</option>
          <option>Coordinator</option>
          <option>Admin</option>
        </select>
      </div>
    `;

    return field;
  };

  addButton.addEventListener("click", () => {
    const index = grid.querySelectorAll('input[type="email"]').length + 1;
    grid.append(
      createField("email", `teammate${index}@company.com`, ""),
      createField("role", "", "Member")
    );
  });

  submitButton.addEventListener("click", () => {
    const invitees = [...grid.querySelectorAll('input[type="email"]')]
      .map((input) => input.value.trim() || input.placeholder)
      .filter(Boolean);

    writeDemoState({
      invitedTeam: invitees,
      onboardingComplete: true,
    });

    showDemoToast(`Added ${invitees.length} team member${invitees.length === 1 ? "" : "s"}`);

    window.setTimeout(() => {
      window.location.href = "./dashboard.html";
    }, 350);
  });
}

function setupVacanciesDemo() {
  const searchInput = document.querySelector("#vacancy-search");
  const statusFilter = document.querySelector("#status-filter");
  const departmentFilter = document.querySelector("#department-filter");
  const resultsCopy = document.querySelector("#vacancies-results-copy");
  const rows = [...document.querySelectorAll(".vacancies-row")];

  if (!searchInput || !statusFilter || !departmentFilter || rows.length === 0) {
    return;
  }

  rows.forEach((row) => {
    row.classList.add("is-clickable");
  });

  const statusOptions = ["All Statuses", "Active", "Draft"];
  const departmentOptions = ["All Departments", "Engineering", "Design", "Marketing"];

  const savedState = readDemoState();
  const state = {
    search: savedState.vacancySearch || "",
    status: savedState.vacancyStatusFilter || statusOptions[0],
    department: savedState.vacancyDepartmentFilter || departmentOptions[0],
  };

  const updateFilterLabel = (button, value) => {
    button.innerHTML = `${value} <b>⌄</b>`;
  };

  const applyFilters = () => {
    let visibleCount = 0;

    rows.forEach((row) => {
      const title = row.dataset.title || "";
      const department = row.dataset.department || "";
      const status = row.dataset.status || "";
      const haystack = `${title} ${department} ${status}`.toLowerCase();

      const matchesSearch = haystack.includes(state.search.toLowerCase());
      const matchesStatus = state.status === "All Statuses" || status === state.status;
      const matchesDepartment = state.department === "All Departments" || department === state.department;
      const visible = matchesSearch && matchesStatus && matchesDepartment;

      row.hidden = !visible;
      if (visible) {
        visibleCount += 1;
      }
    });

    resultsCopy.textContent = visibleCount === 0
      ? "No vacancies match the current filters"
      : `Showing ${visibleCount} matched role${visibleCount === 1 ? "" : "s"} out of 24 results`;

    writeDemoState({
      vacancySearch: state.search,
      vacancyStatusFilter: state.status,
      vacancyDepartmentFilter: state.department,
    });
  };

  searchInput.value = state.search;
  updateFilterLabel(statusFilter, state.status);
  updateFilterLabel(departmentFilter, state.department);
  applyFilters();

  searchInput.addEventListener("input", () => {
    state.search = searchInput.value.trim();
    applyFilters();
  });

  statusFilter.addEventListener("click", () => {
    const nextIndex = (statusOptions.indexOf(state.status) + 1) % statusOptions.length;
    state.status = statusOptions[nextIndex];
    updateFilterLabel(statusFilter, state.status);
    applyFilters();
  });

  departmentFilter.addEventListener("click", () => {
    const nextIndex = (departmentOptions.indexOf(state.department) + 1) % departmentOptions.length;
    state.department = departmentOptions[nextIndex];
    updateFilterLabel(departmentFilter, state.department);
    applyFilters();
  });

  rows.forEach((row) => {
    row.addEventListener("click", () => {
      writeDemoState({
        selectedVacancy: row.dataset.title,
        selectedDepartment: row.dataset.department,
        selectedCandidateName: "Alex Thompson",
        selectedCandidateRole: row.dataset.title,
      });
      window.location.href = "./candidate-overview.html";
    });
  });
}

function setupCandidateOverviewDemo() {
  const savedState = readDemoState();
  const nameHeading = document.querySelector(".candidate-headline h1");
  const roleCopy = document.querySelector(".candidate-main-copy > p");
  const tabs = document.querySelectorAll(".candidate-tabs a");
  const noteLink = document.querySelector(".candidate-note-link");

  if (!nameHeading || !roleCopy) {
    return;
  }

  if (savedState.selectedCandidateName) {
    nameHeading.textContent = savedState.selectedCandidateName;
  }

  if (savedState.selectedCandidateRole) {
    roleCopy.textContent = savedState.selectedCandidateRole;
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      writeDemoState({ candidateTab: tab.textContent.trim() });
    });
  });

  noteLink?.addEventListener("click", (event) => {
    event.preventDefault();
    writeDemoState({ noteDrafted: true });
    showDemoToast("Internal note added to candidate profile");
  });
}

function setupResumeAnalysisDemo() {
  const savedState = readDemoState();
  const title = document.querySelector(".resume-analysis-head h1, .resume-page-head h1, .resume-head h1");
  const exportLink = document.querySelector('a[href="./summary-report.html"]');
  const breadcrumb = document.querySelector(".resume-breadcrumbs a:last-of-type");
  const docName = document.querySelector(".resume-doc-card h2");
  const docRole = document.querySelector(".resume-role");
  const recommendationText = document.querySelector(".resume-recommendation p");

  if (title && savedState.selectedCandidateName) {
    title.textContent = `${savedState.selectedCandidateName} Resume Analysis`;
  }

  if (breadcrumb && savedState.selectedCandidateName && savedState.selectedCandidateRole) {
    breadcrumb.textContent = `${savedState.selectedCandidateName} - ${savedState.selectedCandidateRole}`;
  }

  if (docName && savedState.selectedCandidateName) {
    docName.textContent = savedState.selectedCandidateName;
  }

  if (docRole && savedState.selectedCandidateRole) {
    docRole.textContent = savedState.selectedCandidateRole;
  }

  if (recommendationText && savedState.selectedCandidateRole) {
    recommendationText.textContent = `Proceed to technical interview. Focus on clarifying ownership, delivery impact, and role-fit details for the ${savedState.selectedCandidateRole} position.`;
  }

  exportLink?.addEventListener("click", () => {
    writeDemoState({ reportReady: true });
  });
}

function setupLiveWorkspaceDemo() {
  const responseBox = document.querySelector(".workspace-response-box");
  const scoreValue = document.querySelector("#workspace-score-value");
  const scoreFill = document.querySelector("#workspace-score-fill");
  const nextButton = document.querySelector('.workspace-nav-button.primary[href="./summary-report.html"]');
  const timerValue = document.querySelector(".workspace-live-pill strong");

  if (!responseBox || !scoreValue || !scoreFill) {
    return;
  }

  const savedState = readDemoState();

  if (savedState.workspaceResponse) {
    responseBox.textContent = savedState.workspaceResponse;
  }

  const updateScore = () => {
    const content = responseBox.textContent.trim();
    const lengthScore = Math.min(10, Math.max(4.6, content.length / 26));
    const keywordBoost = /(trade|debt|stakeholder|document|scal|priorit|framework)/i.test(content) ? 0.7 : 0;
    const nextScore = Math.min(9.8, lengthScore + keywordBoost);
    const normalized = Math.round(nextScore * 10) / 10;

    scoreValue.innerHTML = `${normalized}<small>/10</small>`;
    scoreFill.style.width = `${normalized * 10}%`;

    writeDemoState({
      workspaceResponse: content,
      workspaceScore: normalized,
    });
  };

  responseBox.addEventListener("input", updateScore);
  responseBox.addEventListener("focus", () => {
    if (responseBox.textContent.includes("Start typing candidate response here")) {
      responseBox.textContent = "";
    }
  });

  if (timerValue) {
    let seconds = 24 * 60 + 42;
    window.setInterval(() => {
      seconds += 1;
      const mins = String(Math.floor(seconds / 60)).padStart(2, "0");
      const secs = String(seconds % 60).padStart(2, "0");
      timerValue.textContent = `${mins}:${secs}`;
    }, 1000);
  }

  updateScore();

  nextButton?.addEventListener("click", () => {
    writeDemoState({ interviewComplete: true });
  });
}

function setupSummaryDemo() {
  const savedState = readDemoState();
  const candidateName = document.querySelector(".summary-title-row h1");
  const roleCopy = document.querySelector(".summary-profile p");
  const recommendation = document.querySelector(".recommendation-card h3");

  if (candidateName && savedState.selectedCandidateName) {
    candidateName.textContent = savedState.selectedCandidateName;
  }

  if (roleCopy && savedState.selectedCandidateRole) {
    roleCopy.textContent = `${savedState.selectedCandidateRole} • San Francisco, CA`;
  }

  if (recommendation && typeof savedState.workspaceScore === "number") {
    recommendation.textContent = savedState.workspaceScore >= 8.5 ? "Strong Hire" : "Proceed with Caution";
  }
}

function setupDashboardDemo() {
  const savedState = readDemoState();
  const welcomeHeading = document.querySelector(".dashboard-head h1");
  const welcomeCopy = document.querySelector(".dashboard-head p");
  const userName = document.querySelector(".dashboard-user strong");
  const userRole = document.querySelector(".dashboard-user span");
  const vacancyCards = document.querySelectorAll(".dashboard-vacancy-card");
  const insightLink = document.querySelector('.dashboard-insight-card a[href="./invite.html"]');
  const stats = document.querySelectorAll(".dashboard-stat-card strong");

  if (welcomeHeading && savedState.companyName) {
    welcomeHeading.textContent = `Welcome back to ${savedState.companyName}.`;
  }

  if (welcomeCopy && Array.isArray(savedState.invitedTeam) && savedState.invitedTeam.length > 0) {
    welcomeCopy.textContent = `Your workspace is live, ${savedState.invitedTeam.length} teammates were invited, and the hiring flow is ready for review.`;
  }

  if (userName && savedState.userEmail) {
    userName.textContent = savedState.userEmail.split("@")[0] || userName.textContent;
  }

  if (userRole && savedState.hiringGoal) {
    userRole.textContent = savedState.hiringGoal.toUpperCase();
  }

  if (stats.length >= 4 && Array.isArray(savedState.invitedTeam)) {
    stats[0].textContent = savedState.selectedVacancy ? "25" : stats[0].textContent;
    stats[1].textContent = `${1248 + savedState.invitedTeam.length}`;
  }

  vacancyCards.forEach((card) => {
    card.classList.add("is-clickable");
    card.addEventListener("click", () => {
      const title = card.querySelector(".dashboard-vacancy-copy strong")?.textContent.trim();
      if (title) {
        writeDemoState({
          selectedVacancy: title,
          selectedCandidateName: "Alex Thompson",
          selectedCandidateRole: title,
        });
      }
      window.location.href = "./vacancies.html";
    });
  });

  insightLink?.addEventListener("click", (event) => {
    event.preventDefault();
    showDemoToast("Invitations queued for shortlisted candidates");
    window.setTimeout(() => {
      window.location.href = "./invite.html";
    }, 300);
  });
}

function setupBillingDemo() {
  const searchInput = document.querySelector('.billing-top-actions .app-search input');
  const historyRows = [...document.querySelectorAll(".billing-history-row")];
  const actionLinks = document.querySelectorAll(".billing-plan-actions a");
  const exportLink = document.querySelector(".billing-history-card .billing-card-head a");
  const downloadButtons = document.querySelectorAll(".billing-history-row button");

  if (searchInput && historyRows.length > 0) {
    searchInput.addEventListener("input", () => {
      const query = searchInput.value.trim().toLowerCase();
      historyRows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.hidden = query !== "" && !text.includes(query);
      });
    });
  }

  actionLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const label = link.textContent.trim();
      showDemoToast(`${label} opened in billing assistant`);
    });
  });

  exportLink?.addEventListener("click", (event) => {
    event.preventDefault();
    showDemoToast("Billing history exported");
  });

  downloadButtons.forEach((button) => {
    button.addEventListener("click", () => {
      showDemoToast("Invoice downloaded");
    });
  });
}

setupLoginDemo();
setupCompanyDemo();
setupHiringDemo();
setupInviteDemo();
setupDashboardDemo();
setupVacanciesDemo();
setupCandidateOverviewDemo();
setupResumeAnalysisDemo();
setupLiveWorkspaceDemo();
setupSummaryDemo();
setupBillingDemo();
