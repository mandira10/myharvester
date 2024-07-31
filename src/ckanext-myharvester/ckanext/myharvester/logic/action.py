import ckan.plugins.toolkit as tk
import ckanext.myharvester.logic.schema as schema


@tk.side_effect_free
def myharvester_get_sum(context, data_dict):
    tk.check_access(
        "myharvester_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.myharvester_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'myharvester_get_sum': myharvester_get_sum,
    }
