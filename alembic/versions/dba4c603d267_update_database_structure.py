"""update database structure

Revision ID: dba4c603d267
Revises: 01bea449e6f1
Create Date: 2023-12-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'dba4c603d267'
down_revision = '01bea449e6f1'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()

    # Users table
    if not conn.dialect.has_table(conn, 'users'):
        op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.String(), nullable=False),
            sa.Column('email', sa.String(), nullable=True),
            sa.Column('name', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id'),
            sa.UniqueConstraint('email')
        )
    
    with op.batch_alter_table('users', schema=None) as batch_op:
        if not conn.dialect.has_index(conn, 'users', 'ix_users_user_id'):
            batch_op.create_index(batch_op.f('ix_users_user_id'), ['user_id'], unique=True)
        if not conn.dialect.has_index(conn, 'users', 'ix_users_email'):
            batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    # Messages table
    if not conn.dialect.has_table(conn, 'messages'):
        op.create_table('messages',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('wamid', sa.String(), nullable=False),
            sa.Column('sender_id', sa.String(), nullable=True),
            sa.Column('content', sqlite.JSON, nullable=True),
            sa.Column('message_type', sa.String(), nullable=True),
            sa.Column('timestamp', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('wamid')
        )
    
    with op.batch_alter_table('messages', schema=None) as batch_op:
        if not conn.dialect.has_index(conn, 'messages', 'ix_messages_wamid'):
            batch_op.create_index(batch_op.f('ix_messages_wamid'), ['wamid'], unique=True)
        if not conn.dialect.has_index(conn, 'messages', 'ix_messages_sender_id'):
            batch_op.create_index(batch_op.f('ix_messages_sender_id'), ['sender_id'], unique=False)

    # Multimedia Messages table
    if not conn.dialect.has_table(conn, 'multimedia_messages'):
        op.create_table('multimedia_messages',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('message_id', sa.Integer(), nullable=False),
            sa.Column('media_type', sa.String(), nullable=True),
            sa.Column('media_id', sa.String(), nullable=True),
            sa.Column('media_url', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('message_id')
        )

    # Orders table
    if not conn.dialect.has_table(conn, 'orders'):
        op.create_table('orders',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('message_id', sa.Integer(), nullable=False),
            sa.Column('catalog_id', sa.String(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('total_price', sa.Float(), nullable=True),
            sa.Column('order_time', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
            sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('message_id')
        )

    # Order Items table
    if not conn.dialect.has_table(conn, 'order_items'):
        op.create_table('order_items',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('order_id', sa.Integer(), nullable=False),
            sa.Column('product_retailer_id', sa.String(), nullable=True),
            sa.Column('catalog_id', sa.String(), nullable=True),
            sa.Column('item_id', sa.String(), nullable=True),
            sa.Column('quantity', sa.Integer(), nullable=True),
            sa.Column('item_price', sa.Float(), nullable=True),
            sa.Column('currency', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Flow States table
    if not conn.dialect.has_table(conn, 'flow_states'):
        op.create_table('flow_states',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.String(), nullable=False),
            sa.Column('current_flow', sa.String(), nullable=False),
            sa.Column('current_node', sa.String(), nullable=True),
            sa.Column('context', sqlite.JSON, nullable=True),
            sa.Column('last_updated', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id')
        )
    
    with op.batch_alter_table('flow_states', schema=None) as batch_op:
        if not conn.dialect.has_index(conn, 'flow_states', 'ix_flow_states_user_id'):
            batch_op.create_index(batch_op.f('ix_flow_states_user_id'), ['user_id'], unique=True)

    # Window Quotes table
    if not conn.dialect.has_table(conn, 'window_quotes'):
        op.create_table('window_quotes',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('status', sa.String(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Windows table
    if not conn.dialect.has_table(conn, 'windows'):
        op.create_table('windows',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('quote_id', sa.Integer(), nullable=False),
            sa.Column('reference', sa.String(), nullable=True),
            sa.Column('width', sa.Float(), nullable=True),
            sa.Column('height', sa.Float(), nullable=True),
            sa.Column('color', sa.String(), nullable=True),
            sa.Column('has_blind', sa.Boolean(), nullable=True),
            sa.Column('motorized_blind', sa.Boolean(), nullable=True),
            sa.Column('opening_type', sa.String(), nullable=True),
            sa.Column('image_url', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['quote_id'], ['window_quotes.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade():
    # Este método se mantiene igual que en la versión anterior
    op.drop_table('windows')
    op.drop_table('window_quotes')
    with op.batch_alter_table('flow_states', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_flow_states_user_id'))
    op.drop_table('flow_states')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('multimedia_messages')
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_messages_sender_id'))
        batch_op.drop_index(batch_op.f('ix_messages_wamid'))
    op.drop_table('messages')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_index(batch_op.f('ix_users_user_id'))
    op.drop_table('users')

