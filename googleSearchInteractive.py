from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

def buscar_cwpp(county, state):
    """Función para buscar CWPP para un condado y estado específicos"""
    
    consulta = f"""
I need help finding a county-wide CWPP (Community Wildfire Protection Plan) for {county} County, {state}.

CRITERIA FOR EVALUATION:
- The CWPP must be county-wide
- Must have been updated at least once
- If a plan has never been county-wide since its inception, disregard it (but make a note)
- If a plan has evolved into something different (e.g., merged with multiple counties or changed to a different structure), disregard it (but make a note)

Please search for a CWPP that meets these criteria for {county} County, {state}.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=consulta
        )
        
        print("\n" + "="*60)
        print(f"RESULTADOS PARA {county.upper()} COUNTY, {state.upper()}")
        print("="*60)
        print(response.text)
        print("="*60)
        
    except Exception as e:
        print(f"Error en la búsqueda: {e}")

def main():
    """Función principal del programa"""
    
    print("="*60)
    print("BÚSQUEDA DE CWPP (Community Wildfire Protection Plan)")
    print("="*60)
    
    while True:
        print("\n--- NUEVA BÚSQUEDA ---")
        county = input("Ingresa el nombre del condado (o 'salir' para terminar): ").strip()
        
        if county.lower() in ['salir', 'exit', 'quit']:
            print("¡Hasta luego!")
            break
        
        state = input("Ingresa el nombre del estado: ").strip()
        
        if not county or not state:
            print("Error: Debes ingresar tanto el condado como el estado.")
            continue
        
        buscar_cwpp(county, state)
        
        continuar = input("\n¿Quieres buscar otro condado? (s/n): ").strip().lower()
        if continuar not in ['s', 'si', 'sí', 'yes', 'y']:
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
