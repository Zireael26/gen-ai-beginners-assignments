import requests
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
MS_LEARN_API_BASE_URL = "https://learn.microsoft.com/api/catalog/"

tools = [
    {
        "type": "function",
        "name": "get_course_recommendations",
        "description": "Fetch course recommendations from Microsoft Learn Catalog based on user role, level, and product.",
        "parameters": {
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "description": "The user's role (e.g., 'developer', 'data scientist').",
                },
                "level": {
                    "type": "string",
                    "description": "The user's proficiency level (e.g., 'beginner', 'intermediate', 'advanced').",
                },
                "additional_params": {
                    "type": "object",
                    "description": "Additional parameters for filtering recommendations.",
                    "properties": {
                        "locale": {"type": "string"},
                        "type": {"type": "string" , "enum": ["modules", "units", "learningPaths", "appliedSkills", "certifications", "mergedCertifications", "exams", "courses", "levels", "roles", "products", "subjects"]},
                        "subject": {"type": "string"}
                    }
                },
            },
            "required": ["role", "level"],
            "additionalProperties": False
        },
        "strict": False,
    }
]

def get_course_recommendations(role: str, level: str, additional_params: dict) -> dict:
    """
    Fetch course recommendations from Microsoft Learn Catalog based on user role, level, and product.

    Args:
        role (str): The user's role (e.g., 'developer', 'data scientist').
        level (str): The user's proficiency level (e.g., 'beginner', 'intermediate', 'advanced').
        additional_params (dict): Additional parameters for filtering recommendations.
        additional_params shall always have strings, or lists of strings and may include:
            - locale	A single, valid locale code from the supported list of locales. The returned metadata will be in the requested locale if available. If this parameter isn't supplied, the en-us response will be returned.	string	No	?locale=en-us
            - type	A comma-separated list of one or more of the top-level content or taxonomies objects we currently provide in the response to return. Supported values are: modules, units, learningPaths, appliedSkills, certifications, mergedCertifications, exams, courses, levels, roles, products, subjects.	string	No	?type=modules,learningPaths
            - subject	A comma-separated list of one or more of the roles we currently have available (full list is in the subjects object of the API response). The API doesn't support subject hierarchy, so add every subject to the list you want to include in your query.	string	No	?subject=cloud-computing
    """
    params = {
        "role": role,
        "level": level,
    }
    if additional_params:
        params.update({k: v for k, v in additional_params.items() if k not in ["role", "level"]})

    response = requests.get(f"{MS_LEARN_API_BASE_URL}", params=params)
    response.raise_for_status()

    return response.json()

def main():
    openai = OpenAI()

    user_desc = input("Describe your role, level, and any specific domain you're interested in: ")
    input_list = [
        {"role": "system", "content": "You are an expert tutor who provides personalized learning paths. You provide MS learn course recommendations based on user persona, and include as many course details as possible, including but not limited to course title, course URL, short description, prerequisites, learning objectives, and estimated completion times."},
        {"role": "user", "content": f"I want to gain some new skills and need recommendations for learning paths and courses. Here are my details: {user_desc}"}
    ]
    response = openai.responses.create(
        model="gpt-5-nano",
        input=input_list,
        reasoning={"effort": "low"},
        service_tier="flex",
        tools=tools,
        tool_choice="auto",
    )

    function_calls = []
    for out in response.output:
        if hasattr(out, "to_dict"):
            serialized = out.to_dict()
        else:
            # Fallback generic serialization
            serialized = {
                "type": getattr(out, "type", "assistant"),
                "role": getattr(out, "role", "assistant"),
                "content": getattr(out, "content", getattr(out, "text", str(out)))
            }
        input_list.append(serialized)

        # Collect any function call items so we can execute them and append results
        if getattr(out, "type", "") == "function_call":
            function_calls.append(out)

    # Execute captured function calls and append their outputs (must come after adding the function_call item)
    for tool_call in function_calls:
        # tool_call.arguments is a JSON string in the SDK
        params = json.loads(tool_call.arguments)
        if tool_call.name == "get_course_recommendations":
            recommendations = get_course_recommendations(**params)
            # Append as a function_call_output with matching call_id
            input_list.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(recommendations)
            })

    final_response = openai.responses.create(
        model="gpt-5-nano",
        input=input_list,
        service_tier="flex",
        reasoning={"effort": "low"},
        stream=True
    )

    # print("Final response with recommendations: ", final_response.output_text)

    print()
    for event in final_response:
        if event.type == 'response.output_text.delta':
            print(event.delta, end='', flush=True)

if __name__ == "__main__":
    main()