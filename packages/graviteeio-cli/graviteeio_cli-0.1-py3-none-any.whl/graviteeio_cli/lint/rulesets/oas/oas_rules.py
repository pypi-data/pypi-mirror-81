from graviteeio_cli.lint.types.enums import DiagLevel

oas_rules = {
    "oas2-schema": {
        "description": "Validate structure of OpenAPI v2 specification.",
        "message": "{{error}}.",
        "formats": ["oas2"],
        "level": DiagLevel.Error,
        "function": "oasDocumentSchema",
        "functionOption": {
            "schema": "oas/schemas/schema_oas2.json"
        }
    }
}
