from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(128) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "chats" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "conversations" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "sequence" INT NOT NULL,
    "prompt" VARCHAR(1024) NOT NULL,
    "prompt_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "completion" VARCHAR(4096) NOT NULL,
    "completion_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "chat_id" UUID NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tags" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_tags_user_id_557109" UNIQUE ("user_id", "name")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "conversations_tags" (
    "conversations_id" UUID NOT NULL REFERENCES "conversations" ("id") ON DELETE CASCADE,
    "tags_id" UUID NOT NULL REFERENCES "tags" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
