from django.utils.deprecation import MiddlewareMixin

class CroessMiddleware(MiddlewareMixin):

    def process_reqeust(self,request,response):
        return None


    def process_response(self,request,response):

        if request.method == "OPTIONS":
            response["Access-Control-Allow-Headers"] = "X-Requested-With, X-CSRFToken,Content-Type,*"

        response["Access-Control-Allow-Origin"] = "*"

        # Access-Control-Allow-Headers
        return response