# Construcción de ETL con YFinance, Airbyte, Clickhouse, DBT y Airflow

Este proyecto tiene como objetivo integrar y validar múltiples fuentes de información sobre bancos que cotizan en la bolsa de valores de los Estados Unidos. Se utiliza un pipeline de datos que incluye la extracción de la información con Yfinance, un entorno de landing zone en PostgreSQL, un almacén OLAP en ClickHouse, herramientas de integración como Airbyte, validación y transformación de datos con DBT, y orquestación del pipeline con Airflow.

Este es el diagrama de la arquitectura del ETL con las tecnologías utilizadas:

![Arquitectura del ETL](https://github.com/user-attachments/assets/f2a020cf-3519-4836-94e3-f50b94801dad)

Y este está el diagrama del ETL al final de la implementación desde la vista de grafos del Dag Airflow:

![ETL Dag](https://github.com/user-attachments/assets/65565df8-8f06-4843-addb-14dc21e7d466)


## Tecnologías usadas:
- **PostgreSQL**: Para almacenar datos crudos extraídos desde el API.
- **ClickHouse**: Como almacén centralizado de datos curados.
- **Airbyte**: Para la integración de datos entre PostgreSQL y ClickHouse.
- **DBT**: Para validar y transformar los datos.
- **Airflow**: Para orquestar y automatizar el pipeline de datos.
- **yfinance**: Para la extracción de información sobre los bancos.

## Requerimientos previos:

Antes de comenzar con esta integración, asegúrate de tener las siguientes instrucciones listas:

1. **Git**: Si no lo tiene instalado, descárgalo e instálalo desde [Git][[https://docs.docker.com/get-docker/](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)] siguiendo la documentación oficial para tu Sistema Operativo.

2. **Docker y Docker Compose (Docker Desktop)**: Si no lo tiene instalado, descárgalo e instálalo desde [Docker][https://docs.docker.com/get-docker/] siguiendo la documentación oficial para tu Sistema Operativo.

## 1. Configurar el ambiente para el proyecto

Descargue el proyecto en su máquina local siguiendo estos pasos:

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/gabrielcepedag/sib.git
   ```
2. **Clona el repositorio de AirByte**:
   ```bash
   git clone https://github.com/airbytehq/airbyte.git
   ```
3. **Crea un archivo .env en la raíz del proyecto con estas variables un ejemplo del valor**:
   ```bash
   cd sib/
   ```

   ```bash
   #POSTGRESQL
    DB_HOST=localhost
    POSTGRES_USER=sib_user
    POSTGRES_PASSWORD=sib_user
    POSTGRES_DB=landing_zone
    POSTGRES_PORT=5432
    
    #CLICKHOUSE
    CLICKHOUSE_HTTP_PORT=8123
    CLICKHOUSE_TCP_PORT=9000
    
    #AIRFLOW
    AIRFLOW_DB=airflow
    AIRFLOW_WEB_PORT=8080
    #id - u en el host
    AIRFLOW_UID=501
   ```

### 2. Configurar la red para docker
  
  Dado que el servicio de Airbyte se encuentra en otro proyecto, es necesario crear una red externa de forma que
  desde el contenedor en donde se ejecuta Airflow, se tenga comunicación con el contenedor que maneja las conexiones
  de Airbyte. Para ello siga los siguientes pasos: 

  1. Crear la red en docker
     
   ```bash
   docker network create airbyte_airflow
   ```

   2. Agregar la nueva red en el docker-compose.yml del proyecto de Airbyte como se muestra en adelante:
   
   ```bash
   networks:
    airbyte_airflow:
    external: true
   ```

  3. Agregar la red en el servicio de airbyte-proxy:
   
   ```bash
    airbyte-proxy:
      networks:
      - airbyte_airflow
   ```

## 3. Ejecutar los contenedores

  En esta paso usted puede proceder con la ejecución de los contenedores de ambos proyectos para ello, siga las siguientes instrucciones:

  1. Correr AirByte:

   ```bash
    ./airbyte/run-ab-platform.sh
   ```
     
  2. Correr las demás herramientas:

   ```bash
    cd sib/
   ```
   ```bash
    docker-compose up -d
   ```
## 4. Configurar conector de Airbyte desde la UI

Inicia en la UI de Airbyte accediendo a http://localhost:8000/ en tu navegador. Luego:

  1. **Crea una fuente (source)**:

   - Ve al apartado de Sources y click en `+ New source`.
   - Busca el conector para `Postgres`.
   - Ajusta los campos según tus variables de entorno. Una guía puede ser:
     
     ```bash
       host = postgres-db
       port = 5432
       Database Name = landing_zone
       username = sib_user
       password = sib_user
     ```
   - Click en `Set up source`.

2. **Crea un destino**:

   - Ve al apartado de Destinos y click en `+ New destination`.
   - Busca el conector par `Clickhouse`.
    - Ajusta los campos según tus variables de entorno. Una guía puede ser:
      
     ```bash
       host = localhost
       port = 8123
       DB Name = stage
       user = default
     ```
   - Click en `Set up destination`.

3. **Crear una conexión**:

   - Ve al apartado de Conexiones y click en `+ New connection`.
   - Selecciona la fuente y el destino que acabas de crear.
   - Coloca los detalles de las conexiones como sea necesario.
   - Click en `Set up connection`.

Estás listo! Tu conexión está configurada y lista para usarse!🎉 











