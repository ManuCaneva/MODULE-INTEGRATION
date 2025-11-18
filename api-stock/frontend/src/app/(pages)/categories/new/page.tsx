import { CategoryForm } from "../category-form";

export default function NewCategoryPage() {
    return (
        <section className="space-y-4">
            <h1 className="text-xl font-semibold">Nueva categoría</h1>
            <CategoryForm />
        </section>
    );
}