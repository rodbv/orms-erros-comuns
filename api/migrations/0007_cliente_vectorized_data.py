from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_pedido_itempedido_vectorized_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="vectorized_data",
            field=models.TextField(blank=True, default=""),
        ),
    ]
