using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiDePapas.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddedOptimizedIndexes : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameIndex(
                name: "IX_Addresses_postal_code_locality_name",
                table: "Addresses",
                newName: "IX_Addresses_locality_fk");

            migrationBuilder.CreateIndex(
                name: "IX_Shippings_created_at",
                table: "Shippings",
                column: "created_at");

            migrationBuilder.CreateIndex(
                name: "IX_Shippings_status",
                table: "Shippings",
                column: "status");

            migrationBuilder.CreateIndex(
                name: "IX_ShippingLog_ShippingDetailshipping_id",
                table: "ShippingLog",
                column: "ShippingDetailshipping_id");

            migrationBuilder.CreateIndex(
                name: "IX_Localities_locality_name",
                table: "Localities",
                column: "locality_name");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_Shippings_created_at",
                table: "Shippings");

            migrationBuilder.DropIndex(
                name: "IX_Shippings_status",
                table: "Shippings");

            migrationBuilder.DropIndex(
                name: "IX_ShippingLog_ShippingDetailshipping_id",
                table: "ShippingLog");

            migrationBuilder.DropIndex(
                name: "IX_Localities_locality_name",
                table: "Localities");

            migrationBuilder.RenameIndex(
                name: "IX_Addresses_locality_fk",
                table: "Addresses",
                newName: "IX_Addresses_postal_code_locality_name");
        }
    }
}
