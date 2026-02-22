from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_itempedido_valor_total_pedido_valor_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="itempedido",
            name="vectorized_data",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="pedido",
            name="vectorized_data",
            field=models.TextField(blank=True, default=""),
        ),
    ]
