# Cada categoria suma exactamente 100 puntos si se marcan todos los checks.
# El puntaje de cada categoria va de 0 a 100 segun las casillas marcadas.

PREGUNTAS_POR_CATEGORIA = {
    "Habilidades tecnicas": [
        ("Maneja algun lenguaje de programacion",       20),
        ("Tiene experiencia con bases de datos",         20),
        ("Conoce redes o infraestructura IT",            15),
        ("Ha trabajado con APIs o servicios web",        20),
        ("Usa herramientas de control de versiones (Git)", 15),
        ("Tiene conocimientos de ciberseguridad",        10),
    ],
    "Certificados": [
        ("Tiene titulo universitario",                   30),
        ("Posee certificacion tecnica reconocida",       25),
        ("Cuenta con certificacion en idiomas (B2+)",   20),
        ("Tiene diplomado o especializacion",            15),
        ("Ha realizado cursos con certificado (Coursera, etc.)", 10),
    ],
    "Experiencia": [
        ("Mas de 3 anos de experiencia laboral",         40),
        ("Entre 1 y 3 anos de experiencia",              30),
        ("Ha liderado equipos de trabajo",               20),
        ("Tiene experiencia en el sector requerido",     10),
    ],
    "Gestion de proyectos": [
        ("Conoce metodologias agiles (Scrum/Kanban)",    30),
        ("Ha gestionado proyectos con presupuesto",      25),
        ("Usa herramientas de gestion (Jira, Trello)",   20),
        ("Ha entregado proyectos en tiempo y forma",     25),
    ],
    "Comunicacion": [
        ("Se expresa claramente por escrito",            30),
        ("Tiene habilidades de presentacion oral",       30),
        ("Habla mas de un idioma",                       20),
        ("Tiene experiencia en atencion al cliente",     20),
    ],
    "Pensamiento critico": [
        ("Resuelve problemas de forma autonoma",         40),
        ("Propone mejoras en procesos existentes",       35),
        ("Tiene capacidad analitica demostrable",        25),
    ],
}

CATEGORIAS = list(PREGUNTAS_POR_CATEGORIA.keys())
