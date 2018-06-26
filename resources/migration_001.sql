--
-- Add field is_completed to todos
--
ALTER TABLE "todos" RENAME TO "todos__old";
CREATE TABLE "todos" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "description" varchar(100) NOT NULL,
  "is_completed" INT(1) NOT NULL DEFAULT 0,
  "user_id" integer NOT NULL REFERENCES "users"("id")
  );
INSERT INTO "todos" ("id", "description", "user_id", "is_completed")
  SELECT "id", "description", "user_id", 0
  FROM "todos__old";
DROP TABLE "todos__old";
