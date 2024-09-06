# Documentación de la Estrategia y Solución

## Descripción General del Proyecto
En la actualidad, el manejo de datos personales es una tarea crítica, ya que es fundamental identificar y clasificar esta información para aplicar los controles y restricciones necesarios, minimizando el riesgo de fugas de datos. La clasificación de bases de datos relacionales puede realizarse de dos maneras principales: basándose en el nombre de las tablas y columnas, o escaneando muestras de información contenida en las tablas utilizando tecnologías de Prevención de Pérdida de Datos (DLP). En este proyecto, se opta por la primera opción, centrando la búsqueda en una lista específica de tipos de información a identificar, como `FIRST_NAME`, `LAST_NAME`, `IP_ADDRESS`, `CREDIT_CARD_NUMBER`, `USERNAME`, `EMAIL_ADDRESS` entre otros.

## Estrategia de Implementación

### Enfoque General
Se ha decidido utilizar una arquitectura monolítica debido a que se trata de una aplicación pequeña. Este enfoque simplifica la implementación y el mantenimiento, adecuándose al tamaño y requisitos del proyecto.

### Patrones y Principios
Se han aplicado diversos principios para asegurar que la aplicación esté bien estructurada y sea mantenible. Cada clase y función se ha diseñado con un enfoque específico, evitando responsabilidades múltiples y manteniendo el código modular y claro. El sistema es fácilmente extensible, lo que permite añadir nuevas funcionalidades sin necesidad de modificar el código existente. Se han creado clases abstractas enfocadas en necesidades específicas, y se han utilizado abstracciones para facilitar la comunicación entre las capas, brindando flexibilidad y facilitando el mantenimiento a largo plazo.

### Arquitectura
Se emplea una arquitectura hexagonal para dividir la lógica de la aplicación en capas diferenciadas, facilitando el cambio de base de datos o la integración de nuevas fuentes de datos sin afectar la lógica del negocio. Las capas incluyen:

- **Capa de Aplicación**: Contiene los endpoints y casos de uso, gestionando la lógica del negocio.
- **Capa de Dominio**: Define clases abstractas y modelos que la capa de aplicación utiliza.
- **Capa de Infraestructura**: Maneja la configuración de la base de datos y la implementación de los repositorios.

**Base de Datos**: Se ha optado por una base de datos relacional debido a la estructura rígida y la facilidad de consulta que ofrece, lo que facilita el análisis y la clasificación de la información.

## Detalles de Implementación

### Organización del Código
El código está organizado en tres capas principales:
- **Aplicación**: Contiene la lógica de negocio y los casos de uso. Incluye los endpoints que exponen las funcionalidades del sistema.
- **Dominio**: Incluye las clases abstractas y modelos que definen la estructura de datos y las interacciones entre capas.
- **Infraestructura**: Se encarga de la configuración de la base de datos y la implementación de los repositorios para acceder y manipular los datos.

### Manejo de Errores
Se utilizan bloques `try-catch` en los endpoints para capturar y manejar excepciones. Las excepciones se generan con códigos HTTP específicos para proporcionar respuestas claras sobre el error ocurrido.

### Pruebas
Se han implementado pruebas unitarias centradas en los casos de uso, utilizando mocks para simular interacciones con dependencias externas y asegurar que la lógica de negocio funcione correctamente.

### Escalabilidad
Para escalar la solución, se recomienda modificar la implementación de la lectura de bases de datos para permitir el escaneo de múltiples bases simultáneamente, en lugar de una a la vez. La estructura modular del proyecto facilita la escalabilidad, permitiendo que el sistema se expanda sin perder claridad.

### Mantenibilidad
La organización en capas y la división en carpetas aseguran que el flujo del programa sea claro y el mantenimiento sea sencillo.

### Seguridad
Se ha implementado un endpoint para la creación de usuarios y otro para la autenticación mediante JWT (JSON Web Tokens). El token generado se valida en los otros endpoints para asegurar que solo los usuarios autenticados puedan acceder a las funcionalidades.Ademas se encriptan los datos sensibles antes de guardarlos en la base de datos.

## Conclusión
La aplicación proporciona una solución dinámica para la clasificación de datos, permitiendo la identificación y análisis basados en el nombre de las columnas de las tablas en la base de datos. La implementación permite añadir o eliminar clasificaciones y alias según sea necesario. Además, la base de datos está diseñada para ejecutar múltiples escaneos, con la capacidad de organizar las versiones y generar informes sobre el análisis realizado.

## Mejoras Futuras
1. **Integración de DLP**: Se podría considerar la implementación de análisis de datos utilizando tecnologías DLP para mejorar la precisión en la clasificación de columnas y tablas.
2. **Ampliación de Alias**: Ampliar la lista de alias y clasificaciones para cubrir un rango más amplio de tipos de información, guiado por las buenas prácticas y directrices documentadas de la empresa.
