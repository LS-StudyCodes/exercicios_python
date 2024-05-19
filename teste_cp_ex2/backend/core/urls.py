from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from parking_system import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'plans', views.PlanViewSet)
router.register(r'customer-plans', views.CustomerPlanViewSet)
router.register(r'contracts', views.ContractViewSet)
router.register(r'contract-rules', views.ContractRuleViewSet)
router.register(r'park-movements', views.ParkMovementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
