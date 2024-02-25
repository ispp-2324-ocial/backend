# Backend de Ocial

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ispp-2324-ocial_backend&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=ispp-2324-ocial_backend)

## Guía para Poner en Marcha el Repositorio Backend

Esta guía proporciona los pasos necesarios para configurar el entorno y comenzar a utilizar el repositorio backend.

### Preparación del Entorno
Antes de comenzar, asegúrate de tener el entorno adecuado configurado. Sigue estos pasos para preparar el entorno:

1. Preparar WSL:
   Asegúrate de tener Windows Subsystem for Linux (WSL) correctamente configurado en tu sistema. Puedes encontrar instrucciones detalladas sobre cómo configurarlo en la documentación oficial de WSL.
2. Instalar Python:
   Instala Python en tu sistema si aún no lo has hecho. Puedes instalarlo ejecutando el siguiente comando en tu terminal:

```bash
sudo apt install python3 python3-venv
```

### Configuración del Repositorio
Una vez que el entorno esté configurado, sigue estos pasos para configurar el repositorio backend:

1. Clonar el repositorio:
   Clona el repositorio en tu directorio local utilizando el siguiente comando:

```bash
git clone https://github.com/ispp-2324-ocial/backend.git
```
2. Crear Directorio Local y Entorno Virtual:
  A continuación, crea un directorio local para el proyecto y configura un entorno virtual para instalar las dependencias del proyecto:
```bash
# Crear directorio local
mkdir nombre_del_directorio_local
cd nombre_del_directorio_local

# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
source env/bin/activate
```
3. Instalar Dependencias:
   Instala las dependencias del proyecto, incluyendo Django Rest Framework, utilizando el archivo requirements.txt:
```bash
pip install -r requirements.txt
```