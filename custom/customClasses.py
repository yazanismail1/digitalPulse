import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from custom.CustomPagination import CustomUserPagination
from django.core.paginator import Paginator


class CustomAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomUserPagination

    def get_queryset(self, request):
        params_dict = dict(request.query_params.items())
        filterDict = {}
        for param, value in params_dict.items():
            if param != "page" and param != "limit":
                filterDict[param] = value
        return self.model.filter(**filterDict)
    
    def get(self, request):
        if not self.get_actions("get"):
            return Response({"reason": "get action is not allowed"}, status=400)
        queryset = self.get_queryset(request)
        items_per_page = request.GET.get('limit', 10)
        paginator = Paginator(queryset, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        count = paginator.count
        request_url = request.build_absolute_uri()
        nextPage =request_url.replace("page="+str(page_number),"page="+str(page.next_page_number())) if page.has_next() else None
        previousPage = request_url.replace("page="+str(page_number),"page="+str(page.previous_page_number())) if page.has_previous() else None
        serializer = self.serializer_class(page, many=True)

        returnObj = {
            "count": count, 
            "next": nextPage, 
            "previous": previousPage, 
            "limit": request.GET.get('limit', 10),
            "results": serializer.data
        }

        return Response(returnObj, status=200)
    
    def get_actions(self, method):
        actions = self.not_allowed_actions
        print(actions)
        if not actions:
            actions = []
        if method in actions:
            return False
        return True
    
    def post(self, request):
        if not self.get_actions("post"):
            return Response({"reason": "post action is not allowed"}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

    def put(self, request):
        if not self.get_actions("put"):
            return Response({"reason": "put action is not allowed"}, status=400)
        serializer = self.serializer_class(data=request.data, instance=self.model.objects.get(id=request.data.get("id")))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request):
        if not self.get_actions("patch"):
            return Response({"reason": "patch action is not allowed"}, status=400)
        serializer = self.serializer_class(data=request.data, instance=self.model.objects.get(id=request.data.get("id")), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        if not self.get_actions("delete"):
            return Response({"reason": "delete action is not allowed"}, status=400)
        try:
            self.model.objects.get(id=pk).delete()
            return Response({"detail": "deleted successfully"}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
