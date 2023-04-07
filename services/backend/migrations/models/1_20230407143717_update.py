from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" RENAME COLUMN "role" TO "assist_role";
        ALTER TABLE "messages" ADD "role" VARCHAR(9) NOT NULL  DEFAULT 'user';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" RENAME COLUMN "assist_role" TO "role";"""
