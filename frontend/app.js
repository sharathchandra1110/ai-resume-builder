const entryTemplate = document.getElementById("entry-template");
const projectsList = document.getElementById("projects-list");
const experienceList = document.getElementById("experience-list");
const templateSelect = document.getElementById("template-select");
const statusBanner = document.getElementById("status-banner");
const resumeFrame = document.getElementById("resume-frame");
const previewTemplateLabel = document.getElementById("preview-template-label");

const summaryPreview = document.getElementById("summary-preview");
const matchedSkillsContainer = document.getElementById("matched-skills");
const missingSkillsContainer = document.getElementById("missing-skills");
const coreCompetenciesContainer = document.getElementById("core-competencies-preview");
const technicalSkillsPreview = document.getElementById("technical-skills-preview");

const resumeScore = document.getElementById("resume-score");
const matchedSkillCount = document.getElementById("matched-skill-count");
const missingSkillCount = document.getElementById("missing-skill-count");

const demoData = {
    profile: {
        name: "Sharath Chandra Karupakala",
        headline: "Java Backend Developer",
        email: "sharath@example.com",
        phone: "+91 98765 43210",
        location: "Hyderabad, India",
        education: "B.Tech in Computer Science and Engineering\nJNTU - 2025",
        skills: [
            "Java",
            "Spring Boot",
            "REST APIs",
            "MySQL",
            "PostgreSQL",
            "Git",
            "Docker",
            "JWT",
            "OOP",
            "Data Structures & Algorithms"
        ],
        core_competencies: [
            "Backend Development",
            "API Design",
            "Authentication",
            "Database Modeling",
            "Problem Solving"
        ],
        certifications: [
            "Java Fundamentals",
            "REST API Design"
        ],
        links: {
            GitHub: "https://github.com/sharath",
            LinkedIn: "https://linkedin.com/in/sharath",
            Portfolio: "https://portfolio.example.com"
        },
        projects: [
            {
                title: "Inventory Management API",
                subtitle: "Personal Project",
                duration: "2025",
                description: "Developed a backend service for product tracking, secure authentication, and order lifecycle handling.",
                technologies: ["Java", "Spring Boot", "MySQL", "JWT"],
                highlights: [
                    "Built CRUD REST endpoints for inventory and order management",
                    "Added JWT-based authentication and role-based route protection",
                    "Structured SQL tables to support stock, user, and order workflows"
                ],
                link: "https://github.com/sharath/inventory-api"
            }
        ],
        experience: [
            {
                title: "Backend Developer Intern",
                subtitle: "Academic Innovation Lab",
                duration: "2024",
                description: "Supported backend feature development and API integration for student-focused tools.",
                technologies: ["Java", "REST APIs", "Git"],
                highlights: [
                    "Implemented API endpoints and request validation",
                    "Collaborated on bug fixes and backend testing",
                    "Improved code readability and modular service structure"
                ],
                link: ""
            }
        ]
    },
    jobDescription: {
        target_title: "Java Backend Developer",
        company_name: "Example Tech",
        jd_text: "We are hiring a Java Backend Developer with experience in Java, Spring Boot, REST APIs, MySQL or PostgreSQL, Git, Docker, JWT, and strong data structures and algorithms skills. Exposure to AWS is a plus."
    }
};

function parseCommaSeparated(value) {
    return value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
}

function parseMultiLine(value) {
    return value
        .split("\n")
        .map((item) => item.trim())
        .filter(Boolean);
}

function buildLinks() {
    const links = {};
    const github = document.getElementById("github_url").value.trim();
    const linkedin = document.getElementById("linkedin_url").value.trim();
    const portfolio = document.getElementById("portfolio_url").value.trim();

    if (github) {
        links.GitHub = github;
    }
    if (linkedin) {
        links.LinkedIn = linkedin;
    }
    if (portfolio) {
        links.Portfolio = portfolio;
    }

    return links;
}

