## Python helpers for Azure Functions

### Modules

#### elastic_logging
Wrapper for logging handler and APM event tracing

##### Functions
###### Log
 For use as a decorator at Azure Function entry point. 
Requires the setting of the environment variables ```ELASTIC_APM_SERVICE_NAME``` and ```ELASTIC_APM_SERVER_URL```
as defined in APM documentation https://www.elastic.co/guide/en/apm/agent/python/current/api.html

Example usage

```
import logging
import azure.functions as func
from azurefunctionhelpers.elastic_logging import log

@log('transaction_category', 'transaction_name')
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Here is my message')
    raise Exception('Unhandled exceptions will log')
    
    return func.HttpResponse(
         "Ok",
         status_code=200
    )

```

