

private_param_mapping = {
    "climate_zones": ("climate_zones_public", "climate_zones_private"),
    "coefficients": ("coefficients_public", "coefficients_private"),
    "hdd": ("hdd_public", "hdd_private")
    }


def get_parameters(is_private, params, param_key):
    val = private_param_mapping[param_key]
    filename = val[0]
    if is_private:
        filename = val[1]
    return params.__dict__[filename]
