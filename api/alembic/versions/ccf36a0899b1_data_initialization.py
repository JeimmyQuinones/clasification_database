"""data initialization

Revision ID: ccf36a0899b1
Revises: 21fa646ef1bf
Create Date: 2024-09-05 21:57:24.012968

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ccf36a0899b1"
down_revision: Union[str, None] = "21fa646ef1bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        INSERT INTO typeIdentifiedData VALUES (1,'FIRST_NAME','first,give,firstname'),(2,'LAST_NAME','last,surname,lastname'),(3,'IP_ADDRESS','ip,address'),(4,'CREDIT_CARD_NUMBER','card,number,credit,nocard'),(5,'N/A',''),(6,'USERNAME','username,usname,user'),(7,'EMAIL_ADDRESS','email,mail');

        """
    )
    op.execute(
        """
        INSERT INTO users VALUES (1,'string','$2b$12$kqfdN.rQBm108NcBeRLetekWnLlIwNlqE8cRydikagom0aRTn1B2G','2024-09-04 16:05:32');

        """
    )


def downgrade():
    op.execute(
        """
        DELETE FROM users ;
        DELETE FROM typeIdentifiedData ;
        """
    )
