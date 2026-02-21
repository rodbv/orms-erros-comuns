from __future__ import annotations

import datetime as dt
import random

from django.db import models
from django.utils import timezone

SECONDS_24_MONTHS = 730 * 24 * 60 * 60


def random_created_and_updated(rng: random.Random) -> tuple[dt.datetime, dt.datetime]:
    now = timezone.now()
    created_at = now - dt.timedelta(seconds=rng.randint(0, SECONDS_24_MONTHS))
    max_delta_seconds = int((now - created_at).total_seconds())
    updated_at = created_at + dt.timedelta(seconds=rng.randint(0, max_delta_seconds))
    return created_at, updated_at


def apply_random_timestamps(
    objects: list[models.Model],
    rng: random.Random,
    *,
    batch_size: int = 500,
) -> None:
    if not objects:
        return

    for obj in objects:
        created_at, updated_at = random_created_and_updated(rng)
        obj.data_criacao = created_at
        obj.data_alteracao = updated_at

    model_class = type(objects[0])
    model_class.objects.bulk_update(
        objects,
        ["data_criacao", "data_alteracao"],
        batch_size=batch_size,
    )
