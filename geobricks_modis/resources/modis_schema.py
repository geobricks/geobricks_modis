schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "MODIS",
    "description": "MODerate resolution Imaging Spectroradiometer.",
    "definitions": {
        "href": {
            "title": "Endpoint",
            "description": "Relative path to the service.",
            "type": "string",
            "default": "/"
        },
        "method": {
            "title": "HTTP Method",
            "description": "Method type to invoke the service.",
            "type": "string",
            "enum": [
                "GET",
                "POST",
                "PUT",
                "DELETE"
            ]
        },
        "code": {
            "title": "Code",
            "description": "Encoded value.",
            "type": "string"
        },
        "label": {
            "title": "Label",
            "description": "Human-readable label.",
            "type": "string"
        },
        "code_label": {
            "type": "object",
            "properties": {
                "code": {
                    "$ref": "#/definitions/code"
                },
                "label": {
                    "$ref": "#/definitions/label"
                }
            }
        }
    },
    "properties": {
        "service_type": {
            "type": "string",
            "title": "Type",
            "description": "REST service type.",
            "enum": "DATASOURCE",
            "default": "DATASOURCE"
        }
    }
}
