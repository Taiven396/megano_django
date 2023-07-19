class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            request.session["cart"]
            return response
        except KeyError:
            request.session["cart"] = []
            return response
