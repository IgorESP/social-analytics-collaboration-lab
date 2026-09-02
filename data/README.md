# Datos de la red social ficticia

Los tres ficheros CSV (UTF-8, separador `,`) son ficticios y se han generado de
forma determinista. Contienen **errores intencionados** para practicar la
limpieza de datos: duplicados, espacios sobrantes, códigos de país en
minúsculas, publicaciones vacías, tipos de interacción mal escritos y likes
repetidos.

El contrato de columnas está definido en `src/social_analytics/schema.py` y lo
comprueba `tests/test_schema.py`. **Cambiar una columna es cambiar el
contrato**: hay que actualizar a la vez los CSV, el esquema, el código y los
tests.

## users.csv

| Columna       | Tipo     | Descripción                                   |
|---------------|----------|-----------------------------------------------|
| `user_id`     | entero   | Identificador único del usuario               |
| `username`    | texto    | Nombre de usuario (sin @)                     |
| `country`     | texto    | Código ISO de dos letras (puede faltar)       |
| `signup_date` | fecha    | Fecha de alta (AAAA-MM-DD)                    |
| `followers`   | entero   | Número de seguidores                          |
| `verified`    | booleano | Cuenta verificada (`True`/`False`)            |

## posts.csv

| Columna      | Tipo       | Descripción                                    |
|--------------|------------|------------------------------------------------|
| `post_id`    | entero     | Identificador único de la publicación          |
| `author_id`  | entero     | `user_id` del autor                            |
| `created_at` | fecha-hora | Momento de publicación (AAAA-MM-DD HH:MM:SS)   |
| `text`       | texto      | Texto con hashtags (#tema) y menciones (@user) |

## interactions.csv

| Columna          | Tipo       | Descripción                                    |
|------------------|------------|------------------------------------------------|
| `interaction_id` | entero     | Identificador único de la interacción          |
| `post_id`        | entero     | Publicación que recibe la interacción          |
| `actor_id`       | entero     | `user_id` de quien interactúa                  |
| `kind`           | texto      | `like`, `comment` o `share`                    |
| `created_at`     | fecha-hora | Momento de la interacción                      |
