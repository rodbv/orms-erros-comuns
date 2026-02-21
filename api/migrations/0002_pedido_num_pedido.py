import secrets
import string

from django.db import migrations, models


def gerar_num_pedido() -> str:
    return (
        "".join(secrets.choice(string.ascii_uppercase) for _ in range(3))
        + "".join(secrets.choice(string.digits) for _ in range(3))
        + secrets.choice(string.ascii_uppercase)
    )


def popular_num_pedido(apps, schema_editor):
    Pedido = apps.get_model("api", "Pedido")

    for pedido in Pedido.objects.filter(num_pedido__isnull=True):
        tentativas_maximas = 20
        for _ in range(tentativas_maximas):
            candidato = gerar_num_pedido()
            if not Pedido.objects.filter(num_pedido=candidato).exists():
                pedido.num_pedido = candidato
                pedido.save(update_fields=["num_pedido"])
                break
        else:
            raise ValueError("Não foi possível gerar num_pedido único na migração")


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="num_pedido",
            field=models.CharField(db_index=True, max_length=7, null=True, unique=True),
        ),
        migrations.RunPython(popular_num_pedido, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="pedido",
            name="num_pedido",
            field=models.CharField(db_index=True, editable=False, max_length=7, unique=True),
        ),
    ]
