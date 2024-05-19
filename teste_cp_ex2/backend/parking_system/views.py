from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer, Vehicle, Plan, CustomerPlan, Contract, ContractRule, ParkMovement
from .serializers import CustomerSerializer, VehicleSerializer, PlanSerializer, CustomerPlanSerializer, ContractSerializer, ContractRuleSerializer, ParkMovementSerializer
from datetime import datetime
from django.utils import timezone

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def create(self, request, *args, **kwargs):
        plate = request.data.get('plate')
        existing_vehicle = Vehicle.objects.filter(plate=plate).first()
        if existing_vehicle:
            if existing_vehicle.customer:
                return Response({'error': 'Vehicle already registered to a customer.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(VehicleSerializer(existing_vehicle).data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class CustomerPlanViewSet(viewsets.ModelViewSet):
    queryset = CustomerPlan.objects.all()
    serializer_class = CustomerPlanSerializer

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class ContractRuleViewSet(viewsets.ModelViewSet):
    queryset = ContractRule.objects.all()
    serializer_class = ContractRuleSerializer

class ParkMovementViewSet(viewsets.ModelViewSet):
    queryset = ParkMovement.objects.all().order_by('-entry_date')
    serializer_class = ParkMovementSerializer

    def create(self, request, *args, **kwargs):
        plate = request.data.get('plate')
        card_id = request.data.get('card_id')

        if not any([plate, card_id]):
            return Response({'error': 'Either Plate or Card ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if card_id and not Customer.objects.filter(card_id=card_id).exists():
            return Response({'error': 'Invalid Card ID.'}, status=status.HTTP_400_BAD_REQUEST)

        vehicle = None
        if plate:
            vehicle = Vehicle.objects.filter(plate=plate).first()
            if not vehicle:
                vehicle = Vehicle.objects.create(plate=plate, model='', description='')
        elif card_id: 
            customer = Customer.objects.get(card_id=card_id)
            vehicle = customer.vehicle_set.first()

        if ParkMovement.objects.filter(vehicle=vehicle, exit_date__isnull=True).exists():
            return Response({'error': 'Vehicle already parked'}, status=status.HTTP_400_BAD_REQUEST)

        park_movement = ParkMovement.objects.create(vehicle=vehicle, entry_date=datetime.now())

        serializer = ParkMovementSerializer(park_movement)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.exit_date:
            return Response({'error': 'Vehicle already left the parking lot'}, status=status.HTTP_400_BAD_REQUEST)

        instance.exit_date = timezone.now()
        if not instance.vehicle.customer:
            contract = Contract.objects.first()
            duration = instance.exit_date - instance.entry_date
            total_minutes = int(duration.total_seconds() / 60)

            value = 0
            for rule in contract.contractrule_set.all().order_by('until'):
                if total_minutes <= rule.until:
                    value = rule.value
                    break

            if value == 0:
                value = contract.max_value

            instance.value = value
        instance.save()

        serializer = ParkMovementSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)