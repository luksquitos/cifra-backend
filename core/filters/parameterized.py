from rest_framework.filters import BaseFilterBackend


class ParameterizedFilterBackend(BaseFilterBackend):
    def get_params(self, view, request):
        return getattr(view, "filter_params", [])

    def get_params_filter_query(self, view, request):
        return getattr(view, "filter_params_query", [])

    def get_search_params_names(self, view, request):
        params = {}
        raw_params = self.get_params(view, request)
        for param in raw_params:
            param_name = getattr(view, "%s_param" % param, None)
            if not param_name:
                param_name = param

            params[param] = param_name

        return params

    def get_param_value(self, request, param_name):
        value = request.query_params.get(param_name, "")
        value = value.replace("\x00", "")
        value = value.replace(",", " ")
        return value

    def get_search_params_values(self, names: dict, request):
        values = {}
        for name in names.keys():
            values[name] = self.get_param_value(request, names[name])
        return values

    def filter_queryset(self, request, queryset, view):
        names = self.get_search_params_names(view, request)
        query_names = self.get_params_filter_query(view, request)
        values = self.get_search_params_values(names, request)

        queryset_dict = {}
        for item in names.keys():
            if not values[item]:
                continue
            queryset_dict[query_names[item]] = values[item]

        if len(queryset_dict.keys()) == 0:
            return queryset

        return queryset.filter(**queryset_dict)


__all__ = ["ParameterizedFilterBackend"]
