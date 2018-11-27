from esipy import EsiApp
from esipy import EsiClient

esi_app = EsiApp()
app = esi_app.get_latest_swagger

# basic client, for public endpoints only
client = EsiClient(
    retry_requests=True,  # set to retry on http 5xx error (default False)
    headers={'User-Agent': 'Doctrines.space DEVELOPMENT BUILD'},
    raw_body_only=False,  # default False, set to True to never parse response and only return raw JSON string content.
)
