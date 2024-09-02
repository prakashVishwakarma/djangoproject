from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Task
from django.http import JsonResponse
import json

class TaskCreateView(APIView):
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        completed = request.data.get('completed', False)  # default to False if not provided

        if not title or not description:
            return Response({'error': 'Title and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if Task.objects.filter(title=title).exists():
            return Response({'error': 'A task with this title already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.create(
            title=title,
            description=description,
            completed=completed
        )

        return Response({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        tasks = Task.objects.all()
        if tasks is not None :
            task_list = list(tasks.values('id', 'title', 'description', 'completed'))
            return JsonResponse(task_list, safe=False, json_dumps_params={'indent': 2})
        return JsonResponse({'data':'nothing in database'})

    def get(self, request, pk):
        # Validate pk parameter
        if not pk.isdigit():
            return JsonResponse({'error': 'Invalid ID. Must be a positive integer.'}, status=400)

        try:
            task = Task.objects.get(pk=pk)
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed
            }
            return JsonResponse(task_data, json_dumps_params={'indent': 2})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)
        
    def put(self, request, pk):
        # Validate pk parameter
        if not pk.isdigit():
            return JsonResponse({'error': 'Invalid ID. Must be a positive integer.'}, status=400)
        
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)
        
        try:
            # Parse the request body
            data = json.loads(request.body)
            
            title = data.get('title')
            description = data.get('description')
            completed = data.get('completed')
            
            # Validate input
            if title is not None:
                if Task.objects.filter(title=title).exclude(pk=pk).exists():
                    return JsonResponse({'error': 'A task with this title already exists.'}, status=400)
                task.title = title
            
            if description is not None:
                task.description = description
            
            if completed is not None:
                if not isinstance(completed, bool):
                    return JsonResponse({'error': 'Completed must be a boolean value.'}, status=400)
                task.completed = completed
            
            task.save()
            
            # Return the updated task
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed
            }
            return JsonResponse(task_data, json_dumps_params={'indent': 2})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    def patch(self, request, pk):
        # Validate pk parameter
        if not pk.isdigit():
            return JsonResponse({'error': 'Invalid ID. Must be a positive integer.'}, status=400)
        
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)
        
        try:
            # Parse the request body
            data = json.loads(request.body)
            
            title = data.get('title')
            description = data.get('description')
            completed = data.get('completed')
            
            # Update fields if provided
            if title is not None:
                # Ensure title is unique
                if Task.objects.filter(title=title).exclude(pk=pk).exists():
                    return JsonResponse({'error': 'A task with this title already exists.'}, status=400)
                task.title = title
            
            if description is not None:
                task.description = description
            
            if completed is not None:
                if not isinstance(completed, bool):
                    return JsonResponse({'error': 'Completed must be a boolean value.'}, status=400)
                task.completed = completed
            
            task.save()
            
            # Return the updated task
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed
            }
            return JsonResponse(task_data, json_dumps_params={'indent': 2})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)