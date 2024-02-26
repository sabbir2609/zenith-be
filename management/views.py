from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager, IsHousekeeping

from .models import Task, Inventory, Role, Staff

from .serializers import (
    TaskSerializer,
    InventorySerializer,
    RoleSerializer,
    StaffSerializer,
)


class RoleView(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class InventoryView(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsManager]


class StaffView(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsHousekeeping]


class InventoryView(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsManager]
