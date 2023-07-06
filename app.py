from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend's origin or "*" to allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class DataTablesRequest(BaseModel):
    draw: int
    start: int
    length: int
    search: dict
    order: list
    columns: list

@app.post('/data')
async def get_data(request: Request, data_request: DataTablesRequest):
    draw = data_request.draw
    start = data_request.start
    length = data_request.length
    search_value = data_request.search['value']
    order_column_index = data_request.order[0]['column']
    order_column_name = data_request.columns[order_column_index]['data']
    order_direction = data_request.order[0]['dir']


    response = requests.get('https://reqres.in/api/users')
    if response.status_code != 200:
        return JSONResponse(content={'error': 'Failed to fetch data from API'})

    api_data = response.json().get('data', [])

    # Apply filtering/searching
    filtered_data = []
    if search_value:
        for item in api_data:
            if (
                str(item['id']).lower().startswith(search_value.lower()) or
                item['email'].lower().startswith(search_value.lower()) or
                item['first_name'].lower().startswith(search_value.lower()) or
                item['last_name'].lower().startswith(search_value.lower())
            ):
                filtered_data.append(item)
    else:
        filtered_data = api_data

    # Apply ordering
    if order_direction == 'asc':
        filtered_data.sort(key=lambda x: x[order_column_name])
    else:
        filtered_data.sort(key=lambda x: x[order_column_name], reverse=True)

    # Prepare the response
    response = {
        'draw': draw,
        'recordsTotal': len(api_data),
        'recordsFiltered': len(filtered_data),
        'data': filtered_data[start:start + length]
    }
    print(response)
    return response
