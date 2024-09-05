from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import WaterIntake
from user_auth.models import User_Auth
from django.utils import timezone
from django.db.models import Sum

@api_view(['POST'])
def register_intake(request):
    user_id = request.data.get('user_id')
    intake_ml = request.data.get('intake_ml')
    user = User_Auth.objects.get(id=user_id)

    WaterIntake.objects.create(user=user, intake_ml=intake_ml)
    return Response({'message': 'Intake registered successfully!'})

@api_view(['GET'])
def daily_progress(request, user_id):
    try:
        user = User_Auth.objects.get(pk=user_id)
    except User_Auth.DoesNotExist:
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    daily_goal = int(user.weight) * 35 
    max_intake = 5000

    today = timezone.now().date()
    total_intake = WaterIntake.objects.filter(user=user, date=today).aggregate(Sum('intake_ml'))['intake_ml__sum'] or 0

    remaining = max(0, daily_goal - total_intake)

    max_reached = total_intake >= max_intake

    data = {
        'daily_goal': daily_goal,
        'total_intake': total_intake,
        'remaining': remaining,
        'goal_achieved': total_intake >= daily_goal,
        'max_intake_reached': max_reached,
    }

    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
def intake_history(request, user_id):
    user = User_Auth.objects.get(id=user_id)
    daily_goal = int(user.weight) * 35  # Meta diária baseada no peso do usuário

    # Agrupar por data, somar intake_ml e verificar se a meta foi atingida, ordenar por data decrescente
    history = WaterIntake.objects.filter(user=user) \
        .extra(select={'date': 'date(date)'}) \
        .values('date') \
        .annotate(total_intake=Sum('intake_ml')) \
        .order_by('-date')  # Ordenar por data mais recente

    # Preparar a resposta com informações diárias
    detailed_history = []

    for entry in history:
        total_intake = entry['total_intake']
        goal_achieved = total_intake >= daily_goal

        detailed_history.append({
            'date': entry['date'],
            'intake_ml': total_intake,
            'daily_goal': daily_goal,
            'goal_achieved': goal_achieved
        })

    return Response(detailed_history, status=status.HTTP_200_OK)







