from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import TIMESTAMP, text


class TimeStampMixin:
    """
    Миксин для автоматического добавления времени создания и обновления
    """

    # написали чтобы не писать created_at и updated_at каждый раз

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=text("current_timestamp(0)"),        # Генерация времени сервера
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=text("current_timestamp(0)"),
        onupdate=text("current_timestamp(0)"),
    )
