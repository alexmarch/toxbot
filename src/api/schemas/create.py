create_schema = {
    "type" : "object",
    "properties" : {
        "name" : {"type" : "string"},
        "api_admin_endpoint": {"type": "string" },
        "debug": {"type": "number"},
        "use_ssl": {"type": "number"},
        "proxy_port": {"type": "number"},
        "proxy_host": {"type": "string"},
        "welcome_message": {"type": "string"}
    },
    "required": ["name", "api_admin_endpoint"]
}