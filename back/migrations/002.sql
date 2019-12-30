ALTER TABLE "user" ADD "email" VARCHAR;
CREATE INDEX "user_email" ON "user" ("email");
ALTER TABLE "user" ADD "inscription_date" DATE NOT NULL DEFAULT '2019-12-31';
CREATE INDEX "user_inscription_date" ON "user" ("inscription_date");
ALTER TABLE "user" ADD "is_admin" INTEGER NOT NULL DEFAULT 0;
ALTER TABLE "user" ADD "is_member" INTEGER NOT NULL DEFAULT 0;