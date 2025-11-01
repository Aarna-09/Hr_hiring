# small helper: generate dummy resumes for testing


def make_dummy_resume(name, skills, experience_years, extra=''):
    lines = [f"{name}\n", f"Experience: {experience_years} years\n", "Skills: " + ', '.join(skills) + '\n', extra]
    return '\n'.join(lines)