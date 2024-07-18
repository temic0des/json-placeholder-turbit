from unittest.mock import patch, Mock
from app.utils.api_request import APIRequest

posts = [
    {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
    },
    {
        "userId": 1,
        "id": 2,
        "title": "qui est esse",
        "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla",
    },
]


def test_get_data_success():

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = posts
    mock_response.raise_for_status.return_value = Mock()

    with patch('requests.get', return_value=mock_response):
        client = APIRequest(url='https://jsonplaceholder.typicode.com/posts')
        result = client.get_data()

    assert result == posts
    assert result[0]["id"] == posts[0]["id"]
