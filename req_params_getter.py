from flask import request


class ReqParamsGetter:
    @staticmethod
    def get_params(key, default=None):
        value = request.args.get(key)
        if value is not None:
            return value

        value = request.form.get(key)
        if value is not None:
            return value

        # get json value from key
        json = request.get_json()
        if json is not None:
            value = json.get(key)
            if value is not None:
                return value

        return default
