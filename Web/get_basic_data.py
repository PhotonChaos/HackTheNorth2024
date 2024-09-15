# Get medication name, manufacturer and 
import requests


def get_drug_info_by_code(ndc_code):
    url = "https://api.fda.gov/drug/ndc.json?search=openfda.package_ndc=" + ndc_code + "&limit=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            drug_info = data['results'][0]
            generic_name = drug_info.get('generic_name', 'N/A')
            brand_names = drug_info.get('brand_name', 'N/A')
            product_ndc = drug_info.get('product_ndc', 'N/A')
            return {
                'name': generic_name,
                'brand_names': brand_names,
                'product_ndc': product_ndc
            }
        else:
            return {"error": "No results found for the given code."}
    else:
        return {"error": f"API request failed with status code {response.status_code}"}


ndc_code = '80777-345'  # Replace with the actual NDC code
drug_info = get_drug_info_by_code(ndc_code)
print(drug_info)
