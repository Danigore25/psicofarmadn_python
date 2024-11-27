import requests

api_url = "https://api.pharmgkb.org/openapi.json"
response = requests.get(api_url)
print(response.json())

# Conseguir el ID de la variante de PharmGKB (se puede desde Bio)

var_url = "https://api.pharmgkb.org/v1/data/variant/PA166156024"
response2 = requests.get(var_url)
print(response2.json())

var_url2 = "https://api.pharmgkb.org/v1/data/variant/"
response3 = requests.get(var_url2, [("name","rs4680")])
print(response3.json())

var_url3 = "https://api.pharmgkb.org/v1/data/variant/"
response4 = requests.get(var_url2, [("name","CYP2C9*1")])
print("Respuesta: ", response4.json())

# clinic = requests.get("https://api.pharmgkb.org/v1/data/clinicalAnnotation?location.fingerprint=rs4680")
# print(clinic.json())

# variants = requests.get("https://api.pharmgkb.org/v1/data/variant/?symbol=rs4680&view=max")
# print(variants.json())

# clinical = requests.get("https://api.pharmgkb.org/v1/data/clinicalAnnotation?location.fingerprint=rs4680&view=base")
# print(clinical.json())
