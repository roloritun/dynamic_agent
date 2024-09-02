import json
from urllib.parse import urlparse
from utils import Llm, remove_special_characters
from database import API
from sqlalchemy.orm import Session
from langchain_community.utilities import Requests
from langchain_community.agent_toolkits import NLAToolkit
from langchain_community.utilities.openapi import OpenAPISpec



llm = Llm.get_llm()


def create_api_tools(session: Session):

    api_metadata_list = session.query(API).all()
    tools = []

    for api in api_metadata_list:
        # Fetch the OpenAPI spec (either remote or local or text in database)
        # Handle different auth types: apikey, oauth
        if api.auth_type == "bearer":
            # Directly use the API key
            requests = Requests(headers={"Authorization": f"Bearer {api.api_key}"})
            toolkit = from_llm_and_url_or_spec_or_text(requests=requests, api=api)
        elif api.auth_type == "apikey":
            headers = {"x-api-key": f"{api.api_key}"}
            if api.custom_headers:
                custom_headers = json.loads(api.custom_headers.replace("'", '"'))
                headers = {**headers, **custom_headers}
            requests =get_request(headers=headers, url_params=api.url_params)
            toolkit = from_llm_and_url_or_spec_or_text(requests=requests, api=api)

        elif api.auth_type == "oauth2":
            from requests_oauthlib import OAuth2Session

            def get_oauth2_token():
                client = OAuth2Session(client_id=api.client_id)
                token = client.fetch_token(
                    token_url=api.oauth_token_url,
                    client_id=api.client_id,
                    client_secret=api.client_secret,
                )
                return token["access_token"]

            # Get OAuth2 token and dynamically update headers
            oauth2_token = get_oauth2_token()
            headers={"Authorization": f"Bearer {oauth2_token}"}
            if api.custom_headers:
                custom_headers = json.loads(api.custom_headers.replace("'", '"'))
                headers = {**headers, **custom_headers}
            requests = get_request(headers=headers, url_params=api.url_params)
            toolkit = from_llm_and_url_or_spec_or_text(requests=requests, api=api)

        else:
            headers={}
            if api.custom_headers:
                custom_headers = json.loads(api.custom_headers.replace("'", '"'))
                headers = {**headers, **custom_headers}
            requests = get_request(headers=headers, url_params=api.url_params)
            toolkit = from_llm_and_url_or_spec_or_text(requests=requests, api=api)

        api_tools = toolkit.get_tools()
        for a in api_tools:
            #a.name = remove_special_characters(a.name)
            print(a.name)
            print(a.description)
            print(a.args_schema)
        tools.extend(toolkit.get_tools())
    return tools


def from_llm_and_url_or_spec_or_text(
    requests: Requests,
    api: API,
) -> NLAToolkit:
    
    if api.spec_url:
        parsed_url = urlparse(api.spec_url)

        if parsed_url.scheme in ["http", "https"]:
            toolkit = NLAToolkit.from_llm_and_url(
                llm=llm,
                open_api_url=api.spec_url,
                requests=requests,
                allow_dangerous_requests=True,
                verbose=True,
            )
            return toolkit
        elif parsed_url.scheme == "file" or parsed_url.scheme == "":
            file_path = parsed_url.path
            spec = OpenAPISpec.from_file(file_path)
            toolkit = NLAToolkit.from_llm_and_spec(
                llm=llm,
                spec=spec,
                requests=requests,
                allow_dangerous_requests=True,
                verbose=True,
            )
            return toolkit
    else:
        toolkit = NLAToolkit.from_llm_and_spec(
                llm=llm,
                spec= OpenAPISpec.from_text(api.file_content),
                requests=requests,
                allow_dangerous_requests=True,
                verbose=True,
            )
        return toolkit

def get_request(headers: dict, url_params)->Requests:
    # if url_params:
    #     url_params = json.loads(url_params.replace("'", '"'))
    #     return Requests(headers=headers, for k,v in url_params['key'])
    # else:
    return Requests(headers=headers)
