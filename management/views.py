from rest_framework import viewsets
from .models import Task, Inventory, Role, Staff
from .serializers import (
    TaskSerializer,
    InventorySerializer,
    RoleSerializer,
    StaffSerializer,
)
from .permissions import IsManager, IsHousekeeping


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class InventoryView(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class RoleView(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class StaffView(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class InventoryView(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
