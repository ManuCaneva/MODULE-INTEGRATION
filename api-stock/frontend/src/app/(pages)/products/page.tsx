// frontend/src/app/(pages)/products/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react'; // <-- Importar useSession
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { listarProductos, getCategories, eliminarProducto } from '@/lib/api';
import { Product, Category } from '@/lib/definitions';
import { ProductRow } from '@/components/shared/ProductRow';
import { ConfirmModal } from '@/components/shared/ConfirmModal';

const ProductsPage = () => {
  const router = useRouter();
  const { data: session, status } = useSession(); // <-- Obtener sesión y status
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true); // Estado de carga general
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  // --- Efecto principal para manejar autenticación y carga inicial ---
  useEffect(() => {
    // Si la sesión aún está cargando, esperar
    if (status === 'loading') {
      setLoading(true); // Indicar carga
      return; 
    }

    // Si no está autenticado, redirigir al inicio (o login)
    if (status === 'unauthenticated') {
      router.push('/'); 
      return; 
    }

    // Si está autenticado, cargar datos iniciales
    if (status === 'authenticated') {
      fetchProducts(1, '', 'all'); // Cargar primera página sin filtros
      fetchCategories();
    }
  }, [status, router]); // Depender del estado de la sesión

  // --- Efecto para recargar productos al cambiar filtros/página ---
  // Se ejecuta solo si está autenticado y cambian las dependencias
  useEffect(() => {
    if (status === 'authenticated') {
      fetchProducts(currentPage, searchTerm, categoryFilter);
    }
    // No incluir fetchProducts en las dependencias para evitar bucles
  }, [currentPage, searchTerm, categoryFilter, status]); 

  const fetchProducts = async (page: number, search: string, category: string) => {
    setLoading(true);
    try {
      const categoryId = category !== 'all' ? parseInt(category) : undefined;
      // Asumimos que listarProductos usa el token de fetcher
      const paginatedProducts = await listarProductos(page, 10, search, categoryId);
      setProducts(paginatedProducts.items);
      setTotalPages(Math.ceil(paginatedProducts.total / 10));
    } catch (error) {
      console.error('Error fetching products:', error);
      // Podrías mostrar un mensaje de error al usuario
      setProducts([]); // Limpiar productos en caso de error
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      // Asumimos que getCategories usa el token de fetcher
      const cats = await getCategories();
      setCategories(cats);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handlePageChange = (page: number) => {
    if (page > 0 && page <= totalPages) {
      setCurrentPage(page);
    }
  };
  
  // --- Funciones de búsqueda y filtro resetean la página a 1 ---
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1); // Resetear a página 1 al buscar
  };

  const handleCategoryChange = (value: string) => {
    setCategoryFilter(value);
    setCurrentPage(1); // Resetear a página 1 al filtrar
  };
  // -----------------------------------------------------------

  const handleView = (product: Product) => {
    router.push(`/products/${product.id}`);
  };

  const handleEdit = (product: Product) => {
    router.push(`/products/${product.id}/edit`);
  };

  const handleDelete = (product: Product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (selectedProduct) {
      try {
        // Asumimos que eliminarProducto usa el token de fetcher
        await eliminarProducto(selectedProduct.id);
        // Volver a cargar los productos de la página actual
        fetchProducts(currentPage, searchTerm, categoryFilter); 
      } catch (error) {
        console.error('Error deleting product:', error);
      }
      setIsModalOpen(false);
      setSelectedProduct(null);
    }
  };

  const SkeletonRow = () => (
    <TableRow>
      <TableCell className="h-12 w-12 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></TableCell>
      <TableCell className="h-4 w-1/4 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></TableCell>
      <TableCell className="h-4 w-1/4 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></TableCell>
      <TableCell className="h-4 w-1/6 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></TableCell>
      <TableCell className="h-4 w-1/6 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></TableCell>
      <TableCell className="h-4 w-1/12 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></TableCell>
      <TableCell className="flex h-10 items-center justify-end space-x-1">
          <div className="h-8 w-8 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></div>
          <div className="h-8 w-8 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></div>
          <div className="h-8 w-8 animate-pulse rounded-md bg-gray-200 dark:bg-gray-700"></div>
      </TableCell>
    </TableRow>
  );

  // --- Renderizado Condicional ---
  // Mostrar carga mientras se verifica sesión o se cargan datos iniciales
  if (status === 'loading' || (status === 'authenticated' && loading && products.length === 0 && currentPage === 1)) {
      return (
          <div className="container mx-auto py-10">
              <h1 className="text-3xl font-bold mb-6">Cargando Productos...</h1>
              <div className="rounded-md border">
                  <Table>
                      <TableHeader>
                          <TableRow>
                              <TableHead>Imagen</TableHead>
                              <TableHead>Nombre</TableHead>
                              <TableHead>Categoría</TableHead>
                              <TableHead>Precio</TableHead>
                              <TableHead>Stock</TableHead>
                              <TableHead>Estado</TableHead>
                              <TableHead><span className="sr-only">Acciones</span></TableHead>
                          </TableRow>
                      </TableHeader>
                      <TableBody>
                          {Array.from({ length: 5 }).map((_, i) => <SkeletonRow key={i} />)}
                      </TableBody>
                  </Table>
              </div>
          </div>
      );
  }

  // Si después de cargar sabemos que no está autenticado (aunque el useEffect ya debería haber redirigido)
  if (status === 'unauthenticated') {
      return (
          <div className="container mx-auto py-10 text-center">
              <p>Redirigiendo al inicio de sesión...</p> 
          </div>
      );
  }

  // --- Renderizado Principal (cuando está autenticado) ---
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Productos</h1>
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-2">
          <Input
            placeholder="Buscar productos..."
            value={searchTerm}
            onChange={handleSearchChange} // Usar handler que resetea página
            className="max-w-sm"
          />
          <Select onValueChange={handleCategoryChange} value={categoryFilter}> {/* Usar handler que resetea página */}
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Filtrar por categoría" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas las categorías</SelectItem>
              {categories.map((category) => (
                <SelectItem key={category.id} value={String(category.id)}>
                  {category.nombre}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <Button onClick={() => router.push('/products/new')}>Agregar Producto</Button>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {/* ... Encabezados sin cambios ... */}
             <TableRow>
              <TableHead>Imagen</TableHead>
              <TableHead>Nombre</TableHead>
              <TableHead>Categoría</TableHead>
              <TableHead>Precio</TableHead>
              <TableHead>Stock</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead>
                <span className="sr-only">Acciones</span>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {/* Mostrar esqueletos solo si está cargando y es la primera carga */}
            {loading && products.length === 0 ? (
                Array.from({ length: 5 }).map((_, i) => <SkeletonRow key={i} />)
            ) : products.length > 0 ? (
              products.map((product) => (
                <ProductRow
                  key={product.id}
                  product={product}
                  onView={handleView}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={7} className="h-24 text-center">
                  No se encontraron productos con los filtros actuales.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      {/* Paginación (mostrar solo si no está cargando y hay más de una página) */}
      {!loading && totalPages > 1 && (
        <div className="flex items-center justify-end space-x-2 py-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Anterior
          </Button>
          <span className="text-sm">
            Página {currentPage} de {totalPages}
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Siguiente
          </Button>
        </div>
      )}
      <ConfirmModal
        open={isModalOpen}
        onOpenChange={setIsModalOpen}
        title="¿Estás seguro?"
        description={`Esta acción eliminará permanentemente el producto "${selectedProduct?.nombre}".`}
        onConfirm={handleDeleteConfirm}
      />
    </div>
  );
};

export default ProductsPage;