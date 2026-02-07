def build_structured_prompt(topic, domain, output_type, level, sections):

    depth_instructions = """
Interpret Complexity Level as:
- Basic → Simple explanation.
- Medium → Balanced structured clarity.
- High → Technical depth with implementation detail.
- Advanced → Architecture-level explanation with strategic insight.
"""

    section_text = ""
    for section in sections:
        section_text += f"\n{section}"

    prompt = f"""
You are Structify — a structured execution engine.

Generate a professional structured output.

Domain: {domain}
Output Type: {output_type}
Topic: {topic}
Complexity Level: {level}

{depth_instructions}

STRICT RULES:
- Follow the exact section order below.
- Use section names as headings.
- Do NOT return JSON.
- Do NOT use code blocks.
- Format cleanly with clear section headings.

Sections:
{section_text}
"""

    return prompt
