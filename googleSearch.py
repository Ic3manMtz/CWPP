from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

# Consulta formateada para mejor legibilidad
consulta = """
I need help finding a county-wide CWPP (Community Wildfire Protection Plan) for Atlantic County, New Jersey.

CRITERIA FOR EVALUATION:
- The CWPP must be county-wide
- Must have been updated at least once
- If a plan has never been county-wide since its inception, disregard it (but make a note)
- If a plan has evolved into something different (e.g., merged with multiple counties or changed to a different structure), disregard it (but make a note)

Please search for a CWPP that meets these criteria for Atlantic County, New Jersey.
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=consulta
)

print(response.text)
