import requests

result = requests.get('https://api.ambeedata.com/latest/pollen/by-lat-lng?lat=37.54068&lng=-77.43367',
             headers = {"x-api-key": "4fdc231b972e03b1df86d489299f2c39c62375be477304012f912fae0039a3a8", "Content-type": "application/json"}).content
print('Grass Pollen Count: ' + str(eval(result)['data'][0]['Count']['grass_pollen']))
print('Tree Pollen Count: ' + str(eval(result)['data'][0]['Count']['tree_pollen']))
print('Weed Pollen Count: ' + str(eval(result)['data'][0]['Count']['weed_pollen']))
print('Grass Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['grass_pollen']))
print('Tree Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['tree_pollen']))
print('Weed Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['weed_pollen']))

[{
    'Count': {'grass_pollen': 35, 'tree_pollen': 0, 'weed_pollen': 88}, 
  'Risk': {'grass_pollen': 'Moderate', 'tree_pollen': 'Low', 'weed_pollen': 'High'}, 
  'updatedAt': '2023-07-12T23:11:31.000Z'}]