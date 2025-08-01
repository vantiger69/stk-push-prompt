"""empty message

Revision ID: bc3a49eb8c5b
Revises: 658fc0c68512
Create Date: 2025-07-22 11:33:08.176949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc3a49eb8c5b'
down_revision = '658fc0c68512'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stk_push_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('business_shortcode', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('password', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('timestamp', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('transaction_type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('party_a', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('party_b', sa.String(length=20), nullable=False))
        batch_op.alter_column('transaction_desc',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['merchant_request_id'])
        batch_op.drop_column('status')

    with op.batch_alter_table('stk_push_response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('merchant_request_id', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('checkout_request_id', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('response_code', sa.String(length=10), nullable=False))
        batch_op.add_column(sa.Column('response_description', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('customer_message', sa.String(length=255), nullable=True))
        batch_op.drop_column('transaction_date')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('mpesa_receipt_number')
        batch_op.drop_column('result_code')
        batch_op.drop_column('result_desc')

    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('merchant_request_id', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('checkout_request_id', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('result_code', sa.String(length=10), nullable=False))
        batch_op.add_column(sa.Column('result_desc', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('mpesa_receipt_number', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('transaction_date', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('request_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint(batch_op.f('transaction_response_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'stk_push_request', ['request_id'], ['id'])
        batch_op.drop_column('type')
        batch_op.drop_column('reference')
        batch_op.drop_column('response_id')
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('response_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('reference', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('type', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('transaction_response_id_fkey'), 'stk_push_response', ['response_id'], ['id'])
        batch_op.drop_column('request_id')
        batch_op.drop_column('transaction_date')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('mpesa_receipt_number')
        batch_op.drop_column('result_desc')
        batch_op.drop_column('result_code')
        batch_op.drop_column('checkout_request_id')
        batch_op.drop_column('merchant_request_id')

    with op.batch_alter_table('stk_push_response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('result_desc', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('result_code', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('mpesa_receipt_number', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('transaction_date', sa.BIGINT(), autoincrement=False, nullable=True))
        batch_op.drop_column('customer_message')
        batch_op.drop_column('response_description')
        batch_op.drop_column('response_code')
        batch_op.drop_column('checkout_request_id')
        batch_op.drop_column('merchant_request_id')

    with op.batch_alter_table('stk_push_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('transaction_desc',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.drop_column('party_b')
        batch_op.drop_column('party_a')
        batch_op.drop_column('transaction_type')
        batch_op.drop_column('timestamp')
        batch_op.drop_column('password')
        batch_op.drop_column('business_shortcode')

    # ### end Alembic commands ###
