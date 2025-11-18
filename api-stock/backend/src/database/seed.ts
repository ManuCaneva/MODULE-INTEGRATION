import { NestFactory } from '@nestjs/core';
import { AppModule } from '../app.module';
import { SeedsService } from './seeds/seeds.service';

async function bootstrap() {
  const app = await NestFactory.createApplicationContext(AppModule);
  const seedsService = app.get(SeedsService);

  try {
    await seedsService.loadData();
    console.log('Seeding complete!');
  } catch (error) {
    console.error('Seeding failed:', error);
  } finally {
    await app.close();
  }
}

bootstrap();
