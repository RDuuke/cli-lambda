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