import {
  TableRow,
  TableCell,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Product } from "@/lib/definitions";
import { formatCurrency } from "@/lib/utils";
import { MoreHorizontal, Eye, Pencil, Trash2 } from "lucide-react";

interface ProductRowProps {
  product: Product;
  onView: (product: Product) => void;
  onEdit: (product: Product) => void;
  onDelete: (product: Product) => void;
}

export const ProductRow = ({ product, onView, onEdit, onDelete }: ProductRowProps) => {
  const categoryNames = product.categorias?.map(c => c.nombre).join(', ') || 'N/A';
  const status = product.stockDisponible > 0 ? "En Stock" : "Agotado";

  return (
    <TableRow key={product.id}>
      <TableCell>
        <div className="h-10 w-10 bg-gray-100 rounded-md flex items-center justify-center">
          {product.imagenes && product.imagenes.length > 0 ? (
            <img src={product.imagenes.find(img => img.esPrincipal)?.url} alt={product.nombre} className="h-full w-full object-cover rounded-md" />
          ) : (
            <span className="text-xs text-gray-500">IMG</span>
          )}
        </div>
      </TableCell>
      <TableCell className="font-medium">{product.nombre}</TableCell>
      <TableCell>{categoryNames}</TableCell>
      <TableCell>{formatCurrency(product.precio)}</TableCell>
      <TableCell>{product.stockDisponible}</TableCell>
      <TableCell>
        <Badge variant={product.stockDisponible > 0 ? "default" : "destructive"}>
          {status}
        </Badge>
      </TableCell>
      <TableCell>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => onView(product)}>
              <Eye className="mr-2 h-4 w-4" />
              Ver
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => onEdit(product)}>
              <Pencil className="mr-2 h-4 w-4" />
              Editar
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => onDelete(product)} className="text-red-500">
              <Trash2 className="mr-2 h-4 w-4" />
              Eliminar
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </TableCell>
    </TableRow>
  );
};