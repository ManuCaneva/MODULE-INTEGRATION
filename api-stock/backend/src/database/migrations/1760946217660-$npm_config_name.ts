import { MigrationInterface, QueryRunner } from "typeorm";

export class  $npmConfigName1760946217660 implements MigrationInterface {
    name = ' $npmConfigName1760946217660'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "dimensiones" DROP CONSTRAINT "FK_e103ebb174fd7a85e168929232b"`);
        await queryRunner.query(`ALTER TABLE "dimensiones" DROP CONSTRAINT "REL_e103ebb174fd7a85e168929232"`);
        await queryRunner.query(`ALTER TABLE "dimensiones" DROP COLUMN "producto_id"`);
        await queryRunner.query(`ALTER TABLE "productos" ADD "dimensionesId" integer`);
        await queryRunner.query(`ALTER TABLE "productos" ADD CONSTRAINT "UQ_371de83bd89d4002dd34234ab21" UNIQUE ("dimensionesId")`);
        await queryRunner.query(`ALTER TABLE "productos" ADD "ubicacionId" integer`);
        await queryRunner.query(`ALTER TABLE "productos" ADD CONSTRAINT "UQ_5fecc776a59cd149bc2fded563e" UNIQUE ("ubicacionId")`);
        await queryRunner.query(`ALTER TABLE "productos" ADD CONSTRAINT "FK_371de83bd89d4002dd34234ab21" FOREIGN KEY ("dimensionesId") REFERENCES "dimensiones"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "productos" ADD CONSTRAINT "FK_5fecc776a59cd149bc2fded563e" FOREIGN KEY ("ubicacionId") REFERENCES "ubicacion_almacen"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "productos" DROP CONSTRAINT "FK_5fecc776a59cd149bc2fded563e"`);
        await queryRunner.query(`ALTER TABLE "productos" DROP CONSTRAINT "FK_371de83bd89d4002dd34234ab21"`);
        await queryRunner.query(`ALTER TABLE "productos" DROP CONSTRAINT "UQ_5fecc776a59cd149bc2fded563e"`);
        await queryRunner.query(`ALTER TABLE "productos" DROP COLUMN "ubicacionId"`);
        await queryRunner.query(`ALTER TABLE "productos" DROP CONSTRAINT "UQ_371de83bd89d4002dd34234ab21"`);
        await queryRunner.query(`ALTER TABLE "productos" DROP COLUMN "dimensionesId"`);
        await queryRunner.query(`ALTER TABLE "dimensiones" ADD "producto_id" integer`);
        await queryRunner.query(`ALTER TABLE "dimensiones" ADD CONSTRAINT "REL_e103ebb174fd7a85e168929232" UNIQUE ("producto_id")`);
        await queryRunner.query(`ALTER TABLE "dimensiones" ADD CONSTRAINT "FK_e103ebb174fd7a85e168929232b" FOREIGN KEY ("producto_id") REFERENCES "productos"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

}
