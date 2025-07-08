# IRIS CLI 🚀

El CLI de IRIS es una herramienta de línea de comandos diseñada para estandarizar y acelerar la creación de funciones AWS Lambda en IRIS. Genera proyectos listos para producción con una arquitectura de capas bien definida y las mejores prácticas de la industria.

## ✨ Características Principales

- **Arquitectura de Capas**: Todos los proyectos se generan con una separación clara entre `Domain`, `Application` e `Infrastructure`.
- **Calidad de Código Integrada**: Configuraciones listas para usar de **ESLint** (TypeScript), y **Checkstyle** (Java).
- **Testing desde el Día Cero**: Proyectos listos para pruebas con **Jest** (TypeScript) y **JUnit 5 + Mockito** (Java).
- **Logging Estructurado**: Logs en formato JSON para una mejor observabilidad en CloudWatch.
- **Soporte para Múltiples Tecnologías**: Genera proyectos para Node.js (TypeScript), Java (JVM 11/21) y Quarkus (JVM 11/21, GraalVM).

## ⚙️ Instalación

1.  **Clona el repositorio**:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2.  **Crea y activa un entorno virtual de Python**:
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala el CLI en modo editable**:
    ```bash
    pip install --editable .
    ```

4.  **Verifica la instalación**:
    ```bash
    iris --help
    ```

## 🚀 Uso y Ejemplos

El comando principal es `iris scaffold`. A continuación se muestran ejemplos para cada tipo de proyecto.

### 1. Node.js (TypeScript)

Genera un proyecto de Node.js con TypeScript, Jest, ESLint y esbuild.

**Comando:**
```bash
iris scaffold node --name mi-lambda-ts --lang ts --project-prefix CL00079-CustomerInfoSiif
```

### 2. Java (JVM)

Genera un proyecto de Java con Maven, JUnit 5, Mockito, Checkstyle y logging JSON. Puedes especificar la versión de Java (11 o 21).

**Comandos:**
```bash
# Java 11 (por defecto)
iris scaffold java --name mi-lambda-java-11 --project-prefix CL00079-CustomerInfoSiif

# Java 21
iris scaffold java --name mi-lambda-java-21 --project-prefix CL00079-CustomerInfoSiif --java-version 21
```

### 3. Quarkus (Invocación por Evento)

Genera una Lambda de Quarkus que responde a invocaciones directas (ej. SQS, S3). Puedes especificar la versión de Java (11 o 21) y si es una imagen nativa de GraalVM.

**Comandos:**
```bash
# Quarkus JVM 11 (por defecto)
iris scaffold quarkus --name mi-lambda-quarkus-evento-11 --project-prefix CL00079-CustomerInfoSiif

# Quarkus JVM 21
iris scaffold quarkus --name mi-lambda-quarkus-evento-21 --project-prefix CL00079-CustomerInfoSiif --java-version 21

# Quarkus GraalVM (imagen nativa)
iris scaffold quarkus --name mi-lambda-quarkus-graal --project-prefix CL00079-CustomerInfoSiif --graal
```

### 4. Quarkus (API REST)

Genera una API REST completa con Quarkus, lista para ser expuesta a través de API Gateway. Puedes especificar la versión de Java (11 o 21) y si es una imagen nativa de GraalVM.

**Comandos:**
```bash
# Quarkus REST JVM 11 (por defecto)
iris scaffold quarkus --name mi-api-quarkus-11 --type rest --project-prefix CL00079-CustomerInfoSiif

# Quarkus REST JVM 21
iris scaffold quarkus --name mi-api-quarkus-21 --type rest --project-prefix CL00079-CustomerInfoSiif --java-version 21

# Quarkus REST GraalVM (imagen nativa)
iris scaffold quarkus --name mi-api-quarkus-graal --type rest --project-prefix CL00079-CustomerInfoSiif --graal
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas añadir una nueva plantilla o mejorar una existente, por favor sigue el flujo de trabajo estándar de Git (crea una rama, haz tus cambios y abre un Pull Request).

## 📄 Licencia

Este proyecto es propiedad de IRIS. Uso interno únicamente.