function setStatus(message, tone = "neutral") {
    statusBanner.textContent = message;
    statusBanner.classList.remove("status-success", "status-error");

    if (tone === "success") {
        statusBanner.classList.add("status-success");
    }
    if (tone === "error") {
        statusBanner.classList.add("status-error");
    }
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        ...options
    });

    const contentType = response.headers.get("content-type") || "";
    const payload = contentType.includes("application/json")
        ? await response.json()
        : await response.text();

    if (!response.ok) {
        const detail = typeof payload === "object" && payload !== null ? payload.detail || JSON.stringify(payload) : payload;
        throw new Error(detail || "Request failed");
    }

    return payload;
}

function createEntryCard(kind, data = {}) {
    const fragment = entryTemplate.content.cloneNode(true);
    const card = fragment.querySelector(".entry-card");
    const label = kind === "project" ? "Project Entry" : "Experience Entry";

    card.dataset.kind = kind;
    card.querySelector(".entry-badge").textContent = kind === "project" ? "Project" : "Experience";
    card.querySelector(".entry-title-label").textContent = label;

    card.querySelector("[data-field='title']").value = data.title || "";
    card.querySelector("[data-field='subtitle']").value = data.subtitle || "";
    card.querySelector("[data-field='duration']").value = data.duration || "";
    card.querySelector("[data-field='description']").value = data.description || "";
    card.querySelector("[data-field='technologies']").value = (data.technologies || []).join(", ");
    card.querySelector("[data-field='highlights']").value = (data.highlights || []).join("\n");
    card.querySelector("[data-field='link']").value = data.link || "";

    card.querySelector(".remove-entry").addEventListener("click", () => {
        card.remove();
    });

    return card;
}

function collectEntryData(listElement) {
    return Array.from(listElement.querySelectorAll(".entry-card")).map((card) => ({
        title: card.querySelector("[data-field='title']").value.trim(),
        subtitle: card.querySelector("[data-field='subtitle']").value.trim(),
        duration: card.querySelector("[data-field='duration']").value.trim(),
        description: card.querySelector("[data-field='description']").value.trim(),
        technologies: parseCommaSeparated(card.querySelector("[data-field='technologies']").value),
        highlights: parseMultiLine(card.querySelector("[data-field='highlights']").value),
        link: card.querySelector("[data-field='link']").value.trim()
    })).filter((item) => item.title || item.description || item.highlights.length);
}

function collectProfilePayload() {
    return {
        name: document.getElementById("name").value.trim(),
        headline: document.getElementById("headline").value.trim(),
        email: document.getElementById("email").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        location: document.getElementById("location").value.trim(),
        education: document.getElementById("education").value.trim(),
        skills: parseCommaSeparated(document.getElementById("skills").value),
        core_competencies: parseCommaSeparated(document.getElementById("core_competencies").value),
        certifications: parseCommaSeparated(document.getElementById("certifications").value),
        links: buildLinks(),
        projects: collectEntryData(projectsList),
        experience: collectEntryData(experienceList)
    };
}

function collectJobDescriptionPayload() {
    return {
        target_title: document.getElementById("target_title").value.trim(),
        company_name: document.getElementById("company_name").value.trim(),
        jd_text: document.getElementById("jd_text").value.trim()
    };
}

function fillEntryList(listElement, kind, items = []) {
    listElement.innerHTML = "";
    if (!items.length) {
        listElement.appendChild(createEntryCard(kind));
        return;
    }

    items.forEach((item) => {
        listElement.appendChild(createEntryCard(kind, item));
    });
}

