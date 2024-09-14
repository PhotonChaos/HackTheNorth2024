import requests

def get_drug_info_by_code(ndc_code):
    url = f"https://api.fda.gov/drug/ndc.json"
    params = {
        'search': f"openfda.package_ndc=:{ndc_code}",
        'limit': 1  # limit to 1 result
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            drug_info = data['results'][0]
            name = drug_info.get('generic_name', 'N/A')
            manufacturer_name = drug_info.get('labeler_name', 'N/A')
            active_ingredients = drug_info.get('active_ingredients', 'N/A')
            return {
                'name': name,
                'manufacturer_name': manufacturer_name,
                'active_ingredients': active_ingredients
            }
        else:
            return {"error": "No results found for the given code."}
    else:
        return {"error": f"API request failed with status code {response.status_code}"}

ndc_code = '5914-8038-13'  # Replace with the actual NDC code
drug_info = get_drug_info_by_code(ndc_code)
print(drug_info)
