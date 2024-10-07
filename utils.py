import aiohttp


async def create_note(database_id, notion_token, note):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    json_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": note}}]},
            "TYPE": {"select": {"name": "Inbox"}}
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                url, json=json_data, headers=headers
        ) as response:
            return response.status == 200
