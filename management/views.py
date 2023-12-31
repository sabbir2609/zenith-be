from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsManager, IsHousekeeping


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsManager | IsHousekeeping]
