import logging

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        credential = DefaultAzureCredential()

        # Retrieve subscription ID from environment variable.
        subscription_id = "93fab5d6-7007-47d3-9113-21530dd01815"

        # Obtain the management object for resources.
        resource_client = ResourceManagementClient(credential, subscription_id)
        # %%
        # Provision the resource group.
        rg_result = resource_client.resource_groups.create_or_update(
            "Poc_ResorceGroup4", {"location": "eastus"}
        )

        print(
            f"Provisioned resource group {rg_result.name} in \
                the {rg_result.location} region"
        )
    except Exception as err:
        return func.HttpResponse(f"Hello, {err}. This HTTP triggered function ERROR.")

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
