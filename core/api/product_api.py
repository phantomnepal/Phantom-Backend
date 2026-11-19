from rest_framework.views import APIView
from rest_framework.response import Response
from core.models.product import Product
from core.serializers.product_serializer import ProductSerializer
import cloudinary.uploader
from core.mixins.admin_user_mixin import AdminUserMixin


class ProductAPIView(APIView,AdminUserMixin):
    authentication_classes=[]
    permission_classes=[]
    def get(self,request):
        try:
            _,error=self.get_user_or_error(request)
            if (error):
                return error    
            products= Product.objects.all()
            serilizer=ProductSerializer(products,many=True)
            return Response({"status": "success", "data": serilizer.data})
        except Exception as e:
            return Response({"status":"error","error":str(e)},status=500)

    def post(self,request):
        try:
            serializer=ProductSerializer(data=request.data)
            if serializer.is_valid():
                image=request.FILES.get("image")
                image_url=None
                if image:
                    result=cloudinary.uploader.upload(
                        image,
                        folder="maa_durga_products"
                    )
                    image_url=result["secure_url"]
    
                product=serializer.save(image=image_url)
    
                return Response({
                    "status":"success",
                    "data":ProductSerializer(product).data,
                },status=200
                )
            
            return Response(
                    {
                        "status": "Failed",
                        "error": serializer.errors
                    },
                    status=400
                    )
        except Exception as e:
             return Response({
                  "status":"Failed",
                  "error":str(e)
             },status=400)