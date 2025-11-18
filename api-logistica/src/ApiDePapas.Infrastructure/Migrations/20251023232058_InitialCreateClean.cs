using System;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiDePapas.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreateClean : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterDatabase()
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Localities",
                columns: table => new
                {
                    postal_code = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    locality_name = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    state_name = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    country = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    lat = table.Column<float>(type: "float", nullable: false),
                    lon = table.Column<float>(type: "float", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Localities", x => new { x.postal_code, x.locality_name });
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "TransportMethods",
                columns: table => new
                {
                    transport_id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    transport_type = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    average_speed = table.Column<float>(type: "float", nullable: false),
                    available = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    max_capacity = table.Column<float>(type: "float", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_TransportMethods", x => x.transport_id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Addresses",
                columns: table => new
                {
                    address_id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    street = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    number = table.Column<int>(type: "int", nullable: false),
                    postal_code = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    locality_name = table.Column<string>(type: "varchar(255)", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Addresses", x => x.address_id);
                    table.ForeignKey(
                        name: "FK_Addresses_Localities_postal_code_locality_name",
                        columns: x => new { x.postal_code, x.locality_name },
                        principalTable: "Localities",
                        principalColumns: new[] { "postal_code", "locality_name" },
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "DistributionCenters",
                columns: table => new
                {
                    distribution_center_id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    address_id = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DistributionCenters", x => x.distribution_center_id);
                    table.ForeignKey(
                        name: "FK_DistributionCenters_Addresses_address_id",
                        column: x => x.address_id,
                        principalTable: "Addresses",
                        principalColumn: "address_id",
                        onDelete: ReferentialAction.Restrict);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Travels",
                columns: table => new
                {
                    travel_id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    departure_time = table.Column<DateTime>(type: "datetime(6)", nullable: false),
                    arrival_time = table.Column<DateTime>(type: "datetime(6)", nullable: true),
                    transport_method_id = table.Column<int>(type: "int", nullable: false),
                    distribution_center_id = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Travels", x => x.travel_id);
                    table.ForeignKey(
                        name: "FK_Travels_DistributionCenters_distribution_center_id",
                        column: x => x.distribution_center_id,
                        principalTable: "DistributionCenters",
                        principalColumn: "distribution_center_id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_Travels_TransportMethods_transport_method_id",
                        column: x => x.transport_method_id,
                        principalTable: "TransportMethods",
                        principalColumn: "transport_id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Shippings",
                columns: table => new
                {
                    shipping_id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    order_id = table.Column<int>(type: "int", nullable: false),
                    user_id = table.Column<int>(type: "int", nullable: false),
                    delivery_address_id = table.Column<int>(type: "int", nullable: false),
                    status = table.Column<int>(type: "int", nullable: false),
                    travel_id = table.Column<int>(type: "int", nullable: false),
                    tracking_number = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    carrier_name = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    total_cost = table.Column<float>(type: "float", nullable: false),
                    currency = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    estimated_delivery_at = table.Column<DateTime>(type: "datetime(6)", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime(6)", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime(6)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Shippings", x => x.shipping_id);
                    table.ForeignKey(
                        name: "FK_Shippings_Addresses_delivery_address_id",
                        column: x => x.delivery_address_id,
                        principalTable: "Addresses",
                        principalColumn: "address_id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Shippings_Travels_travel_id",
                        column: x => x.travel_id,
                        principalTable: "Travels",
                        principalColumn: "travel_id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "ProductQty",
                columns: table => new
                {
                    RowId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    ShippingDetailshipping_id = table.Column<int>(type: "int", nullable: false),
                    id = table.Column<int>(type: "int", nullable: false),
                    quantity = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ProductQty", x => new { x.RowId, x.ShippingDetailshipping_id });
                    table.ForeignKey(
                        name: "FK_ProductQty_Shippings_ShippingDetailshipping_id",
                        column: x => x.ShippingDetailshipping_id,
                        principalTable: "Shippings",
                        principalColumn: "shipping_id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "ShippingLog",
                columns: table => new
                {
                    ShippingDetailshipping_id = table.Column<int>(type: "int", nullable: false),
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    Timestamp = table.Column<DateTime>(type: "datetime(6)", nullable: true),
                    Status = table.Column<int>(type: "int", nullable: true),
                    Message = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ShippingLog", x => new { x.ShippingDetailshipping_id, x.Id });
                    table.ForeignKey(
                        name: "FK_ShippingLog_Shippings_ShippingDetailshipping_id",
                        column: x => x.ShippingDetailshipping_id,
                        principalTable: "Shippings",
                        principalColumn: "shipping_id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateIndex(
                name: "IX_Addresses_postal_code_locality_name",
                table: "Addresses",
                columns: new[] { "postal_code", "locality_name" });

            migrationBuilder.CreateIndex(
                name: "IX_DistributionCenters_address_id",
                table: "DistributionCenters",
                column: "address_id");

            migrationBuilder.CreateIndex(
                name: "IX_ProductQty_ShippingDetailshipping_id",
                table: "ProductQty",
                column: "ShippingDetailshipping_id");

            migrationBuilder.CreateIndex(
                name: "IX_Shippings_delivery_address_id",
                table: "Shippings",
                column: "delivery_address_id");

            migrationBuilder.CreateIndex(
                name: "IX_Shippings_travel_id",
                table: "Shippings",
                column: "travel_id");

            migrationBuilder.CreateIndex(
                name: "IX_Travels_distribution_center_id",
                table: "Travels",
                column: "distribution_center_id");

            migrationBuilder.CreateIndex(
                name: "IX_Travels_transport_method_id",
                table: "Travels",
                column: "transport_method_id");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "ProductQty");

            migrationBuilder.DropTable(
                name: "ShippingLog");

            migrationBuilder.DropTable(
                name: "Shippings");

            migrationBuilder.DropTable(
                name: "Travels");

            migrationBuilder.DropTable(
                name: "DistributionCenters");

            migrationBuilder.DropTable(
                name: "TransportMethods");

            migrationBuilder.DropTable(
                name: "Addresses");

            migrationBuilder.DropTable(
                name: "Localities");
        }
    }
}
