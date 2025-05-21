from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import ShoppingCart
from recipes.models import Recipe
from .serializers import (
    ShoppingCartSerializer,
)


class ShoppingCartCreateDeleteView(
    generics.CreateAPIView, generics.DestroyAPIView,
):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ShoppingCartSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'recipe_id'

    def get_object(self):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)

        try:
            return ShoppingCart.objects.get(
                user=self.request.user, recipe=recipe,
            )
        except ShoppingCart.DoesNotExist:
            raise ValidationError(
                {"detail": "Рецепт не найден в вашем списке покупок."},
                code=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if ShoppingCart.objects.filter(
            user=request.user, recipe=recipe,
        ).exists():
            return Response(
                {"detail": "Рецепт уже в списке покупок."},
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite = ShoppingCart.objects.create(
            user=request.user, recipe=recipe
        )
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShoppingCartDownloadPDF(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)

        if not shopping_cart.exists():
            raise ValidationError({'detail': 'Ваш список покупок пуст.'})

        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        except Exception:
            return HttpResponse(
                "Файл шрифта DejaVuSans.ttf не найден", status=500
            )

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        top_margin = height - 50
        left_margin = 50
        bottom_margin = 50

        y_position = top_margin

        pdf.setFont("DejaVuSans", 18)
        pdf.drawCentredString(width / 2, y_position, "Список покупок")
        y_position -= 40

        for item in shopping_cart:
            recipe = item.recipe

            if y_position < 200:
                pdf.showPage()
                pdf.setFont("DejaVuSans", 18)
                y_position = top_margin
                pdf.drawCentredString(width / 2, y_position, "Список покупок")
                y_position -= 40

            pdf.setFont("DejaVuSans", 14)
            pdf.drawString(left_margin, y_position, f"Рецепт: {recipe.name}")
            y_position -= 20

            cooking_time = recipe.cooking_time
            last_digit = cooking_time % 10
            if 11 <= cooking_time % 100 <= 14:
                time_string = f"Время приготовления: {cooking_time} минут"
            elif last_digit == 1:
                time_string = f"Время приготовления: {cooking_time} минута"
            elif 2 <= last_digit <= 4:
                time_string = f"Время приготовления: {cooking_time} минуты"
            else:
                time_string = f"Время приготовления: {cooking_time} минут"

            pdf.setFont("DejaVuSans", 12)
            pdf.drawString(left_margin, y_position, time_string)
            y_position -= 20

            if recipe.image:
                try:
                    img = ImageReader(recipe.image.file)
                    img_width, img_height = img.getSize()

                    max_width = 150
                    max_height = 150
                    ratio = min(max_width / img_width, max_height / img_height)
                    new_width = img_width * ratio
                    new_height = img_height * ratio

                    img_x = left_margin
                    img_y = y_position - new_height

                    if img_y < bottom_margin:
                        pdf.showPage()
                        y_position = top_margin
                        img_y = y_position - new_height

                    pdf.drawImage(
                        img,
                        img_x,
                        img_y,
                        width=new_width,
                        height=new_height,
                        preserveAspectRatio=True,
                        mask='auto'
                    )

                    y_position = img_y - 20

                except Exception:
                    pass

            pdf.setFont("DejaVuSans", 11)
            pdf.drawString(left_margin, y_position, "Ингредиенты:")
            y_position -= 15

            for ingredient_rel in recipe.recipe_from_ingredient.all():
                ingredient = ingredient_rel.ingredient
                text = f"- {ingredient.name}: {ingredient_rel.amount} {ingredient.measurement_unit}"

                if y_position < bottom_margin + 30:
                    pdf.showPage()
                    y_position = top_margin

                pdf.drawString(left_margin + 20, y_position, text)
                y_position -= 15

            y_position -= 30

        pdf.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.pdf"'
        return response
