import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Categoria } from './entities/categoria.entity';
import { CreateCategoriaDto } from './dto/create-categoria.dto';
import { UpdateCategoriaDto } from './dto/update-categoria.dto';

@Injectable()
export class CategoriasService {
  constructor(
    @InjectRepository(Categoria)
    private categoriasRepository: Repository<Categoria>,
  ) {}

  async findAll(): Promise<Categoria[]> {
    return this.categoriasRepository.find({
      where: { activa: true },
      order: { nombre: 'ASC' }
    });
  }

  async findOne(id: number): Promise<Categoria> {
    const categoria = await this.categoriasRepository.findOne({
      where: { id, activa: true }
    });

    if (!categoria) {
      throw new NotFoundException(`Categoría con ID ${id} no encontrada`);
    }

    return categoria;
  }

  async create(createCategoriaDto: CreateCategoriaDto): Promise<Categoria> {
    // Verificar si ya existe una categoría con el mismo nombre
    const existe = await this.categoriasRepository.findOne({
      where: { nombre: createCategoriaDto.nombre }
    });

    if (existe) {
      throw new Error('Ya existe una categoría con ese nombre');
    }

    const categoria = this.categoriasRepository.create(createCategoriaDto);
    return await this.categoriasRepository.save(categoria);
  }

  async update(id: number, updateCategoriaDto: UpdateCategoriaDto): Promise<Categoria> {
    const categoria = await this.findOne(id);
    
    // Si se actualiza el nombre, verificar que no exista otro con el mismo nombre
    if (updateCategoriaDto.nombre && updateCategoriaDto.nombre !== categoria.nombre) {
      const existe = await this.categoriasRepository.findOne({
        where: { nombre: updateCategoriaDto.nombre }
      });

      if (existe) {
        throw new Error('Ya existe una categoría con ese nombre');
      }
    }

    const updated = this.categoriasRepository.merge(categoria, updateCategoriaDto);
    return await this.categoriasRepository.save(updated);
  }

  async remove(id: number): Promise<void> {
    const categoria = await this.findOne(id);
    categoria.activa = false;
    await this.categoriasRepository.save(categoria);
  }
}