function fillProfileForm(profile) {
    document.getElementById("name").value = profile.name || "";
    document.getElementById("headline").value = profile.headline || "";
    document.getElementById("email").value = profile.email || "";
    document.getElementById("phone").value = profile.phone || "";
    document.getElementById("location").value = profile.location || "";
    document.getElementById("education").value = profile.education || "";
    document.getElementById("skills").value = (profile.skills || []).join(", ");
    document.getElementById("core_competencies").value = (profile.core_competencies || []).join(", ");
    document.getElementById("certifications").value = (profile.certifications || []).join(", ");
    document.getElementById("github_url").value = profile.links?.GitHub || "";
    document.getElementById("linkedin_url").value = profile.links?.LinkedIn || "";
    document.getElementById("portfolio_url").value = profile.links?.Portfolio || "";

    fillEntryList(projectsList, "project", profile.projects || []);
    fillEntryList(experienceList, "experience", profile.experience || []);
}

function fillJobDescriptionForm(jobDescription) {
    document.getElementById("target_title").value = jobDescription.target_title || "";
    document.getElementById("company_name").value = jobDescription.company_name || "";
    document.getElementById("jd_text").value = jobDescription.jd_text || "";
}

function renderChipRow(container, items, tone = "normal") {
    container.classList.remove("empty-chip-row");
    container.innerHTML = "";

    if (!items || !items.length) {
        container.classList.add("empty-chip-row");
        return;
    }

    items.forEach((item) => {
        const chip = document.createElement("span");
        chip.className = tone === "muted" ? "chip chip-muted" : "chip";
        chip.textContent = item;
        container.appendChild(chip);
    });
}

function renderTechnicalSkills(groups) {
    technicalSkillsPreview.classList.remove("empty-list-state");
    technicalSkillsPreview.innerHTML = "";

    const entries = Object.entries(groups || {});
    if (!entries.length) {
        technicalSkillsPreview.classList.add("empty-list-state");
        technicalSkillsPreview.textContent = "Technical groups will appear here after preview generation.";
        return;
    }

    entries.forEach(([category, skills]) => {
        const item = document.createElement("div");
        item.className = "skill-summary-item";
        item.innerHTML = `<strong>${category}</strong><span>${skills.join(", ")}</span>`;
        technicalSkillsPreview.appendChild(item);
    });
}

async function loadTemplates() {
    const templatePayload = await requestJson("/templates");
    const templates = templatePayload.available_templates || [];

    templateSelect.innerHTML = "";
    templates.forEach((template) => {
        const option = document.createElement("option");
        option.value = template.id;
        option.textContent = template.name;
        templateSelect.appendChild(option);
    });

    if (templatePayload.default_template) {
        templateSelect.value = templatePayload.default_template;
    }

    previewTemplateLabel.textContent = templateSelect.selectedOptions[0]?.textContent || "No template selected";
}

async function loadExistingState() {
    try {
        const profile = await requestJson("/profile");
        fillProfileForm(profile);
    } catch (error) {
        fillEntryList(projectsList, "project");
        fillEntryList(experienceList, "experience");
    }

    try {
        const jobDescription = await requestJson("/job-description");
        fillJobDescriptionForm(jobDescription);
    } catch (error) {
        document.getElementById("jd_text").value = "";
    }
}

