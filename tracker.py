import json
import time
import requests



# Initial 
grid_old = [20000, 10000, 5000, 3000, 1000, 500, 50, 1]
grid = [x * 10**9 for x in grid_old]
result = [0,0,0,0,0,0,0,0]
base = 1000000000
page_size = 1000
endPoint = 6
block = 0



def apiRequest(page, page_size):
	url = "https://api.covalenthq.com/v1/56/tokens/TOKEN_ADDRESS/token_holders/?page-number={}&page-size={}&key=YOUR_KEY".format(page, page_size)
	counter = 0
	status = 0
	while status != 200:
		if counter == 5: break
		response = requests.get(url)
		status = response.status_code
		counter += 1
		time.sleep(0.5)
	return response.json()



def dataBasketing(items, grid, result, i):
	for item in items:
		case = int(int(item['balance'])/1000000000)
		if grid[i] < case:
			result[i] += 1
		elif grid[i+1] < case:
			result[i+1] += 1
			i += 1
		elif grid[i+2] < case:
			result[i+2] += 1
			i += 2
		elif grid[i+3] < case:
			result[i+3] += 1
			i += 3
		else:
			result[i+4] += 1
			i += 4
	return result



# Cycle
page = 0
i = 0
while result[endPoint] == 0:
	data = apiRequest(page, page_size)
	items = data["data"]["items"]
	block = items[0]["block_height"]
	result = dataBasketing(items, grid, result, i)
	page += 1



# Save Data
with open('tracker.json', 'w') as f:
	result = dict(zip(grid_old, result))
	json.dump(result, f)


