# ⚠️ IMPORTANTE: Migraciones y Datos de Prueba

## 🔴 **Problema Común: "No hay datos en la base de datos"**

### ❓ ¿Por qué no aparecen datos?

Si tu compañero clona el proyecto y NO ejecuta los siguientes pasos, **NO habrá datos** en la base de datos:

1. ❌ **Sin migraciones** → No se crean las tablas
2. ❌ **Sin datos de prueba** → Las tablas están vacías
3. ❌ **Resultado** → Las APIs Mock devuelven listas vacías

---

## ✅ **Solución: Pasos Obligatorios Después de Clonar**

### **Opción A - Automática (Recomendada):**

Ejecuta este comando que hace todo automáticamente:

```bash
python crear_datos_prueba.py
```

Este script:
- ✅ Crea automáticamente las tablas (si no existen)
- ✅ Crea 4 categorías de productos
- ✅ Crea 15 productos con stock
- ✅ Crea 4 métodos de transporte
- ✅ No duplica datos si ya existen

### **Opción B - Manual (Paso a Paso):**

```bash
# 1. Crear las tablas en la base de datos
python manage.py migrate

# 2. Crear los datos de prueba
python crear_datos_prueba.py
```

---

## 🔍 **¿Cómo verificar que todo está bien?**

```bash
python verificar_instalacion.py
```

Deberías ver:
```
✅ Datos de prueba encontrados:
ℹ️    - Productos: 15
ℹ️    - Categorías: 4
ℹ️    - Métodos de transporte: 4
```

---

## 📊 **¿Qué datos se crean?**

### **Categorías (4):**
- Electrónica
- Ropa
- Hogar
- Deportes

### **Productos (15):**
- Laptop Dell XPS 13 - $1299.99 (Stock: 15)
- iPhone 15 Pro - $999.00 (Stock: 25)
- Samsung Galaxy S24 - $849.00 (Stock: 30)
- iPad Air - $599.00 (Stock: 20)
- AirPods Pro - $249.00 (Stock: 50)
- Camiseta Nike - $29.99 (Stock: 100)
- Zapatillas Adidas - $89.99 (Stock: 40)
- Jeans Levis - $79.99 (Stock: 60)
- Lámpara LED - $39.99 (Stock: 35)
- Cafetera Nespresso - $199.00 (Stock: 15)
- Bicicleta Mountain Bike - $499.00 (Stock: 10)
- Pelota de Fútbol - $29.99 (Stock: 80)
- Raqueta de Tenis - $149.00 (Stock: 25)
- Mochila deportiva - $49.99 (Stock: 45)
- Smartwatch Samsung - $299.00 (Stock: 20)

### **Métodos de Transporte (4):**
- 🚛 **Transporte Terrestre** (road): $10 base + $2/kg, 3-7 días
- ✈️ **Transporte Aéreo** (air): $50 base + $10/kg, 1-3 días
- 🚢 **Transporte Marítimo** (sea): $5 base + $0.50/kg, 15-30 días
- 🚆 **Transporte Ferroviario** (rail): $8 base + $1.50/kg, 5-10 días

---

## 🚨 **Errores Comunes**

### Error 1: `no such table: stockApi_producto`
**Causa:** No se ejecutaron las migraciones  
**Solución:** 
```bash
python manage.py migrate
```

### Error 2: APIs devuelven listas vacías `{"data": []}`
**Causa:** No hay datos en la base de datos  
**Solución:**
```bash
python crear_datos_prueba.py
```

### Error 3: `ImproperlyConfigured: Requested setting INSTALLED_APPS`
**Causa:** El entorno virtual no está activado  
**Solución:**
```bash
.\venv\Scripts\Activate.ps1  # Windows PowerShell
source venv/bin/activate      # Linux/Mac
```

---

## 📝 **Instrucciones para tu Equipo**

Copia y pega esto en el chat del equipo:

```
👋 ¡Hola equipo!

Después de hacer `git pull`, SIEMPRE ejecuten:

1️⃣ Activar entorno virtual:
   .\venv\Scripts\Activate.ps1

2️⃣ Instalar/actualizar dependencias:
   pip install -r requirements.txt

3️⃣ Aplicar migraciones:
   python manage.py migrate

4️⃣ Crear/actualizar datos de prueba:
   python crear_datos_prueba.py

5️⃣ Verificar que todo funciona:
   python verificar_instalacion.py

Si sale "🎉 ¡TODO ESTÁ CORRECTAMENTE INSTALADO! 🎉", ya pueden trabajar.

Si tienen problemas, revisen: INSTALACION.md o MIGRACIONES_Y_DATOS.md
```

---

## 🎯 **Resumen Visual**

```
┌─────────────────────────────────────────┐
│  1. git pull                            │
│     ↓                                   │
│  2. Activar venv                        │
│     ↓                                   │
│  3. pip install -r requirements.txt     │
│     ↓                                   │
│  4. python manage.py migrate            │
│     ↓                                   │
│  5. python crear_datos_prueba.py        │  ← ⚠️ IMPORTANTE
│     ↓                                   │
│  6. python verificar_instalacion.py     │  ← ✅ VERIFICAR
│     ↓                                   │
│  7. python manage.py runserver          │
└─────────────────────────────────────────┘
```

---

## 💡 **Tips Pro**

1. **Siempre verifica** después de hacer `git pull`:
   ```bash
   python verificar_instalacion.py
   ```

2. **Si la BD se corrompe**, bórrala y recréala:
   ```bash
   # ⚠️ CUIDADO: Esto borra TODOS los datos
   rm db.sqlite3  # Linux/Mac
   del db.sqlite3  # Windows
   
   python manage.py migrate
   python crear_datos_prueba.py
   ```

3. **Para desarrollo local**, los datos de prueba son suficientes. Para producción, se usarán datos reales.

---

**¿Dudas?** Revisa `INSTALACION.md` o pregunta al equipo.
