import src.decorate_response
from flask import current_app
from src.variables import app
from src.endpoints import (
    main_endpoint,
    save_via_api,
    get_lang,
    view_product,
    buy_product,
    query_params
)

if __name__ == "__main__":
    app.run(host='10.100.100.100', port=8000)
