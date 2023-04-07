from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(128) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS "chats" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "role" VARCHAR(2048) NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "messages" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "content" VARCHAR(2048) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "chat_id" UUID NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
