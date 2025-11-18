﻿import { z } from "zod";

export const dimensionesSchema = z.object({
    largoCm: z.coerce.number().positive({ message: "El largo debe ser positivo." }),
    anchoCm: z.coerce.number().positive({ message: "El ancho debe ser positivo." }),
    altoCm: z.coerce.number().positive({ message: "El alto debe ser positivo." }),
});

export const ubicacionSchema = z.object({
    street: z.string().min(1, "La calle es requerida."),
    city: z.string().min(1, "La ciudad es requerida.").regex(/^[a-zA-Z\s'-]+$/, {
        message: 'La ciudad solo puede contener letras y espacios.',
      }),
    state: z.string().min(1, "La provincia es requerida.").regex(/^[a-zA-Z\s'-]+$/, {
        message: 'La provincia solo puede contener letras y espacios.',
      }),
    postalCode: z.string().min(1, "El código postal es requerido.").regex(/^([A-Z]{1}\d{4}[A-Z]{3})$/, {
        message: 'Formato de CPA inválido (ej: C1024AAB).',
      }),
    country: z.string().length(2, { message: "Debe ser un código de 2 letras (ej: AR)." }),
});

export const productSchema = z.object({
    nombre: z.string().min(2, "El nombre debe tener al menos 2 caracteres."),
    descripcion: z.string().optional(),
    precio: z.coerce.number().min(0, "El precio no puede ser negativo."),
    stockInicial: z.coerce.number().int().min(0, "El stock debe ser un entero no negativo."),
    dimensiones: dimensionesSchema,
    ubicacion: ubicacionSchema,
    categoriaIds: z.array(z.coerce.number()).optional(),
});

// No necesitamos un tipo de entrada separado, podemos inferirlo directamente
// export type ProductInput = z.infer<typeof productSchema>;

export const categorySchema = z.object({
    nombre: z.string().min(2, "Mínimo 2 caracteres"),
});
export type CategoryInput = z.infer<typeof categorySchema>;

export const reservationSchema = z.object({
    idCompra: z.string().min(1, "Obligatorio"),
    productos: z.array(
        z.object({
            idProducto: z.coerce.number().int().positive(),
            cantidad: z.coerce.number().int().positive(),
        })
    ).min(1, "Agregá al menos un producto"),
});
export type ReservationInput = z.infer<typeof reservationSchema>;
