from rest_framework import serializers
from .models import Customer, Vehicle, Plan, CustomerPlan, Contract, ContractRule, ParkMovement

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Vehicle
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class CustomerPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPlan
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    rules = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = '__all__'

    def create(self, validated_data):
        rules_data = validated_data.pop('rules', [])
        contract = Contract.objects.create(**validated_data)
        for rule_data in rules_data:
            ContractRule.objects.create(contract=contract, **rule_data)
        return contract

    def update(self, instance, validated_data):
        rules_data = validated_data.pop('rules', [])
        instance = super().update(instance, validated_data)
        instance.contractrule_set.all().delete()  
        for rule_data in rules_data:
            ContractRule.objects.create(contract=instance, **rule_data)
        return instance

    def get_rules(self, obj):
        rules = obj.contractrule_set.all()
        return ContractRuleSerializer(rules, many=True).data

class ContractRuleSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ContractRule
        fields = '__all__'

class ParkMovementSerializer(serializers.ModelSerializer):
    plate = serializers.CharField(source='vehicle.plate', read_only=True)
    card_id = serializers.CharField(source='vehicle.customer.card_id', read_only=True)
    
    class Meta:
        model = ParkMovement
        fields = '__all__'