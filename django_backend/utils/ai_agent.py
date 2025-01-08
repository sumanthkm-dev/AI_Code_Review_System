from groq import Groq

key = "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"


def analyse_code_with_llm(file_content, file_name):
    prompt = f"""
    Analyze the following code for:
    - Code style and formatting issues
    - Potential bugs or errors
    - Performance improvements
    - Best practices

    File: {file_name}
    Content:
    {file_content}

    Provide a detailed JSON output with the structure:
    {{
        "issues": [
            {{
                "type": "<style|bug|performance|best_practice>",
                "line": <line_number>,
                "description": "<description>",
                "suggestion": "<suggestion>"
            }}
        ]
    }}
    ``json
    """

    client = Groq(api_key=key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        top_p=1,
    )
    print(completion.choices[0].message.content)
