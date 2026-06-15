import aiohttp
import asyncio
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

async def run(target_url, session: aiohttp.ClientSession):
    """
    Valkyrie Module: Asynchronous Parameter Reflection & Input Validation Audit
    """
    # Safe, generic alphanumeric token to monitor string reflection
    test_token = "valkyrie_audit_token"
    parsed_url = urlparse(target_url)
    query_params = parse_qsl(parsed_url.query)
    
    # Structure test parameters safely based on existing variables
    if not query_params:
        query_params = [('ref', test_token), ('id', test_token)]
    else:
        query_params = [(k, test_token) for k, v in query_params]

    # Reassemble the safe auditing configuration
    new_query = urlencode(query_params)
    audit_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))

    try:
        # Asynchronously verify input reflection behaviors cleanly
        async with session.get(audit_url, timeout=8, ssl=False) as response:
            if response.status == 200:
                body_content = await response.text()
                
                # Check if the text matches the tracking token exactly inside the DOM
                if test_token in body_content:
                    return {
                        "status": "Vulnerable / Alert",
                        "timestamp": "Parameter Reflection Detected",
                        "summary": f"Injected test string reflects back transparently at endpoint: {audit_url}"
                    }
    except Exception as e:
        pass

    return {
        "status": "Safe / Clean",
        "timestamp": "No Reflection",
        "summary": "Input text does not project back into the application body."
    }
  
