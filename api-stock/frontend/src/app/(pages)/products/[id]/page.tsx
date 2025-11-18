import { obtenerProductoPorId } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import { notFound } from 'next/navigation';
import { getServerSession, Session } from 'next-auth/next';
import { authOptions } from '@/app/api/auth/[...nextauth]/route';

interface CustomSession extends Session {
    accessToken?: string;
}

export default async function ProductDetailPage({ params }: { params: { id: string } }) {
    const session: CustomSession | null = await getServerSession(authOptions);
    const token = session?.accessToken;

    const id = parseInt(params.id);
    const product = await obtenerProductoPorId(id, token);

    if (!product) {
        notFound();
    }

    const status = product.stockDisponible > 0 ? 'En Stock' : 'Agotado';

    return (
        <div className="container mx-auto py-10">
            <Breadcrumb>
                <BreadcrumbList>
                    <BreadcrumbItem>
                        <BreadcrumbLink href="/products">Productos</BreadcrumbLink>
                    </BreadcrumbItem>
                    <BreadcrumbSeparator />
                    <BreadcrumbItem>
                        <BreadcrumbPage>{product.nombre}</BreadcrumbPage>
                    </BreadcrumbItem>
                </BreadcrumbList>
            </Breadcrumb>

            <div className="grid md:grid-cols-2 gap-8 mt-6">
                <div>
                    <Card>
                        <CardContent className="p-4">
                            {product.imagenes && product.imagenes.length > 0 ? (
                                <img
                                    src={product.imagenes.find((img) => img.esPrincipal)?.url}
                                    alt={product.nombre}
                                    className="w-full h-auto object-cover rounded-lg shadow-lg"
                                />
                            ) : (
                                <div className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center">
                                    <span className="text-gray-500">Sin imagen</span>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
                <div>
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-3xl font-bold">{product.nombre}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-gray-600 mt-2 text-lg">{product.descripcion}</p>
                            <div className="flex items-center mt-4">
                                <span className="text-3xl font-bold text-blue-600">{formatCurrency(product.precio)}</span>
                                <Badge variant={product.stockDisponible > 0 ? 'default' : 'destructive'} className="ml-4 text-lg px-4 py-1">
                                    {status}
                                </Badge>
                            </div>
                            <div className="mt-6">
                                <h3 className="text-xl font-semibold">Categorías</h3>
                                <div className="flex flex-wrap gap-2 mt-2">
                                    {product.categorias?.map((cat) => (
                                        <Badge key={cat.id} variant="secondary" className="text-md">{cat.nombre}</Badge>
                                    ))}
                                </div>
                            </div>
                            <div className="mt-6">
                                <h3 className="text-xl font-semibold">Detalles del Producto</h3>
                                <ul className="list-disc list-inside mt-2 space-y-2 text-gray-700">
                                    {product.pesoKg && <li><strong>Peso:</strong> {product.pesoKg} kg</li>}
                                    {product.dimensiones && (
                                        <li>
                                            <strong>Dimensiones:</strong> {product.dimensiones.largoCm}cm x {product.dimensiones.anchoCm}cm x {product.dimensiones.altoCm}cm
                                        </li>
                                    )}
                                    {product.ubicacion && (
                                        <li>
                                            <strong>Ubicación:</strong> Almacén {product.ubicacion.almacenId}, Pasillo {product.ubicacion.pasillo}, Estantería {product.ubicacion.estanteria}, Nivel {product.ubicacion.nivel}
                                        </li>
                                    )}
                                </ul>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
