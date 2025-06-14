# CLI Lambda Generator

Generador de scaffolding para funciones [AWS Lambda](https://aws.amazon.com/lambda/) en [Java](https://www.java.com/) usando [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) y arquitectura hexagonal. Ideal para pruebas locales con Docker.

Compatible con:
- [Java 11 (Temurin)](https://adoptium.net/)
- [Maven](https://maven.apache.org/)
- [Docker](https://www.docker.com/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)


## ✅ Requisitos

- [Java 11](https://adoptium.net/)
- [Apache Maven](https://maven.apache.org/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.8+](https://www.python.org/)

Para probar funciones localmente se requiere Docker configurado correctamente con red y permisos.

## 🐍 Uso del entorno virtual
Se recomienda utilizar un entorno virtual para mantener las dependencias del proyecto aisladas.

1. Crear el entorno virtual

``` bash
python -m venv venv
```

2. Activar el entorno virtual

-  En Windows:
``` bash
venv\Scripts\activate
```
- En Linux/macOS:

``` bash
source venv/bin/activate
```

## 🔧 Instalación

Clona el repositorio y usa instalación editable con [pip](https://pip.pypa.io/):

```bash
pip install --editable .

```

Verificar que el CLI funciona
```bash
cli_lambda --help
```

## ⚙️ Configuración del entorno (env.json)

Para generar automáticamente el script `setup-codeartifact.ps1`, debes configurar tus credenciales de CodeArtifact en un archivo `env.json` ubicado dentro de la carpeta `cli_lambda/`.

Ejemplo

``` json
{
  "domain": "iris",
  "domain_owner": "713823698889",
  "region": "us-east-1",
  "repo_name": "mvn-internal",
  "aws_profile": "dev-tools",
  "server_id": "iris-mvn-internal"
}
```
Este archivo será utilizado por el CLI para renderizar dinámicamente los valores necesarios para autenticar Maven con CodeArtifact.

## 🧪 Cómo usarlo

Una vez instalado, puedes ejecutar el comando para generar una nueva función Lambda en Java:

```bash
cli_lambda java lda-MiLambdaJava
```

Esto generará un proyecto con la siguiente estructura:

### 📁 Estructura generada

```text
lda-MiLambdaJava/
├── pom.xml
├── template.yaml
├── event.json
├── setup-codeartifact.ps1
├── settings-codeartifact.xml
├── src/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   ├── main/
│   │   └── java/com/milambdajava/
│   │       ├── Handler.java
│   │       └── Response.java
│   └── test/
│       └── com/milambdajava/
│           └── HandlerTest.java
```

### ✨ Para probar la función localmente con SAM:

1. Compila el proyecto:
``` bash
sam build
```

2. Ejecuta la función con un evento de prueba:

``` bash
sam local invoke --event event.json
```

### 🛠️ Ejecutar el script para configurar CodeArtifact

Antes de compilar o ejecutar tests si usas dependencias privadas, debes generar el archivo `settings-codeartifact.xml` ejecutando el siguiente script:

```powershell
./setup-codeartifact.ps1
```

Este script:

- Solicita un token temporal a AWS CodeArtifact

- Genera `settings-codeartifact.xml` con las credenciales necesarias

- Permite que Maven pueda descargar dependencias privadas desde el repositorio `iris-mvn-internal`

### ✅ Ejecutar pruebas unitarias

Si usas dependencias internas de IRIS, recuerda compilar con el archivo settings-codeartifact.xml:
``` bash
mvn test --settings settings-codeartifact.xml
```

Si no usas dependencias internas, puedes ejecutar simplemente:
``` bash
mvn test
```

### ℹ️ Agregar dependencias IRIS (opcional)
Si necesitas bibliotecas internas de IRIS, agrégalas al pom.xml como cualquier dependencia de Maven:

``` xml
<dependency>
  <groupId>com.iris</groupId>
  <artifactId>iris-core-utils</artifactId>
  <version>1.4.2</version>
</dependency>
```

Estas estarán disponibles si generaste previamente el archivo settings-codeartifact.xml con el script:

``` bash
./setup-codeartifact.ps1
```

---