async function saveProfile() {
    const payload = collectProfilePayload();
    await requestJson("/profile", {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

async function saveJobDescription() {
    const payload = collectJobDescriptionPayload();
    await requestJson("/job-description", {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

async function refreshPreview() {
    const templateId = templateSelect.value;
    previewTemplateLabel.textContent = templateSelect.selectedOptions[0]?.textContent || templateId;

    const [fitAnalysis, previewData, htmlPreview] = await Promise.all([
        requestJson("/analysis/fit"),
        requestJson(`/resume/preview?template_id=${encodeURIComponent(templateId)}`),
        requestJson(`/resume/html?template_id=${encodeURIComponent(templateId)}`)
    ]);

    resumeScore.textContent = `${fitAnalysis.resume_score}%`;
    matchedSkillCount.textContent = String((fitAnalysis.matched_skills || []).length);
    missingSkillCount.textContent = String((fitAnalysis.missing_skills || []).length);
    summaryPreview.textContent = previewData.professional_summary || "No summary available.";

    renderChipRow(matchedSkillsContainer, fitAnalysis.matched_skills || []);
    renderChipRow(missingSkillsContainer, fitAnalysis.missing_skills || [], "muted");
    renderChipRow(coreCompetenciesContainer, previewData.core_competencies || []);
    renderTechnicalSkills(previewData.technical_skills || {});

    resumeFrame.srcdoc = htmlPreview.html_resume || "<p>No resume preview available.</p>";
}

async function generatePreviewFlow() {
    try {
        setStatus("Saving profile and job description, then generating the resume preview...");
        await saveProfile();
        await saveJobDescription();
        await refreshPreview();
        setStatus("Preview generated successfully. Your frontend is connected to the backend flow.", "success");
    } catch (error) {
        setStatus(error.message, "error");
    }
}

function loadDemoData() {
    fillProfileForm(demoData.profile);
    fillJobDescriptionForm(demoData.jobDescription);
    setStatus("Demo data loaded. Generate a preview to verify the full frontend path.", "success");
}

async function resetBackendState() {
    try {
        await requestJson("/state/reset", { method: "DELETE" });
        resumeFrame.srcdoc = "";
        summaryPreview.textContent = "Save profile and job details to see the generated summary.";
        resumeScore.textContent = "--";
        matchedSkillCount.textContent = "0";
        missingSkillCount.textContent = "0";
        renderChipRow(matchedSkillsContainer, []);
        renderChipRow(missingSkillsContainer, []);
        renderChipRow(coreCompetenciesContainer, []);
        renderTechnicalSkills({});
        setStatus("Backend state cleared. Your local form inputs are still available in the page.", "success");
    } catch (error) {
        setStatus(error.message, "error");
    }
}

function openHtmlView() {
    const templateId = templateSelect.value;
    window.open(`/resume/view?template_id=${encodeURIComponent(templateId)}`, "_blank", "noopener");
}

function downloadPdf() {
    const templateId = templateSelect.value;
    window.open(`/resume/pdf?template_id=${encodeURIComponent(templateId)}`, "_blank", "noopener");
}

document.getElementById("add-project").addEventListener("click", () => {
    projectsList.appendChild(createEntryCard("project"));
});

document.getElementById("add-experience").addEventListener("click", () => {
    experienceList.appendChild(createEntryCard("experience"));
});

document.getElementById("save-profile").addEventListener("click", async () => {
    try {
        await saveProfile();
        setStatus("Profile saved successfully.", "success");
    } catch (error) {
        setStatus(error.message, "error");
    }
});

document.getElementById("save-job-description").addEventListener("click", async () => {
    try {
        await saveJobDescription();
        setStatus("Job description saved successfully.", "success");
    } catch (error) {
        setStatus(error.message, "error");
    }
});

document.getElementById("generate-preview").addEventListener("click", generatePreviewFlow);
document.getElementById("load-demo").addEventListener("click", loadDemoData);
document.getElementById("open-html-view").addEventListener("click", openHtmlView);
document.getElementById("download-pdf").addEventListener("click", downloadPdf);
document.getElementById("reset-state").addEventListener("click", resetBackendState);

templateSelect.addEventListener("change", async () => {
    previewTemplateLabel.textContent = templateSelect.selectedOptions[0]?.textContent || templateSelect.value;

    try {
        await refreshPreview();
        setStatus("Template switched and preview refreshed.", "success");
    } catch (error) {
        setStatus("Template updated. Generate a preview after saving your data if needed.");
    }
});

window.addEventListener("DOMContentLoaded", async () => {
    try {
        await loadTemplates();
        await loadExistingState();
        await refreshPreview();
        setStatus("Existing state loaded and preview refreshed.", "success");
    } catch (error) {
        setStatus("Frontend connected. Save a profile and a job description to generate a preview.");
    }
});
