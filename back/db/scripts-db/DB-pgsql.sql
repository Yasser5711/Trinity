CREATE TABLE "addresses"(
    "user_id" INTEGER NULL,
    "address_id" INTEGER NOT NULL,
    "address_line" VARCHAR(255) NOT NULL,
    "city" VARCHAR(100) NULL,
    "zip_code" VARCHAR(20) NULL,
    "country" VARCHAR(100) NULL
);
ALTER TABLE
    "addresses" ADD PRIMARY KEY("address_id");
CREATE TABLE "user_roles"(
    "user_id" INTEGER NOT NULL,
    "role_id" INTEGER NOT NULL
);
ALTER TABLE
    "user_roles" ADD PRIMARY KEY("user_id");
ALTER TABLE
    "user_roles" ADD PRIMARY KEY("role_id");
CREATE TABLE "users"(
    "email" VARCHAR(255) NULL,
    "user_id" INTEGER NOT NULL,
    "phone" VARCHAR(50) NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(255) NULL,
    "password_hash" TEXT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "role_id" INTEGER NULL,
    "address_id" INTEGER NULL,
    "last_name" VARCHAR(255) NULL
);
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
ALTER TABLE
    "users" ADD PRIMARY KEY("user_id");
CREATE TABLE "products"(
    "nutriScore" VARCHAR(2) NULL,
    "product_id" VARCHAR(255) NOT NULL,
    "barCode" VARCHAR(255) NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "picture" TEXT NULL,
    "price" DECIMAL(10, 2) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "brand" VARCHAR(255) NULL
);
ALTER TABLE
    "products" ADD PRIMARY KEY("product_id");
CREATE TABLE "invoices"(
    "total_amount" DECIMAL(10, 2) NOT NULL,
    "invoice_id" INTEGER NOT NULL,
    "user_id" INTEGER NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "payment_status" VARCHAR(50) NULL
);
ALTER TABLE
    "invoices" ADD PRIMARY KEY("invoice_id");
CREATE TABLE "cart_items"(
    "product_id" VARCHAR(255) NULL,
    "quantity" INTEGER NOT NULL,
    "cart_id" INTEGER NULL,
    "cart_item_id" INTEGER NOT NULL,
);
ALTER TABLE
    "cart_items" ADD PRIMARY KEY("cart_item_id");
CREATE TABLE "kpis"(
    "kpi_id" INTEGER NOT NULL,
    "kpi_name" VARCHAR(255) NOT NULL,
    "kpi_value" DECIMAL(10, 2) NULL,
    "last_updated" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "kpis" ADD PRIMARY KEY("kpi_id");
CREATE TABLE "invoice_items"(
    "product_id" VARCHAR(255) NULL,
    "quantity" INTEGER NOT NULL,
    "invoice_id" INTEGER NULL,
    "invoice_item_id" INTEGER NOT NULL,
    "unit_price" DECIMAL(10, 2) NOT NULL
);
ALTER TABLE
    "invoice_items" ADD PRIMARY KEY("invoice_item_id");
CREATE TABLE "roles"(
    "role_name" VARCHAR(255) NOT NULL,
    "role_id" INTEGER NOT NULL
);
ALTER TABLE
    "roles" ADD PRIMARY KEY("role_id");
CREATE TABLE "stocks"(
    "product_id" VARCHAR(255) NULL,
    "quantity" INTEGER NOT NULL,
    "stock_id" VARCHAR(255) NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "stocks" ADD PRIMARY KEY("stock_id");
CREATE TABLE "carts"(
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INTEGER NULL,
    "cart_id" INTEGER NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "carts" ADD PRIMARY KEY("cart_id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_address_id_foreign" FOREIGN KEY("address_id") REFERENCES "addresses"("address_id");
ALTER TABLE
    "addresses" ADD CONSTRAINT "addresses_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
ALTER TABLE
    "cart_items" ADD CONSTRAINT "cart_items_cart_id_foreign" FOREIGN KEY("cart_id") REFERENCES "carts"("cart_id");
ALTER TABLE
    "cart_items" ADD CONSTRAINT "cart_items_product_id_foreign" FOREIGN KEY("product_id") REFERENCES "products"("product_id");
ALTER TABLE
    "invoice_items" ADD CONSTRAINT "invoice_items_product_id_foreign" FOREIGN KEY("product_id") REFERENCES "products"("product_id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user_roles"("user_id");
ALTER TABLE
    "invoices" ADD CONSTRAINT "invoices_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_role_id_foreign" FOREIGN KEY("role_id") REFERENCES "roles"("role_id");
ALTER TABLE
    "roles" ADD CONSTRAINT "roles_role_id_foreign" FOREIGN KEY("role_id") REFERENCES "user_roles"("role_id");
ALTER TABLE
    "carts" ADD CONSTRAINT "carts_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
ALTER TABLE
    "stocks" ADD CONSTRAINT "stocks_product_id_foreign" FOREIGN KEY("product_id") REFERENCES "products"("product_id");
ALTER TABLE
    "invoice_items" ADD CONSTRAINT "invoice_items_invoice_id_foreign" FOREIGN KEY("invoice_id") REFERENCES "invoices"("invoice_id");