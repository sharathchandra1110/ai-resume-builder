from typing import Dict, List


def _format_resume_items(items: List[Dict[str, str]]) -> List[str]:
    lines = []
    for item in items:
        title_line = item["title"]
        if item.get("subtitle"):
            title_line = f"{title_line} | {item['subtitle']}"
        if item.get("duration"):
            title_line = f"{title_line} ({item['duration']})"

        lines.append(title_line)

        if item.get("technologies"):
            lines.append(f"Technologies: {', '.join(item['technologies'])}")

        for highlight in item.get("highlights", []):
            lines.append(f"- {highlight}")

        if item.get("description"):
            lines.append(item["description"])

        lines.append("")

    return lines


def assemble_resume(
    name: str,
    headline: str,
    summary: str,
    core_competencies: List[str],
    technical_skills: Dict[str, List[str]],
    education: str,
    projects: List[Dict[str, str]],
    experience: List[Dict[str, str]],
):
    lines = [name]

    if headline:
        lines.append(headline)

    lines.extend(["", "PROFESSIONAL SUMMARY", summary, ""])

    if core_competencies:
        lines.extend(["CORE COMPETENCIES", ", ".join(core_competencies), ""])

    if technical_skills:
        lines.append("TECHNICAL SKILLS")
        for category, skills in technical_skills.items():
            lines.append(f"{category}: {', '.join(skills)}")
        lines.append("")

    if projects:
        lines.extend(["PROJECTS", *_format_resume_items(projects)])

    if experience:
        lines.extend(["EXPERIENCE", *_format_resume_items(experience)])

    if education:
        lines.extend(["EDUCATION", education])

    return "\n".join(line for line in lines if line is not None).strip()
