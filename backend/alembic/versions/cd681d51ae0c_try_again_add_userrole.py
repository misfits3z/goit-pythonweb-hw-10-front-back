"""TRY AGAIN ADD USERROLE

Revision ID: cd681d51ae0c
Revises: 6480903b31ec
Create Date: 2025-04-08 06:23:26.614503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd681d51ae0c'
down_revision: Union[str, None] = '6480903b31ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Створюємо enum окремо
user_role_enum = sa.Enum("USER", "ADMIN", name="userrole")


def upgrade() -> None:
    """Upgrade schema."""
    # Створення enum типу
    user_role_enum.create(op.get_bind())

    # Додаємо колонку role з цим типом
    op.add_column("users", sa.Column("role", user_role_enum, nullable=False))

    # Робимо колонку is_verified обов'язковою
    op.alter_column("users", "is_verified", existing_type=sa.BOOLEAN(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Повертаємо is_verified як nullable
    op.alter_column("users", "is_verified", existing_type=sa.BOOLEAN(), nullable=True)

    # Видаляємо колонку role
    op.drop_column("users", "role")

    # Видаляємо enum тип
    user_role_enum.drop(op.get_bind())
