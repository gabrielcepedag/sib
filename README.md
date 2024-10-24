# Construcción de Pipeline con YFinance, Airbyte, Clickhouse, DBT y Airflow

Este proyecto tiene como objetivo integrar y validar múltiples fuentes de información sobre bancos que cotizan en la bolsa de valores de los Estados Unidos. Se utiliza un pipeline de datos que incluye la extracción de la información con Yfinance, un entorno de landing zone en PostgreSQL, un almacén OLAP en ClickHouse, herramientas de integración como Airbyte, validación y transformación de datos con DBT, y orquestación del pipeline con Airflow.

Este es el diagrama de la arquitectura del ETL con las tecnologías utilizadas:

![Arquitectura del ETL](https://github.com/user-attachments/assets/f2a020cf-3519-4836-94e3-f50b94801dad)

Y este está el diagrama del ETL al final de la implementación desde la vista de grafos del Dag Airflow:

Este es el DAG que ejecuta la extracción y la carga de la data desde el source hasta el stage:
![ELT Dag](https://github.com/user-attachments/assets/f7d53a23-bf82-494f-a6cb-5f03ac15934d)

Este es el DAG que ejecuta las transformaciones con DBT cuando hubo algún cambio en el datawarehouse:
![DBT jobs](https://github.com/user-attachments/assets/e5f1e019-eb41-4c33-8864-d2612c030cd4)


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

## 3. Ejecutar los contenedores

  En esta paso usted puede proceder con la ejecución de los contenedores de ambos proyectos para ello, siga las siguientes instrucciones:
     
  1. Correr las demás herramientas:

   ```bash
    cd sib/
   ```
   ```bash
    docker-compose up -d
   ```

   2. Este comando descarga el archivo docker-compose.yaml y corre Airbyte. Por lo tanto, primero lo ejecutamos para descargar el archivo:

   ```bash
    ./airbyte/run-ab-platform.sh
   ```

   3. Luego, agregamos la nueva red en el docker-compose.yml del proyecto de Airbyte como se muestra en adelante:
   
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
   
## 4. Configurar conector de Airbyte desde la UI

Inicia en la UI de Airbyte accediendo a http://localhost:8000/ en tu navegador. El usuario y contraseña por defecto es airbyte y password. Luego:

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

4. **Copiar Connection-id para poder ejecutar el sync desde Airflow**:

   - En la URL de la conexión copia lo que está luego del path `/connections/`
   - Pega ese ID en la variable de entorno `AIRBYTE_CONNECTION_ID`
   - Reinicia el proyecto principal

    ```bash
    cd sib/
    docker-compose up down
    docker-compose up -d
   ```

## 5. Configurar conector de Airbyte desde la UI en Airflow

Inicia en la UI de Airflow accediendo a http://localhost:8080/ en tu navegador. El usuario y contraseña por defecto es airflow. Luego:

   - Ve al apartado de Conexiones y click en `+ New connection`.
   - Elige el tipo de conexión de Airbyte
   - Ajusta los campos con la siguiente guia:
     
     ```bash
       Connection Id = airbyte_conn_id
       host = airbyte-proxy
       login = airbyte
       password = password
       port = 8001
     ```
     
   - Click en `Save`.
## 6. Orquestación con Airflow

Ahora que todo está configurado, es tiempo de correr el pipeline!

- En la UI de Airflow, ve al apartado de "DAGs"
- Localiza `extract_info_banks_stocks` y click en "Trigger DAG".

Esto iniciará el pipeline completo, comenzando con la extracción de la data desde yfinance, almacenando esa data en PostgreSQL, luego ejecutando el proceso de `sync` de Airbyte para transportar la data cruda desde Postgres a Clickhouse. Y por último, corriendo las validaciones y transformaciones con DBT para tener como resultado la data para ser utilizada por los analistas.

- Confirma el estado de la sincronización en Airbyte.
- Luego de que el job `send_to_datawarehouse` se ejecute, puedes observar la data en clickhouse en el esquema definido en la conexión del destino. Si no definiste esquema estará en el esquema `_airbyte_internal_`.
- Una vez que el proceso anterior se complete, se ejecutará un trigger que ejecutará el DAG `execute_dbt_jobs`. Este es el encargado de ejecutar las validaciones y transformaciones de los datos en stage.
- Cuando el proceso anterior culmine, puedes observar en la base de datos de clickhouse en el esquema `dwh` estarán los modelos y vistas creadas con DBT.


# Demo visual en Youtube

[![Demo Pipeline](https://img.youtube.com/vi/aOJAdJFkF28/0.jpg)](https://www.youtube.com/watch?v=aOJAdJFkF28)






