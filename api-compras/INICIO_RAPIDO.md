# ⚡ INICIO RÁPIDO - Para tus compañeros

## 🚀 Instalación Express (5 minutos)

```bash
# 1. Clonar
git clone https://github.com/Maximo-Vazquez/DesarrolloAPP.git
cd DesarrolloAPP

# 2. Entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Instalar todo
pip install -r requirements.txt

# 4. Migrar BD
python manage.py migrate

# 5. Crear datos de prueba (IMPORTANTE)
python crear_datos_prueba.py

# 6. VERIFICAR ✅ (IMPORTANTE)
python verificar_instalacion.py
```

## ✅ Si ves esto, estás listo:

```
🎉 ¡TODO ESTÁ CORRECTAMENTE INSTALADO! 🎉
```

## 🏃 Correr el proyecto:

```bash
python manage.py runserver
```

Abre: **http://127.0.0.1:8000/api/docs/** 

## 🧪 Probar que todo funciona:

```bash
python tests/test_apis_mock_completo.py
```

Deberías ver: **"🎉 ¡TODAS LAS PRUEBAS PASARON! 🎉"**

---

## ❌ Problemas comunes:

### "No se reconoce python"
```bash
# Verifica que Python está instalado
python --version
# Si no funciona, reinstala Python desde python.org
```

### "No se puede activar venv"
```powershell
# PowerShell: Cambiar política de ejecución
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Module not found"
```bash
# Asegúrate que venv está activo (debes ver (venv) en la terminal)
# Luego reinstala
pip install -r requirements.txt
```

### "Error de migraciones"
```bash
python manage.py migrate
```

---

## 📖 Documentación completa:

Lee **INSTALACION.md** para instrucciones detalladas.

---

## 🆘 Si nada funciona:

1. ✅ Verifica que Python 3.12+ está instalado
2. ✅ Verifica que el entorno virtual está activo (ves `(venv)`)
3. ✅ Ejecuta: `python verificar_instalacion.py`
4. ✅ Lee los errores que te muestra
5. ✅ Consulta `INSTALACION.md`
6. 📞 Contacta al equipo

---

**¡Listo para desarrollar! 💻**
